import shapefile
import codecs
import json as js
from json import dumps

# read the shapefile
def shp2geo(file="sa2.shp"):
    reader = shapefile.Reader(file)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        record = sr.record
        record = [r.decode('gb2312', 'ignore') if isinstance(r, bytes)
                  else r for r in record]
        atr = dict(zip(field_names, record))
        if 206000000 <= int(atr["sa2_main16"]) <= 214000000:
            del atr["0feature_c"]
            del atr["1feature_n"]
            with open("num.json") as num:
                aa = js.load(num)
                for fea in aa["features"]:
                    if fea["properties"]["sa2_main16"] == atr["sa2_main16"]:
                        atr["ave_wh"] = atr["p_tot_tot"]/fea["properties"]["p_total_total"]
                        atr["p_num"] = fea["properties"]["p_total_total"]
                        print(atr)
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", geometry=geom, properties=atr))
        # write the GeoJSON file

    geojson = codecs.open(file.split('.')[0] + ".geojson", "w", encoding="gb2312")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2))
    geojson.close()


if __name__ == '__main__':
    # import os
    # for z,x,c in os.walk('.'):
    #     for zz in c:
    #         if zz.endswith(".shp"):
    #             shp2geo(zz)

    # shp2geo(file='D.shp')
    shp2geo(file='sa2.shp')
