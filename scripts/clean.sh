#!/bin/bash
# Locally run `chmod u+x <path to clean.sh>` to make it locally executable :)

# Remove unused variables in directory in which command was run
poetry run autoflake -r --in-place --remove-unused-variables .

# Sort using in directory in which command was run
poetry run isort -rc .

# Run formatting tool black in directory which command was run
poetry run black .