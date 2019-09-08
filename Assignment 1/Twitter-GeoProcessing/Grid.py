import sys
import json


class Grid:
    def __init__(self):
        self.zone_range = {'min_x': sys.maxsize, 'max_x': -sys.maxsize, 'min_y': sys.maxsize, 'max_y': -sys.maxsize}
        self.matrix = {'x':[], 'y':[]}
        grid_file = "../melbGrid.json"
        if grid_file:
            with open(grid_file, 'r') as grid_file:
                grid = json.load(grid_file)
            self.zones = {}
            for zone in grid["features"]:
                self.zones[zone["properties"]["id"]] = {'x0': zone["properties"]["xmin"],
                                                        'x1': zone["properties"]["xmax"],
                                                        'y0': zone["properties"]["ymin"],
                                                        'y1': zone["properties"]["ymax"]}
                # self.matrix['x'].append(zone["properties"]["xmin"])
                # self.matrix['x'].append(zone["properties"]["xmin"])
                # self.matrix['x'].append(zone["properties"]["xmax"])
                # self.matrix['x'].append(zone["properties"]["xmax"])
                # self.matrix['y'].append(zone["properties"]["ymin"])
                # self.matrix['y'].append(zone["properties"]["ymax"])
                # self.matrix['y'].append(zone["properties"]["ymax"])
                # self.matrix['y'].append(zone["properties"]["ymin"])
                self.zone_range['min_x'] = min(self.zone_range['min_x'], zone["properties"]["xmin"])
                self.zone_range['max_x'] = max(self.zone_range['max_x'], zone["properties"]["xmax"])
                self.zone_range['min_y'] = min(self.zone_range['min_y'], zone["properties"]["ymin"])
                self.zone_range['max_y'] = max(self.zone_range['max_y'], zone["properties"]["ymax"])
                # print(zone["properties"]["id"], self.zones[zone["properties"]["id"]])

