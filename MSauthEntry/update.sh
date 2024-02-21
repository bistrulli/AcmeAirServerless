#! /bin/sh

#https://cloud.google.com/sdk/gcloud/reference/run/services/update#--max-instances
gcloud run services update msauthentry \
--concurrency=$1 \
--project=modellearning \
--region=northamerica-northeast1 \
--max-instances=$2 \
--min-instances=$3 
