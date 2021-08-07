rm -rf logs
mkdir logs
elasticsearch > logs/elasticsearch.log &
echo $! > logs/elasticsearch.pid

cd rasa
 
rasa run actions > ../logs/rasa-actions.log &
echo $! > ../logs/rasa-actions.pid
rasa run > ../logs/rasa-server.log &
echo $! > ../logs/rasa-server.pid
