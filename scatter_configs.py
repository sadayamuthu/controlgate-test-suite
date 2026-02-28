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
      run: pip install git+https://github.com/sadayamuthu/controlgate.git@main
      
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
    - pip install git+https://github.com/sadayamuthu/controlgate.git@main
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
                sh 'pip install git+https://github.com/sadayamuthu/controlgate.git@main'
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

controlgate_yml_standard = """baseline: moderate
gov: false
"""

controlgate_yml_gov = """baseline: moderate
gov: true
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
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "compliant.py"), "w") as f:
        f.write(compliant_code)

    # 7. .controlgate.yml Configuration File
    # Define standard vs fedramp config based on the repo name prefix
    with open(os.path.join(repo_path, ".controlgate.yml"), "w") as f:
        if repo.startswith("cg-fedramp-test"):
            f.write(controlgate_yml_gov)
        else:
            f.write(controlgate_yml_standard)

print("Successfully injected enterprise configurations and compliant code into all projects!")
