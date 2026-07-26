from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "verify_sovereignty_portability.py"
spec = importlib.util.spec_from_file_location("sovereignty_gate", SCRIPT)
assert spec and spec.loader
GATE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(GATE)


class GateFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run("git", "init", "-q")
        self.run("git", "config", "user.name", "fixture")
        self.run("git", "config", "user.email", "fixture@example.invalid")
        (self.root / ".github").mkdir()
        self.registry([])
        (self.root / "portable.py").write_text("value = 'semantic'\n", encoding="utf-8")
        self.run("git", "add", ".")
        self.run("git", "commit", "-qm", "base")
        self.base = self.run("git", "rev-parse", "HEAD").stdout.strip()

    def run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(args, cwd=self.root, text=True, capture_output=True, check=True)

    def registry(self, exceptions: list[dict[str, str]]) -> None:
        path = self.root / ".github" / "sovereignty-portability-registry.json"
        path.write_text(json.dumps({"version": 1, "exceptions": exceptions}), encoding="utf-8")

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def close(self) -> None:
        self.temp.cleanup()


class SovereigntyGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = GateFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def scan(self) -> list[str]:
        self.fixture.run("git", "add", ".")
        self.fixture.run("git", "commit", "-qm", "change")
        return GATE.scan(self.fixture.root, self.fixture.base)

    def test_allows_environment_and_repo_root_discovery(self) -> None:
        self.fixture.write(
            "portable.py",
            "from pathlib import Path\nroot = Path(__file__).resolve().parents[1]\nendpoint = __import__('os').environ['APP_ROOT']\n",
        )
        self.assertEqual([], self.scan())

    def test_rejects_native_process_receiving_msys_path(self) -> None:
        msys = "/" + "c" + "/" + "workspace"
        self.fixture.write("launch.py", f"subprocess.run(['native-tool', '{msys}'], check=True)\n")
        violations = self.scan()
        self.assertTrue(any("POSIX home or mount path" in item for item in violations), violations)

    def test_rejects_windows_path_prepended_to_bash_path(self) -> None:
        native = "C" + ":" + chr(92) + "tools"
        self.fixture.write("launch.sh", f"PATH='{native}:$PATH'\nexport PATH\n")
        violations = self.scan()
        self.assertTrue(any("Windows drive path" in item for item in violations), violations)

    def test_exact_unexpired_exception_is_allowed(self) -> None:
        native = "C" + ":" + chr(92) + "adapter"
        line = f"native_adapter '{native}'"
        self.fixture.registry(
            [{
                "text": line,
                "reason": "platform adapter boundary",
                "issue": "https://github.com/example/repository/issues/1",
                "expires": "2099-01-01",
            }]
        )
        self.fixture.write("adapter.sh", line + "\n")
        self.assertEqual([], self.scan())

    def test_expired_exception_fails_closed(self) -> None:
        self.fixture.registry(
            [{
                "text": "legacy adapter",
                "reason": "temporary fixture",
                "issue": "https://github.com/example/repository/issues/1",
                "expires": "2000-01-01",
            }]
        )
        with self.assertRaises(SystemExit) as error:
            self.scan()
        self.assertIn("expired", str(error.exception))

    def test_missing_registry_fails_closed(self) -> None:
        (self.fixture.root / ".github" / "sovereignty-portability-registry.json").unlink()
        with self.assertRaises(SystemExit) as error:
            self.scan()
        self.assertIn("missing required registry contract", str(error.exception))


if __name__ == "__main__":
    unittest.main()
