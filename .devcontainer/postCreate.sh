#! usr/local/env bash

python -m venv env
source env/bin/activate
pip install -r requirements.txt

bash ./.devcontainer/cloneRepos.sh
