import os
import shutil

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
    "cg-test-aiml",
    "cg-test-api",
    "cg-test-container",
    "cg-test-deps",
    "cg-test-incident",
    "cg-test-license",
    "cg-test-memsafe",
    "cg-test-observability",
    "cg-test-privacy",
    "cg-test-resilience",
    "cg-fedramp-test-audit",
    "cg-fedramp-test-change",
    "cg-fedramp-test-crypto",
    "cg-fedramp-test-iac",
    "cg-fedramp-test-iam",
    "cg-fedramp-test-input",
    "cg-fedramp-test-sbom",
    "cg-fedramp-test-secrets",
    "cg-fedramp-test-aiml",
    "cg-fedramp-test-api",
    "cg-fedramp-test-container",
    "cg-fedramp-test-deps",
    "cg-fedramp-test-incident",
    "cg-fedramp-test-license",
    "cg-fedramp-test-memsafe",
    "cg-fedramp-test-observability",
    "cg-fedramp-test-privacy",
    "cg-fedramp-test-resilience"
]

vuln_files = {
    "audit_vuln.py": os.path.join(base_dir, "cg-test-audit/src/cg_test_audit/vulnerable.py"),
    "change_vuln.py": os.path.join(base_dir, "cg-test-change/src/cg_test_change/vulnerable.py"),
    "crypto_vuln.py": os.path.join(base_dir, "cg-test-crypto/src/cg_test_crypto/vulnerable.py"),
    "iac_vuln.tf": os.path.join(base_dir, "cg-test-iac/src/cg_test_iac/main.tf"),
    "iam_policy.json": os.path.join(base_dir, "cg-test-iam/src/cg_test_iam/policy.json"),
    "input_vuln.py": os.path.join(base_dir, "cg-test-input/src/cg_test_input/vulnerable.py"),
    "secrets_vuln.py": os.path.join(base_dir, "cg-test-secrets/src/cg_test_secrets/vulnerable.py"),
    "aiml_vuln.py": os.path.join(base_dir, "cg-test-aiml/src/cg_test_aiml/vulnerable.py"),
    "api_vuln.py": os.path.join(base_dir, "cg-test-api/src/cg_test_api/vulnerable.py"),
    "container_vuln.Dockerfile": os.path.join(base_dir, "cg-test-container/src/cg_test_container/Dockerfile"),
    "requirements_deps_vuln.txt": os.path.join(base_dir, "cg-test-deps/src/cg_test_deps/vulnerable.txt"),
    "incident_vuln.py": os.path.join(base_dir, "cg-test-incident/src/cg_test_incident/vulnerable.py"),
    "requirements_license_vuln.txt": os.path.join(base_dir, "cg-test-license/src/cg_test_license/vulnerable.txt"),
    "memsafe_vuln.py": os.path.join(base_dir, "cg-test-memsafe/src/cg_test_memsafe/vulnerable.py"),
    "observability_vuln.py": os.path.join(base_dir, "cg-test-observability/src/cg_test_observability/vulnerable.py"),
    "privacy_vuln.py": os.path.join(base_dir, "cg-test-privacy/src/cg_test_privacy/vulnerable.py"),
    "resilience_vuln.py": os.path.join(base_dir, "cg-test-resilience/src/cg_test_resilience/vulnerable.py"),
}

for repo in repos:
    src_dir = os.path.join(base_dir, repo, "src", repo.replace("-", "_"))
    
    # Ensure src dir exists
    os.makedirs(src_dir, exist_ok=True)
    
    # Copy all vuln files into this repo
    for name, path in vuln_files.items():
        if os.path.exists(path):
            # Don't overwrite itself if it's the source, just copy to the new name if different, 
            # or skip if same. But they have different names in `vuln_files` vs disk (`vulnerable.py` -> `audit_vuln.py`).
            dest_path = os.path.join(src_dir, name)
            shutil.copy(path, dest_path)
            
    # Update pyproject.toml to include the vulnerable SBOM dependency
    pyproject_path = os.path.join(base_dir, repo, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, "r") as f:
            content = f.read()
            
        if "requests==2.20.0" not in content:
            content = content.replace('    "controlgate"\n]', '    "controlgate",\n    "requests==2.20.0"\n]')
            with open(pyproject_path, "w") as f:
                f.write(content)

print("Finished scattering all vulnerabilities to all projects!")
