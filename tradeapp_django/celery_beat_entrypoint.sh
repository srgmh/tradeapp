#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
python -m celery -A tradeapp_django beat -l info
