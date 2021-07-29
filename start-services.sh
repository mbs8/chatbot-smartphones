elasticsearch > logs/elasticsearch.log &
echo $! > logs/elasticsearch.pid

cd /Users/matheus/Git/chatbot-smartphones/rasa
 
rasa run actions > /Users/matheus/Git/chatbot-smartphones/logs/rasa-actions.log &
echo $! > /Users/matheus/Git/chatbot-smartphones/logs/rasa-actions.pid
rasa run > /Users/matheus/Git/chatbot-smartphones/logs/rasa-server.log &
echo $! > /Users/matheus/Git/chatbot-smartphones/logs/rasa-server.pid
