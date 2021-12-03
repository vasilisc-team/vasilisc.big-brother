#!/bin/bash

GIT_COMMIT=$(cat .git_commit)

curl \
    -X POST \
    -H 'Content-Type: application/json' \
    -d "{\"chat_id\": \"${TG_TO}\", \"text\": \"<pre>Run container from commit: ${GIT_COMMIT}</pre>\", \"disable_notification\": true, \"parse_mode\": \"html\"}" \
    https://api.telegram.org/bot${TG_TOKEN}/sendMessage

source /app/env/bin/activate

python3 \
    ./manage.py \
    runsslserver 0.0.0.0:443 \
    --static