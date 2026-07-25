## Summary

-

## Verification

Paste the real checks run, with links or command output where useful.

```text

```

## Cross-platform text integrity — conditional

Use this section only if the change pins, fingerprints, verifies, or generates from **text source material** using a checksum or equivalent content hash.

- [ ] N/A — this PR has no text-source checksum/fingerprint contract.
- [ ] The contract hashes canonical UTF-8 text after normalising `CRLF` and bare `CR` line endings to `LF`; it does **not** hash checkout-specific raw working-tree bytes.
- [ ] A regression proves equivalent LF and CRLF renderings validate against the same pin and produce identical downstream output.

## Safety and review

- [ ] No secrets, tokens, raw private material, or `not-public` content is included.
- [ ] Independent reviewer requested:
- [ ] Merge authority / human gate, if any:
