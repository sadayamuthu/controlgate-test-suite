#!/usr/bin/env python3
"""
Test runner that executes ControlGate scans across all child test projects.
"""
import os
import subprocess
import sys
from pathlib import Path

PROJECTS = [
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

BASE_DIR = Path(__file__).parent


def scan_project(project: str, mode: str = "pr", target_branch: str = "main",
                 fmt: str = "markdown") -> int:
    project_dir = BASE_DIR / project
    if not project_dir.is_dir():
        print(f"  SKIP: {project} directory not found")
        return -1

    controlgate = os.path.join(os.path.dirname(sys.executable), "controlgate")
    cmd = [controlgate, "scan", "--mode", mode, "--format", fmt]
    if mode == "pr":
        cmd += ["--target-branch", target_branch]

    result = subprocess.run(cmd, cwd=project_dir, capture_output=False)
    return result.returncode


def main():
    mode = "pr"
    fmt = "markdown"
    target_branch = "main"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            i += 2
        elif args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i] == "--target-branch" and i + 1 < len(args):
            target_branch = args[i + 1]
            i += 2
        elif args[i] == "--help":
            print("Usage: cg-test-all [--mode pr|pre-commit] [--format markdown|json|sarif] [--target-branch BRANCH]")
            print("\nRuns controlgate scan across all test projects.")
            return 0
        else:
            i += 1

    results = {}
    for project in PROJECTS:
        print(f"\n{'=' * 50}")
        print(f"  {project}")
        print(f"{'=' * 50}")
        rc = scan_project(project, mode=mode, target_branch=target_branch, fmt=fmt)
        results[project] = rc

    print(f"\n{'=' * 50}")
    print("  SUMMARY")
    print(f"{'=' * 50}")
    for project, rc in results.items():
        if rc == -1:
            status = "SKIPPED"
        elif rc == 0:
            status = "PASS"
        else:
            status = "BLOCK"
        print(f"  {project:<25} {status}")

    blocked = sum(1 for rc in results.values() if rc > 0)
    passed = sum(1 for rc in results.values() if rc == 0)
    skipped = sum(1 for rc in results.values() if rc == -1)
    print(f"\n  Total: {len(results)} | Blocked: {blocked} | Passed: {passed} | Skipped: {skipped}")

    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
