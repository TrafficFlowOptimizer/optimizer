import json
import os
from uuid import uuid4
from warnings import warn

from python.Utils import add_variable


class OptimizationRequest:
    def __init__(self, data=None):
        self.idx = uuid4().int >> (128 - 24)
        while os.path.exists(f'../minizinc/data/{self.idx}.dzn'):
            self.idx = uuid4().int >> (128 - 24)
        self.scaling = None

        self.lights_type = None
        self.number_of_time_units = None
        self.time_units_in_minute = None
        self.lights_count = None
        self.car_flow_per_minute = None
        self.connections_count = None
        self.roads_connections_lights = None
        self.heavy_collisions_count = None
        self.heavy_collisions = None
        self.light_collisions_count = None
        self.light_collisions = None
        self.roads_count = None
        self.optimization_time = None
        self.max_connections_from_one_entrance = None
        self.connections = None
        self.intermediates_capacities = None
        self.intermediates_count = None

        self.variables_type = {"time_units_in_minute": "int",
                               "number_of_time_units": "int",
                               "lights_count": "int",
                               "roads_count": "int",
                               "connections_count": "int",
                               "car_flow_per_minute": "array",
                               "roads_connections_lights": "array2d",
                               "heavy_collisions": "array2d",
                               "heavy_collisions_count": "int",
                               "light_collisions": "array2d",
                               "light_collisions_count": "int",
                               "max_connections_from_one_entrance": "int",
                               "connections": "array2d",
                               "intermediates_capacities": "array2d",
                               "intermediates_count": "int"}

        if data is None:
            self.fill_fields()
        else:
            print(data)
            self.fill_fields(
                optimization_time=data['optimizationTime'],
                roads_count=data['roadsCount'],
                light_collisions=data['lightCollisions'],
                light_collisions_count=data['lightCollisionsCount'],
                heavy_collisions=data['heavyCollisions'],
                heavy_collisions_count=data['heavyCollisionsCount'],
                roads_connections_lights=data['roadsConnectionsLights'],
                connections_count=data['connectionsCount'],
                car_flow_per_minute=data['carFlowPerMinute'],
                lights_count=data['lightsCount'],
                time_units_in_minute=data['timeUnitsInMinute'],
                number_of_time_units=data['numberOfTimeUnits'],
                lights_type=data['lightsType'],
                max_connections_from_one_entrance=data['maxConnectionsFromOneEntrance'],
                connections=data['connections'],
                intermediates_capacities=data['intermediatesCapacities'],
                intermediates_count=data['intermediatesCount'],
                scaling=data['scaling'])

    def fill_fields(self, optimization_time=0, roads_count=0, light_collisions=None,
                    light_collisions_count=0, heavy_collisions=None, heavy_collisions_count=0,
                    roads_connections_lights=None, connections_count=0, car_flow_per_minute=None,
                    lights_count=0, time_units_in_minute=0, number_of_time_units=0, lights_type=None,
                    max_connections_from_one_entrance=0, connections=None, intermediates_capacities=None,
                    intermediates_count=0, scaling=0):
        self.optimization_time = optimization_time
        self.roads_count = roads_count
        self.light_collisions = light_collisions
        self.light_collisions_count = light_collisions_count
        self.heavy_collisions = heavy_collisions
        self.heavy_collisions_count = heavy_collisions_count
        self.roads_connections_lights = roads_connections_lights
        self.connections_count = connections_count
        self.car_flow_per_minute = car_flow_per_minute
        self.lights_count = lights_count
        self.time_units_in_minute = time_units_in_minute
        self.number_of_time_units = number_of_time_units
        self.lights_type = lights_type
        self.max_connections_from_one_entrance = max_connections_from_one_entrance
        self.connections = connections
        self.intermediates_capacities = intermediates_capacities
        self.intermediates_count = intermediates_count
        self.scaling = scaling

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def save_as_json(self):
        with open(f'../input_data/{self.idx}.json', 'w') as f:
            f.write(self.to_json())
        return self.idx

    def save_as_dzn(self):
        as_json = self.to_dict()
        for key in self.variables_type.keys():
            if key in as_json:
                if key == "number_of_time_units":
                    add_variable(f'../minizinc/data/{self.idx}.dzn', key, int(as_json[key]) // self.scaling,
                                 self.variables_type[key])
                else:
                    add_variable(f'../minizinc/data/{self.idx}.dzn', key, as_json[key], self.variables_type[key])
            else:
                warn(key + " is missing in OptimizationRequest")
