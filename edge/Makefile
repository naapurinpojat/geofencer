# Makefile

# Define variables
REVISION_SCRIPT := ../getrevision.sh
REVISION=$(shell ./${REVISION_SCRIPT})
GIT_VERSION_PY := gitversion.py
PACKAGE_NAME := ../snowdog.tgz

# Define targets and rules
all: $(GIT_VERSION_PY) $(PACKAGE_NAME)

# Run getrevision.sh and store output to a variable
$(GIT_VERSION_PY):
	@echo "Generating git version information..."
	@REVISION=$$(./$(REVISION_SCRIPT)); \
	echo "git_revision = '$$REVISION'" > $(GIT_VERSION_PY)
	@echo "Git version information stored in $(GIT_VERSION_PY)"

# Tgz the Python files into a package named by snowdog.tgz
$(PACKAGE_NAME): $(GIT_VERSION_PY)
	@echo "Creating package $(PACKAGE_NAME)..."
	@tar -czvf ../$(PACKAGE_NAME) *
	@echo "Package $(PACKAGE_NAME) created successfully"

# Clean up intermediate files
clean:
	@echo "Cleaning up..."
	@rm -f $(GIT_VERSION_PY) $(PACKAGE_NAME)
	@rm -rf __pycache__
	@echo "Cleanup complete"

# PHONY targets to avoid conflicts with file names
.PHONY: all clean

