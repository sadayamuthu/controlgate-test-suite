#!/bin/bash
pip install controlgate

for d in cg-test-*; do
  if [ -d "$d" ]; then
    echo "======================================"
    echo "Processing $d"
    echo "======================================"
    cd "$d"
    
    # If the scaffold files are untracked, we need to commit them to our feature branch.
    # First ensure we are on the branch
    git checkout -b feature/python-scaffold > /dev/null 2>&1 || git checkout feature/python-scaffold > /dev/null 2>&1
    
    # Stage newly created files
    git add pyproject.toml README.md src tests
    
    echo "--- Running pre-commit scan (markdown) ---"
    controlgate scan --mode pre-commit --format markdown
    
    # Commit changes 
    git commit -m "Scaffold python project structure" > /dev/null 2>&1 || true
    
    echo "--- Running PR scan against main (json) ---"
    controlgate scan --mode pr --target-branch main --format json
    
    echo "--- Running PR scan against main (markdown) ---"
    controlgate scan --mode pr --target-branch main --format markdown
    
    cd ..
  fi
done
