# Coordinate node 172.26.38.27
sudo groupadd docker
sudo gpasswd -a ubuntu docker
newgrp - docker

docker run -d --network host --name couchdb-1 couchdb

docker exec couchdb-1 bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb-1 bash -c "echo \"-name couchdb@172.26.38.27\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb-1 cat /opt/couchdb/etc/vm.args

docker restart couchdb-1
sleep 3

curl -X PUT http://127.0.0.1:5984/_node/_local/_config/admins/admin -d '"admin"'
curl -X PUT http://admin:admin@127.0.0.1:5984/_node/_local/_config/chttpd/bind_address -d '"0.0.0.0"'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'

#-----------------

curl -X POST -H "Content-Type: application/json" http://admin:admin@172.26.38.27:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "port": 5984, "node_count": "2", "remote_node": "172.26.38.6", "remote_current_user": "admin", "remote_current_password": "admin" }'
curl -X POST -H "Content-Type: application/json" http://admin:admin@172.26.38.27:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "port": 5984, "node_count": "2", "remote_node": "172.26.38.59", "remote_current_user": "admin", "remote_current_password": "admin" }'

curl -X POST -H "Content-Type: application/json" http://admin:admin@172.26.38.27:5984/_cluster_setup -d '{"action": "add_node", "host":"172.26.38.6", "port": 5984, "username": "admin", "password":"admin"}'
curl -X POST -H "Content-Type: application/json" http://admin:admin@172.26.38.27:5984/_cluster_setup -d '{"action": "add_node", "host":"172.26.38.59", "port": 5984, "username": "admin", "password":"admin"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@172.26.38.27:5984/_cluster_setup -d '{"action": "finish_cluster"}'
#Delete nonode@nohost
rev=`curl -XGET "http://172.26.38.27:5986/_nodes/nonode@nohost" --user "admin:admin" | sed -e 's/[{}"]//g' | cut -f3 -d:`
curl -X DELETE "http://172.26.38.27:5986/_nodes/nonode@nohost?rev=${rev}"  --user "admin:admin"

curl http://admin:admin@172.26.38.27:5984/_membership

#==============================================================================================#

# Node 172.26.38.6
sudo groupadd docker
sudo gpasswd -a ubuntu docker
newgrp - docker

docker run -d --network host --name couchdb-2 couchdb

docker exec couchdb-2 bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb-2 bash -c "echo \"-name couchdb@172.26.38.6\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb-2 cat /opt/couchdb/etc/vm.args
docker restart couchdb-2
sleep 3

curl -X PUT http://127.0.0.1:5984/_node/_local/_config/admins/admin -d '"admin"'
curl -X PUT http://admin:admin@127.0.0.1:5984/_node/_local/_config/chttpd/bind_address -d '"0.0.0.0"'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'

#==============================================================================================#

# Node 172.26.38.59
sudo groupadd docker
sudo gpasswd -a ubuntu docker
newgrp - docker

docker run -d --network host --name couchdb-3 couchdb

docker exec couchdb-3 bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb-3 bash -c "echo \"-name couchdb@172.26.38.59\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb-3 cat /opt/couchdb/etc/vm.args
docker restart couchdb-3
sleep 3

curl -X PUT http://127.0.0.1:5984/_node/_local/_config/admins/admin -d '"admin"'
curl -X PUT http://admin:admin@127.0.0.1:5984/_node/_local/_config/chttpd/bind_address -d '"0.0.0.0"'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'
