#!/bin/sh

set -o errexit
set -o nounset

python -m celery -A tradeapp_django worker --loglevel=info
