#! /bin/sh
gcloud beta functions deploy MScancelbookingEntry \
--gen2 \
--runtime=java17 \
--region=northamerica-northeast1 \
--source=. \
--entry-point=functions.Logic \
--memory=1024MB \
--cpu=1 \
--trigger-http \
--allow-unauthenticated \
--project modellearning \
--max-instances=50 \
--min-instances=1
