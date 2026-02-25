import os

base_dir = os.path.dirname(os.path.abspath(__file__))
repos = [
    "cg-test-audit",
    "cg-test-change",
    "cg-test-crypto",
    "cg-test-iac",
    "cg-test-iam",
    "cg-test-input",
    "cg-test-sbom",
    "cg-test-secrets",
    "cg-fedramp-test-audit",
    "cg-fedramp-test-change",
    "cg-fedramp-test-crypto",
    "cg-fedramp-test-iac",
    "cg-fedramp-test-iam",
    "cg-fedramp-test-input",
    "cg-fedramp-test-sbom",
    "cg-fedramp-test-secrets"
]

readme_template = """# {repo_name}

A test python project for {repo_name} containing intentionally vulnerable code to validate [ControlGate](https://github.com/sadayamuthu/controlgate).

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
"""

for repo in repos:
    readme_path = os.path.join(base_dir, repo, "README.md")
    
    with open(readme_path, "w") as f:
        f.write(readme_template.format(repo_name=repo))
        
print("Successfully generated all README.md files!")
