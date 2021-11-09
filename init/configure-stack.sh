#!/bin/bash


# Wait for Elasticsearch to start up before doing anything.
until curl -u elastic:changeme -s http://elasticsearch:9200/_cat/health -o /dev/null; do
    echo Waiting for Elasticsearch...
    sleep 1
done

echo "Setting Elasticsearch password to ${ES_PASSWORD}"
curl -s -XPUT -u elastic:changeme 'elasticsearch:9200/_security/user/elastic/_password' -H "Content-Type: application/json" -d "{
  \"password\" : \"${ES_PASSWORD}\"
}"

curl -s -XPUT -u elastic:${ES_PASSWORD} 'elasticsearch:9200/_security/user/kibana/_password' -H "Content-Type: application/json" -d "{
  \"password\" : \"${ES_PASSWORD}\"
}"

curl -s -XPUT -u elastic:${ES_PASSWORD} 'elasticsearch:9200/_security/user/logstash_system/_password' -H "Content-Type: application/json" -d "{
  \"password\" : \"${ES_PASSWORD}\"
}"


curl -s -XPUT -u elastic:${ES_PASSWORD} 'elasticsearch:9200/_ingest/pipeline/search_event_pipeline' -H "Content-Type: application/json" -d "{
 \"description\": \"Takes the eventTime field and turns it into a date field\",
    \"processors\": [
        {
            \"date\": {
                \"field\": \"timestamp\",
                \"target_field\": \"@timestamp\",
                \"formats\": [
                    \"YYYY-MM-DD HH:mm:ss\"
                ]
            }
        }
    ],
    \"on_failure\": [
        {
            \"set\": {
                \"field\": \"_index\",
                \"value\": \"failed-{{_index}}\"
            }
        },
        {
            \"set\": {
                \"field\": \"error\",
                \"value\": \"{{_ingest.on_failure_message}}\"
            }
        }
    ]
}"


# Wait for Kibana to start up before doing anything.
until curl -s http://kibana:5601/login -o /dev/null; do
    echo Waiting for Kibana...
    sleep 1
done


# Set the default index pattern.
curl -s -XPUT -u elastic:${ES_PASSWORD} http://elastic:${ES_PASSWORD}@elasticsearch:9200/.kibana/config/${ELASTIC_VERSION} -H "Content-Type: application/json" \
     -d "{\"defaultIndex\" : \"${ES_DEFAULT_INDEX_PATTERN}\"}"
