#!/bin/sh
export FLASK_RUN_HOST=0.0.0.0
export DATABASE_PASSWORD='1ABbCc#'

python3 -m flask --app hello11app run --debug