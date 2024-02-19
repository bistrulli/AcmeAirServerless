#! /bin/sh
locust --headless -f SimpleWorkload.py  --u $1 --run-time=$2  --host=https://northamerica-northeast1-modellearning.cloudfunctions.net/
#locust --headless -f SimpleWorkload.py,sinShape.py  --u $1 --host=https://northamerica-northeast1-modellearning.cloudfunctions.net/f3