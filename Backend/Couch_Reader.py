import couchdb
import json
from geojson_utils import point_in_polygon
from tqdm import tqdm

melbourne_polygon = []
false_polygons = {}
true_polygons = {}
polygon_dict = {}

with open("sa2.geojson") as geoInfo:
    data = json.load(geoInfo)

for feature in data["features"]:
    tempo = {
        "name": feature["properties"]["sa2_name16"],
        "type": "Polygon",
        "coordinates": feature["geometry"]["coordinates"]
    }
    melbourne_polygon.append(tempo)

couch = couchdb.Server('http://admin:admin@172.26.38.59:5984')

db = couch['gluttony']
for info in tqdm(db.view("_design/result_view/_view/new-view")):
    detail = info["value"]
    point = {
        "type": "Point",
        "coordinates": detail["coordinates"]
    }
    for i in range(0, len(melbourne_polygon)):
        if point_in_polygon(point, melbourne_polygon[i]):
            if detail["result"]["related"]:
                if melbourne_polygon[i]["name"] not in true_polygons.keys():
                    true_polygons[melbourne_polygon[i]["name"]] = 1
                else:
                    true_polygons[melbourne_polygon[i]["name"]] += 1
            else:
                if melbourne_polygon[i]["name"] not in false_polygons.keys():
                    false_polygons[melbourne_polygon[i]["name"]] = 1
                else:
                    false_polygons[melbourne_polygon[i]["name"]] += 1
            break


result = []
for feature in data["features"]:
    if feature["properties"]["sa2_name16"] in true_polygons:
        feature["properties"]["gluttony"] = true_polygons[feature["properties"]["sa2_name16"]]
    else:
        feature["properties"]["gluttony"] = 0
    if feature["properties"]["sa2_name16"] in false_polygons:
        feature["properties"]["not-gluttony"] = false_polygons[feature["properties"]["sa2_name16"]]
    else:
        feature["properties"]["not-gluttony"] = 0
    if (feature["properties"]["gluttony"] + feature["properties"]["not-gluttony"]) == 0:
        feature["properties"]["ratio"] = 0
    else:
        feature["properties"]["ratio"] = feature["properties"]["gluttony"]/\
                                         (feature["properties"]["gluttony"] + feature["properties"]["not-gluttony"])
    result.append(feature)

finalresult = {
    "type": "FeatureCollection",
    "features": result
}

file = "finalresult.geojson"
fp = open(file, "w+")
fp.write(json.dumps(finalresult))
fp.close


