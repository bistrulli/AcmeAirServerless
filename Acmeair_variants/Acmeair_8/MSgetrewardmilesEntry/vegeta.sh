echo "GET https://europe-north1-my-microservice-test-project.cloudfunctions.net/java-http-function"| vegeta attack -rate 50 -duration=30s| vegeta report -type text

