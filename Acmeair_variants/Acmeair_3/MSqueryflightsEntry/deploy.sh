#! /bin/sh
gcloud beta functions deploy msqueryflightsentry \
--gen2 \
--runtime=java17 \
--region=northamerica-northeast1 \
--source=. \
--entry-point=functions.Logic \
--memory=1024MB \
--cpu=1 \
--trigger-http \
--allow-unauthenticated \
--project my-microservice-test-project \
--max-instances=100 \
--min-instances=1
