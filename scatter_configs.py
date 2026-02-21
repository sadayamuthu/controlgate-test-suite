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
    "cg-test-secrets"
]

github_action = """name: ControlGate Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install ControlGate
      run: pip install controlgate
      
    - name: Run ControlGate PR Scan
      if: github.event_name == 'pull_request'
      run: |
        controlgate scan --mode pr --target-branch origin/main --format github
        
    - name: Run ControlGate Full Scan
      if: github.event_name == 'push'
      run: |
        controlgate scan --mode full --format markdown
"""

gitlab_ci = """stages:
  - scan

controlgate_scan:
  stage: scan
  image: python:3.12
  script:
    - pip install controlgate
    - |
      if [ -n "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME" ]; then
        controlgate scan --mode pr --target-branch origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME --format gitlab
      else
        controlgate scan --mode full --format gitlab
      fi
"""

jenkinsfile = """pipeline {
    agent {
        docker { image 'python:3.12' }
    }
    stages {
        stage('Install ControlGate') {
            steps {
                sh 'pip install controlgate'
            }
        }
        stage('Scan Code') {
            steps {
                script {
                    if (env.CHANGE_ID) {
                        sh 'controlgate scan --mode pr --target-branch origin/${CHANGE_TARGET} --format jenkins'
                    } else {
                        sh 'controlgate scan --mode full --format html'
                    }
                }
            }
        }
    }
}
"""

pre_commit_config = """repos:
  - repo: local
    hooks:
      - id: controlgate
        name: ControlGate Security Scan
        entry: controlgate scan --mode pre-commit --format markdown
        language: system
        pass_filenames: false
"""

gitignore_content = """# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Pytest / Coverage
.pytest_cache/
.coverage
htmlcov/

# ControlGate
.controlgate/

# IDEs
.idea/
.vscode/
*.swp
"""

compliant_code = """import hashlib
import logging
import os

logging.basicConfig(level=logging.INFO)

# 1. Compliant Crypto (SHA-256 instead of MD5/SHA-1)
def hash_securely(data: str) -> str:
    \"\"\"Hashes data using a secure algorithm (SHA-256).\"\"\"
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# 2. Compliant Logging (No secrets)
def process_user_login(username: str):
    \"\"\"Logs user activity without recording their password or PII.\"\"\"
    logging.info(f"User {username} successfully authenticated.")
    return True

# 3. Compliant Secrets (Using Environment Variables)
def get_database_connection():
    \"\"\"Retrieves database connection string securely from the environment.\"\"\"
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "app_user")
    
    # We do NOT hardcode the password.
    db_password = os.environ.get("DB_PASSWORD")
    
    if not db_password:
        raise ValueError("Database password must be set in the environment.")
        
    return f"postgresql://{db_user}:{db_password}@{db_host}/prod"
"""

for repo in repos:
    repo_path = os.path.join(base_dir, repo)
    
    # 1. GitHub Actions
    github_dir = os.path.join(repo_path, ".github", "workflows")
    os.makedirs(github_dir, exist_ok=True)
    with open(os.path.join(github_dir, "controlgate.yml"), "w") as f:
        f.write(github_action)
        
    # 2. GitLab CI
    with open(os.path.join(repo_path, ".gitlab-ci.yml"), "w") as f:
        f.write(gitlab_ci)
        
    # 3. Jenkinsfile
    with open(os.path.join(repo_path, "Jenkinsfile"), "w") as f:
        f.write(jenkinsfile)
        
    # 4. pre-commit
    with open(os.path.join(repo_path, ".pre-commit-config.yaml"), "w") as f:
        f.write(pre_commit_config)
        
    # 5. .gitignore
    with open(os.path.join(repo_path, ".gitignore"), "w") as f:
        f.write(gitignore_content)
        
    # 6. Compliant Code Example
    src_dir = os.path.join(repo_path, "src", repo.replace("-", "_"))
    with open(os.path.join(src_dir, "compliant.py"), "w") as f:
        f.write(compliant_code)

print("Successfully injected enterprise configurations and compliant code into all projects!")
