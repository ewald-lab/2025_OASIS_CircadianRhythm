#!/bin/bash

uv venv dex-env --python=python3.11
source dex-env/bin/activate
uv pip install -r requirements.txt
python -m ipykernel install --user --name=dex-env --display-name "Python (dex-env)"

echo "To activate later: source dex-env/bin/activate"