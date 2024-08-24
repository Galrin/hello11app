#!/bin/bash

service mariadb start

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install .
pip install python-dotenv

bash ./run.sh