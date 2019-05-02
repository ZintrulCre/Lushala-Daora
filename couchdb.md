deploy couchdb <https://github.com/AURIN/comp90024/tree/master/couchdb>

1. (main instance) docker swarm init --advertise-addr 172.26.37.212
2. docker swarm join-token worker
3. copy command (docker swarm join --token XXXXXXXXXXXXXXXXXXXXX)
4. (other instances) docker swarm join --token XXXXXXXXXXXXXXXXXXXXX
5. (main instance) docker service create --replicas 3 -p 5984:5984 couchdb
6. docker service ls



7. create db
   - curl -X PUT http://172.26.37.212:5984/melbourne
8. 

