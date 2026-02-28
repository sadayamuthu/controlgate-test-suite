# ControlGate Test Suite

Parent project that orchestrates [ControlGate](https://github.com/sadayamuthu/controlgate) security scans across multiple test repositories, each containing intentionally vulnerable code targeting specific NIST SP 800-53 security gates.

## Test Projects

| Project | Gate Tested | Vulnerabilities |
|---------|-------------|-----------------|
| `cg-test-audit` | Audit & Accountability | Sensitive data logging, missing audit trails |
| `cg-test-change` | Change Control | Unreviewed deployments, missing change tickets |
| `cg-test-crypto` | Cryptographic Protection | MD5/SHA-1 usage, weak algorithms |
| `cg-test-iac` | Infrastructure as Code | Public S3 buckets, open security groups, insecure Dockerfiles |
| `cg-test-iam` | Identity & Access Mgmt | Overly permissive IAM policies, wildcard permissions |
| `cg-test-input` | Input Validation | Command injection, shell=True, unsanitized input |
| `cg-test-sbom` | Supply Chain / SBOM | Unpinned deps, known-vulnerable packages |
| `cg-test-secrets` | Secrets Management | Hardcoded API keys, credentials, connection strings |
| `cg-test-aiml` | AI/ML Security | trust_remote_code=True, unsafe model loading |
| `cg-test-api` | API Security | TLS verification disabled |
| `cg-test-container` | Container Security | Root user, privileged containers |
| `cg-test-deps` | Dependency Vulnerability | Unpinned dependencies, HTTP registries |
| `cg-test-incident` | Incident Response | Silenced exceptions, disabled alerts |
| `cg-test-license` | License Compliance | Copyleft licenses (GPL, AGPL) |
| `cg-test-memsafe` | Memory Safety | dynamic code execution, eval() |
| `cg-test-observability` | Observability | Disabled monitoring |
| `cg-test-privacy` | Data Privacy | PII in logs |
| `cg-test-resilience` | Resilience & Backup | Deletion protection disabled |

## Quick Start

```bash
# Install controlgate in a virtual environment
make install

# Run ControlGate PR scans on all test projects
make scan

# Run scans with JSON output
make scan-json

# Run a single project
make scan-cg-test-secrets

# Run pre-commit mode scans
make scan-precommit
```

## Manual Usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install controlgate

# Scan all projects
python test_runner.py --mode pr --format markdown

# Scan a single project
cd cg-test-crypto
controlgate scan --mode pr --target-branch main --format markdown
```

## Project Structure

```
controlgate-test-suite/
├── Makefile                  # Build & scan orchestration
├── pyproject.toml            # Parent project metadata
├── test_runner.py            # Python test runner for all projects
├── README.md
├── run_scans.sh              # Shell-based scan runner
├── scatter_configs.py        # Generates CI configs for all child projects
├── scatter_vulns.py          # Copies vulnerability files across projects
├── update_readme.py          # Generates READMEs for child projects
├── cg-test-audit/            # Each child is an independent git repo
├── cg-test-change/
├── cg-test-crypto/
├── cg-test-iac/
├── cg-test-iam/
├── cg-test-input/
├── cg-test-sbom/
├── cg-test-secrets/
├── cg-test-aiml/
├── cg-test-api/
├── cg-test-container/
├── cg-test-deps/
├── cg-test-incident/
├── cg-test-license/
├── cg-test-memsafe/
├── cg-test-observability/
├── cg-test-privacy/
├── cg-test-resilience/
└── cg-fedramp-test-*/        # FedRAMP variants for all gates
```

Each child project includes:
- `pyproject.toml` with `controlgate` as a dependency
- `requirements.txt` with `controlgate`
- CI configs: GitHub Actions, GitLab CI, Jenkinsfile
- `.pre-commit-config.yaml` for local scanning
- Intentionally vulnerable source code under `src/`

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `scatter_configs.py` | Writes CI/CD configs, `.gitignore`, and compliant code to all child projects |
| `scatter_vulns.py` | Copies vulnerability test files across all child projects |
| `update_readme.py` | Generates standardized `README.md` for each child project |
| `run_scans.sh` | Shell script to run scans across all projects |

Re-scaffold all child projects after changes:

```bash
make setup-projects
```
