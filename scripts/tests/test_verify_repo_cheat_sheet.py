#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "verify_repo_cheat_sheet.py"
TEMPLATE = ROOT / "templates" / "REPO_CHEAT_SHEET.md"


class RepositoryCheatSheetContractTests(unittest.TestCase):
    def run_check(self, path: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(CHECKER), "--template", str(path)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_template_passes(self) -> None:
        result = self.run_check(TEMPLATE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_over_line_budget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = pathlib.Path(directory) / "sheet.md"
            shutil.copyfile(TEMPLATE, copy)
            copy.write_text(copy.read_text(encoding="utf-8") + "\n" * 121, encoding="utf-8")
            result = self.run_check(copy)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("line count", result.stdout)

    def test_rejects_more_than_eight_active_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = pathlib.Path(directory) / "sheet.md"
            content = TEMPLATE.read_text(encoding="utf-8")
            exemplar = "| `migration-fixture-impact` | changing a migration | Locate the migration-version fixture before changing the migration count. | `PR/issue URLs` | `test/PR URL` | `role or team` | `YYYY-MM-DD` | `verified` | `—` |"
            content = content.replace(exemplar, "\n".join([exemplar] * 9))
            copy.write_text(content, encoding="utf-8")
            result = self.run_check(copy)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("active invariant rows", result.stdout)

    def test_rejects_missing_controlled_tag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = pathlib.Path(directory) / "sheet.md"
            content = TEMPLATE.read_text(encoding="utf-8").replace(
                "| `provider-safety` | explicit provider/model/network guard |\n", ""
            )
            copy.write_text(content, encoding="utf-8")
            result = self.run_check(copy)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing controlled tags", result.stdout)


if __name__ == "__main__":
    unittest.main()
