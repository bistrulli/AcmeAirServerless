echo "GET https://europe-north1-modellearning.cloudfunctions.net/java-http-function"| vegeta attack -rate 50 -duration=30s| vegeta report -type text

