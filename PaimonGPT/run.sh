#!/bin/bash

# shellcheck disable=SC2164
cd /workspace/PaimonGPT
nginx -c /workspace/PaimonGPT/nginx_paimonGPT.conf
nohup python manage_paimongpt.py >/dev/null 2>&1 &
