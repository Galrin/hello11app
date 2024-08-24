#!/bin/bash

service mariadb start

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install .
pip install python-dotenv

nc 0.0.0.0 -l 8000