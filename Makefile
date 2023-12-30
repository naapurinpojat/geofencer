# Makefile

# Define variables
REVISION_SCRIPT := getrevision.sh
REVISION=$(shell ./${REVISION_SCRIPT})
GIT_VERSION_PY := edge/gitversion.py
GIT_VERSION_PHP := web_app/gitversion.php
PACKAGE_NAME := snowdog.tgz

# Define targets and rules
all: $(GIT_VERSION_PY) $(GIT_VERSION_PHP) $(PACKAGE_NAME)

$(GIT_VERSION_PHP):
	@echo "Generating git version information..."
	@REVISION=$$(./$(REVISION_SCRIPT)); \
	echo "<?php" > $(GIT_VERSION_PHP); \
	echo "define('GIT_REVISION', '$$REVISION');" >> $(GIT_VERSION_PHP)
	echo "?>" >> $(GIT_VERSION_PHP)
	@echo "Git version information stored in $(GIT_VERSION_PHP)"

# Run getrevision.sh and store output to a variable
$(GIT_VERSION_PY):
	@echo "Generating git version information..."
	@REVISION=$$(./$(REVISION_SCRIPT)); \
	echo "git_revision = '$$REVISION'" > $(GIT_VERSION_PY)
	@echo "Git version information stored in $(GIT_VERSION_PY)"

# Tgz the Python files into a package named by snowdog.tgz
$(PACKAGE_NAME): $(GIT_VERSION_PY)
	@echo "Creating package $(PACKAGE_NAME)..."
	@cd edge && tar -czvf ../$(PACKAGE_NAME) *
	@echo "Package $(PACKAGE_NAME) created successfully"

# Clean up intermediate files
clean:
	@echo "Cleaning up..."
	@rm -f $(GIT_VERSION_PY) $(PACKAGE_NAME) $(GIT_VERSION_PHP)
	@echo "Cleanup complete"

test:
	@echo "Running tests..."
	@./run_rpa_tests.sh

# PHONY targets to avoid conflicts with file names
.PHONY: all clean

