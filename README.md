# Cherry Blossom Spaceship — Organization `.github`

Default community-health files and shared starters for repositories across the Cherry Blossom Spaceship org. Per-repository files and settings supersede these defaults.

## Contents

- `.gitattributes` — canonical LF line-ending policy for new repositories.

## Line endings: read this before copying

`.gitattributes` **does not auto-propagate** from this repository. GitHub only propagates community-health files from an org `.github` repo (issue/PR templates, CONTRIBUTING, SECURITY, and friends). This file is the canonical copy: when bootstrapping a new repository, copy it in as part of the initial commit, and keep binary exclusions in sync here so the org shares one policy.

Optional enforcement: a reusable `workflow_call` drift-check can live here and be wired per-repository via a thin caller workflow, so a missing `.gitattributes` fails CI. Per-repo files remain the actual enforcement for each repository.
