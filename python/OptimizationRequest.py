import json
from uuid import uuid4
import os


class OptimizationRequest:
    def __init__(self, data=None):
        self.lights_type = None
        self.number_of_time_units = None
        self.time_units_in_minute = None
        self.lights_count = None
        self.car_flow_per_minute = None
        self.connections_count = None
        self.roads_connections = None
        self.heavy_collisions_count = None
        self.heavy_collisions = None
        self.light_collisions_count = None
        self.light_collisions = None
        self.roads_count = None
        self.optimization_time = None
        if data is None:
            self.fill_fields()
        else:
            self.fill_fields(
                optimization_time=data['optimizationTime'],
                roads_count=data['roadsCount'],
                light_collisions=data['lightCollisions'],
                light_collisions_count=data['lightCollisionsCount'],
                heavy_collisions=data['heavyCollisions'],
                heavy_collisions_count=data['heavyCollisionsCount'],
                roads_connections=data['roadsConnections'],
                connections_count=data['connectionsCount'],
                car_flow_per_minute=data['carFlowPerMinute'],
                lights_count=data['lightsCount'],
                time_units_in_minute=data['timeUnitsInMinute'],
                number_of_time_units=data['numberOfTimeUnits'],
                lights_type=data['lightsType']
            )

    def fill_fields(self, optimization_time=0, roads_count=0, light_collisions=None,
                    light_collisions_count=0, heavy_collisions=None, heavy_collisions_count=0,
                    roads_connections=None, connections_count=0, car_flow_per_minute=None,
                    lights_count=0, time_units_in_minute=0, number_of_time_units=0, lights_type=None):
        if light_collisions is None:
            light_collisions = []
        if heavy_collisions is None:
            heavy_collisions = []
        if roads_connections is None:
            roads_connections = []
        if car_flow_per_minute is None:
            car_flow_per_minute = []
        if lights_type is None:
            lights_type = []

        self.optimization_time = optimization_time
        self.roads_count = roads_count
        self.light_collisions = light_collisions
        self.light_collisions_count = light_collisions_count
        self.heavy_collisions = heavy_collisions
        self.heavy_collisions_count = heavy_collisions_count
        self.roads_connections = roads_connections
        self.connections_count = connections_count
        self.car_flow_per_minute = car_flow_per_minute
        self.lights_count = lights_count
        self.time_units_in_minute = time_units_in_minute
        self.number_of_time_units = number_of_time_units
        self.lights_type = lights_type

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def save_to_json(self):
        idx = uuid4().int >> (128 - 24)
        while os.path.exists(f'../input_data/{idx}.json'):
            idx = uuid4().int >> (128 - 24)
        with open(f'../input_data/{idx}.json', 'w') as f:
            f.write(self.toJSON())
        return idx
