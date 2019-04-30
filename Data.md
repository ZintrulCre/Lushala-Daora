1. selecte by location (each of the main capital cities) and time interval (down to the day)

root@server-1:/home/ubuntu# curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" -G --data-urlencode 'start_key=["perth",2014,1,1]' --data-urlencode 'end_key=["perth",2014,12,31]' --data-urlencode 'reduce=false' --data-urlencode 'include_docs=true' --user "readonly:ween7ighai9gahR6" -o /tmp/twitter.json



2. aggregate tweets by city, the "summary" view can be used

curl -XGET "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" -G --data-urlencode 'reduce=true' --data-urlencode 'include_docs=false' --data-urlencode 'group_level=1' --user "readonly:ween7ighai9gahR6" 



3. extracts GeoJSON limited to an area around Melbourne CBD ("r1r0" to "r1r1" geohash): 

curl -XGET "http://45.113.232.90/couchdbro/twitter/_design/twitter/_list/geojson/geoindex?reduce=false" -G --data-urlencode 'start_key=["r1r0",null,null,null]' --data-urlencode 'end_key=["r1r1",{},{},{}]' --user "readonly:ween7ighai9gahR6" 