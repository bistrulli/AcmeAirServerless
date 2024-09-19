#! /bin/sh

#https://cloud.google.com/sdk/gcloud/reference/run/services/update#--max-instances
gcloud run services update msqueryflightsentry \
--concurrency=$1 \
--project=my-microservice-test-project  \
--region=northamerica-northeast1 \
--max-instances=$2 \
--min-instances=$3 
