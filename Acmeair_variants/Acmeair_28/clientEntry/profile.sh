#! /bin/sh
#locust --headless -f SimpleWorkload.py  --u $1 --run-time=$2  --host=https://northamerica-northeast1-my-microservice-test-project.cloudfunctions.net/
locust --headless -f SimpleWorkload.py,traceShape.py  --u $1 --host=https://northamerica-northeast1-my-microservice-test-project.cloudfunctions.net/