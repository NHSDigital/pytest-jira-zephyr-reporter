# Makefile for pytest-jira-zephyr-reporter

# ==============================================================================
# Project targets

dependencies: # Install dependencies needed to build and test the project @Pipeline
	pip install -e .

build: # Build the project artefact @Pipeline
	python -m build

publish: # Publish the project artefact @Pipeline
	# Publishing handled by twine in CI/CD

deploy: # Deploy the project artefact to the target environment @Pipeline
	# Not applicable for library projects

clean:: # Clean-up project resources @Operations
	rm -rf \
		build/ \
		dist/ \
		*.egg-info/ \
		.pytest_cache/ \
		__pycache__/ \
		.coverage \
		htmlcov/

config:: # Configure development environment @Configuration
	pip install -e ".[dev]"

# ==============================================================================
# Utility targets

help: # Print help @Others
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?# "}; {printf "  %-20s %s\n", $$1, $$2}'

list-variables: # List all the variables available to make @Others
	@$(foreach v, $(sort $(.VARIABLES)),\
		$(if $(filter-out default automatic, $(origin $v)),\
			$(if $(and $(patsubst %_PASSWORD,,$v), $(patsubst %_PASS,,$v), $(patsubst %_KEY,,$v), $(patsubst %_SECRET,,$v)),\
				$(info $v=$($v) ($(value $v)) [$(flavor $v),$(origin $v)]),\
				$(info $v=****** (******) [$(flavor $v),$(origin $v)])\
			)\
		)\
	)

# ==============================================================================

.DEFAULT_GOAL := help
.PHONY: dependencies build publish deploy clean config help list-variables
