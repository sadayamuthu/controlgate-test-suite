# cg-test-api

A test python project for cg-test-api containing intentionally vulnerable code to validate [ControlGate](https://github.com/sadayamuthu/controlgate).

## Installation

Ensure you have python 3.8+ installed.

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install ControlGate:
   ```bash
   pip install controlgate
   ```

## Running ControlGate

You can run `controlgate` against this repository to verify the rules engine can detect the built-in vulnerabilities.

### Scan Staged Changes (Pre-Commit Mode)
To scan only files that are currently staged in git:
```bash
controlgate scan --mode pre-commit --format markdown
```

### Scan PR Diff (PR Mode)
To scan the differences between the current branch and `main`:
```bash
controlgate scan --mode pr --target-branch main --format markdown
```

*Note: You may also use `--format json` to get machine-readable output.*
