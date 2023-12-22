# Makefile

# Define variables
REVISION_SCRIPT := getrevision.sh
GIT_VERSION_PY := gitversion.py
PACKAGE_NAME := dog.zip

# Define targets and rules
all: $(GIT_VERSION_PY) $(PACKAGE_NAME)

# Run getrevision.sh and store output to a variable
$(GIT_VERSION_PY):
	@echo "Generating git version information..."
	@REVISION=$$(./$(REVISION_SCRIPT)); \
	echo "git_revision = '$$REVISION'" > $(GIT_VERSION_PY)
	@echo "Git version information stored in $(GIT_VERSION_PY)"

# Zip the Python files into a package named by dog.zip
$(PACKAGE_NAME): $(GIT_VERSION_PY)
	@echo "Creating package $(PACKAGE_NAME)..."
	@zip -r $(PACKAGE_NAME) *.py
	@echo "Package $(PACKAGE_NAME) created successfully"

# Clean up intermediate files
clean:
	@echo "Cleaning up..."
	@rm -f $(GIT_VERSION_PY) $(PACKAGE_NAME)
	@echo "Cleanup complete"

# PHONY targets to avoid conflicts with file names
.PHONY: all clean

