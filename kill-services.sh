cd /Users/matheus/Git/chatbot-smartphones/logs

elasticsearch_pid=`cat elasticsearch.pid`
rasa_server_pid=`cat rasa-server.pid`
rasa_actions_pid=`cat rasa-actions.pid`

kill $rasa_actions_pid $rasa_server_pid $elasticsearch_pid
rm -rf rasa-server.pid rasa-actions.pid elasticsearch.pid