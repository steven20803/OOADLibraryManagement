#!/bin/bash
isort . --skip=__pycache__ --skip=env
black .
pylint --recursive=y $(git ls-files "*.py" )
