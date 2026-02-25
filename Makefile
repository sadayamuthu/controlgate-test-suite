SHELL := /bin/bash
PYTHON := python3
CG_BRANCH ?= main
VENV := .venv
PIP := $(VENV)/bin/pip
CG := $(VENV)/bin/controlgate
RUNNER := $(VENV)/bin/python test_runner.py

PROJECTS := cg-test-audit cg-test-change cg-test-crypto cg-test-iac \
            cg-test-iam cg-test-input cg-test-sbom cg-test-secrets \
            cg-fedramp-test-audit cg-fedramp-test-change cg-fedramp-test-crypto cg-fedramp-test-iac \
            cg-fedramp-test-iam cg-fedramp-test-input cg-fedramp-test-sbom cg-fedramp-test-secrets

.PHONY: help install scan scan-json scan-sarif clean setup-projects

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: $(VENV)/bin/controlgate ## Create venv and install controlgate

$(VENV)/bin/controlgate:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install git+https://github.com/sadayamuthu/controlgate.git@$(CG_BRANCH)

scan: install ## Run PR scans (markdown) on all test projects
	$(RUNNER) --mode pr --format markdown

scan-json: install ## Run PR scans (JSON) on all test projects
	$(RUNNER) --mode pr --format json

scan-sarif: install ## Run PR scans (SARIF) on all test projects
	$(RUNNER) --mode pr --format sarif

scan-precommit: install ## Run pre-commit scans on all test projects
	$(RUNNER) --mode pre-commit --format markdown

scan-%: install ## Run PR scan on a single project (e.g. make scan-cg-test-audit)
	cd $* && $(CURDIR)/$(CG) scan --mode pr --target-branch main --format markdown

setup-projects: ## Scaffold configs into all child test projects
	$(PYTHON) scatter_configs.py
	$(PYTHON) scatter_vulns.py
	$(PYTHON) update_readme.py

clean: ## Remove venv and generated reports
	rm -rf $(VENV)
	for d in $(PROJECTS); do rm -rf $$d/.controlgate/reports; done
