#!/bin/sh
export FLASK_RUN_HOST=0.0.0.0
export DATABASE_PASSWORD='qwerty'

python3 -m flask --app hello11app run --debug