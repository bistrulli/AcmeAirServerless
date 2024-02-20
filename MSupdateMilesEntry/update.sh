#! /bin/sh

#https://cloud.google.com/sdk/gcloud/reference/run/services/update#--max-instances
gcloud run services update MSupdateMilesEntry \
--concurrency=2 \
--project=modellearning \
--region=northamerica-northeast1 \
--max-instances=100 \
--min-instances=1 
