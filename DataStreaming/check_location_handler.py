import json

# check point
class Check_Location_Handler():

    # check polygon
    @staticmethod
    def point_inside_polygon(log, lat, poly):
        num = len(poly)
        j = num - 1
        c = False
        for i in range(num):
            if ((poly[i][1] > lat) != (poly[j][1] > lat)) and \
                    (log < poly[i][0] + (poly[j][0] - poly[i][0]) * (lat - poly[i][1]) /
                     (poly[j][1] - poly[i][1])):
                c = not c
            j = i
        return c

    # get polygon
    @staticmethod
    def append_attribute(log, lat):
        try:
            file_name = 'GeoJson.json'

            with open(file_name, 'r') as grid_file:
                json_data = json.load(grid_file)

                for block in json_data['features']:
                    if Check_Location_Handler.point_inside_polygon(log, lat, block['geometry']['coordinates'][0][0]):
                        return block['properties']

        except Exception as e:
            pass

        return None

