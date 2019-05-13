import couchdb
import json
from geojson_utils import point_in_polygon
from tqdm import tqdm
melbourne_polygon = []
polygons = {}
polygon_dict = {}
with open("sa2.geojson") as geoInfo:
    data = json.load(geoInfo)

for feature in data["features"]:
    data = {
        "name": feature["properties"]["sa2_name16"],
        "type": "Polygon",
        "coordinates": feature["geometry"]["coordinates"]
    }
    melbourne_polygon.append(data)


couch = couchdb.Server('http://admin:admin@172.26.38.59:5984')
db = couch['gluttony']
for info in tqdm(db.view("_design/test/_view/test")):
    detail = info["value"]
    if detail["result"]["related"]:
        point = {
            "type": "Point",
            "coordinates": detail["coordinates"]
        }
        for i in range(0, len(melbourne_polygon)):
            if point_in_polygon(point, melbourne_polygon[i]):
                if melbourne_polygon[i]["name"] not in polygons.keys():
                    polygons[melbourne_polygon[i]["name"]] = 1
                else:
                    polygons[melbourne_polygon[i]["name"]] += 1
                # print(polygons)
                break


file = "result.json"
fp = open(file, "w+")
fp.write(json.dumps(polygons))
fp.close




# for rev in db:
#     info = db[rev]["ogc_fid, y_coordinate, x_coordinate"]
#     info_list = info.split(",")
#     y = info_list[1]
#     x = info_list[2]
#     coordinates = [float(x[1:-1]), float(y[1:-1])]
#     point = {
#         "type": "Point",
#         "coordinates": coordinates
#     }
#     for i in range(0, len(melbourne_polygon)):
#         if point_in_polygon(point, melbourne_polygon[i]):
#             polygons.append(melbourne_polygon[i]["name"])
#             break
#
# counter = Counter(polygons)
# for key in counter:
#     tempo = {
#         key: counter[key]
#     }
#     polygon_dict.append(tempo)
