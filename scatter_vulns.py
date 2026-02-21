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
    "cg-test-secrets"
]

vuln_files = {
    "audit_vuln.py": os.path.join(base_dir, "cg-test-audit/src/cg_test_audit/vulnerable.py"),
    "change_vuln.py": os.path.join(base_dir, "cg-test-change/src/cg_test_change/vulnerable.py"),
    "crypto_vuln.py": os.path.join(base_dir, "cg-test-crypto/src/cg_test_crypto/vulnerable.py"),
    "iac_vuln.tf": os.path.join(base_dir, "cg-test-iac/src/cg_test_iac/main.tf"),
    "iam_policy.json": os.path.join(base_dir, "cg-test-iam/src/cg_test_iam/policy.json"),
    "input_vuln.py": os.path.join(base_dir, "cg-test-input/src/cg_test_input/vulnerable.py"),
    "secrets_vuln.py": os.path.join(base_dir, "cg-test-secrets/src/cg_test_secrets/vulnerable.py"),
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
