import json

melbourne_polygon = []
polygons = {}
polygon_dict = {}

with open("sa2.geojson") as geoInfo:
    data = json.load(geoInfo)

with open("result.json") as res:
    result = json.load(res)

for feature in data["features"]:
    feature["properties"]['value'] = result.get(feature["properties"]['name'])

file = "result.geojson"
fp = open(file, "w+")
fp.write(json.dumps(data))
fp.close

