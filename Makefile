# Makefile

# Define variables
REVISION_SCRIPT := getrevision.sh
REVISION=$(shell ./${REVISION_SCRIPT})
GIT_VERSION_PHP := web_app/gitversion.php

# Define targets and rules
all: $(GIT_VERSION_PHP) edge

$(GIT_VERSION_PHP):
	@echo "Generating git version information..."
	@REVISION=$$(./$(REVISION_SCRIPT)); \
	echo "<?php" > $(GIT_VERSION_PHP); \
	echo "define('GIT_REVISION', '$$REVISION');" >> $(GIT_VERSION_PHP)
	echo "?>" >> $(GIT_VERSION_PHP)
	@echo "Git version information stored in $(GIT_VERSION_PHP)"

edge:
	make -C edge
# Clean up intermediate files
clean:
	@echo "Cleaning up..."
	@rm -f $(GIT_VERSION_PHP)
	make clean -C edge
	@echo "Cleanup complete"

test:
	@echo "Running tests..."
	@./run_rpa_tests.sh

# PHONY targets to avoid conflicts with file names
.PHONY: all clean edge

