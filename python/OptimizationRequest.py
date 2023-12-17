import json
import os
from uuid import uuid4
from warnings import warn

from pydantic import BaseModel

from Utils import add_variable


class OptimizationRequestModel(BaseModel):
    optimization_request: dict


class OptimizationRequest:
    def __init__(self, data=None):
        self.idx = uuid4().int >> (128 - 24)
        while os.path.exists(f'../minizinc/data/{self.idx}.dzn'):
            self.idx = uuid4().int >> (128 - 24)
        self.scaling = None
        self.optimization_time = None
        self.lights_types = None

        self.time_units_in_minute = None
        self.time_unit_count = None
        self.light_count = None
        self.road_count = None
        self.connection_count = None
        self.collision_count = None

        self.road_capacities = None
        self.expected_car_flow = None
        self.connection_lights = None
        self.road_connections_in = None
        self.road_connections_out = None
        self.is_collision_important = None
        self.collision_connections = None
        self.is_connection_from_intermediate = None

        self.previous_results = None

        self.variables_type = {
            "time_units_in_minute": "int",
            "time_unit_count": "int",
            "light_count": "int",
            "road_count": "int",
            "connection_count": "int",
            "collision_count": "int",
            "road_capacities": "array",
            "expected_car_flow": "array",
            "connection_lights": "array2d",
            "road_connections_in": "array2d",
            "road_connections_out": "array2d",
            "is_collision_important": "array",
            "collision_connections": "array2d",
            "is_connection_from_intermediate": "array"
        }

        if data is None:
            self.fill_fields()
        else:
            print(data)
            self.fill_fields(
                time_units_in_minute=data['timeUnitsInMinute'],
                time_unit_count=data['timeUnitCount'],
                light_count=data['lightCount'],
                road_count=data['roadCount'],
                connection_count=data['connectionCount'],
                collision_count=data['collisionCount'],
                road_capacities=data['roadCapacities'],
                expected_car_flow=data['expectedCarFlow'],
                connection_lights=data['connectionLights'],
                road_connections_in=data['roadConnectionsIn'],
                road_connections_out=data['roadConnectionsOut'],
                is_collision_important=data['isCollisionImportant'],
                collision_connections=data['collisionConnections'],
                is_connection_from_intermediate=data['isConnectionFromIntermediate'],
                scaling=data['scaling'],
                optimization_time=data['optimizationTime'],
                lights_type=data['lightsTypes'],
                previous_results=data['previousResults']
            )

    def fill_fields(self, time_units_in_minute=0, time_unit_count=0, light_count=0, road_count=0,
                    connection_count=0, collision_count=0, road_capacities=None, expected_car_flow=None,
                    connection_lights=None, road_connections_in=None, road_connections_out=None,
                    is_collision_important=None, collision_connections=None, is_connection_from_intermediate=None,
                    scaling=0, optimization_time=0, lights_type=None, previous_results=None):
        self.time_units_in_minute = time_units_in_minute
        self.time_unit_count = time_unit_count
        self.light_count = light_count
        self.road_count = road_count
        self.connection_count = connection_count
        self.collision_count = collision_count

        self.road_capacities = road_capacities
        self.expected_car_flow = expected_car_flow
        self.connection_lights = connection_lights
        self.road_connections_in = road_connections_in
        self.road_connections_out = road_connections_out
        self.is_collision_important = is_collision_important
        self.collision_connections = collision_connections
        self.is_connection_from_intermediate = is_connection_from_intermediate

        self.scaling = scaling
        self.optimization_time = optimization_time
        self.lights_types = lights_type

        self.previous_results = previous_results

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def save_as_json(self):
        with open(f'../input_data/{self.idx}.json', 'w') as f:
            f.write(self.to_json())
        return self.idx

    def save_as_dzn(self, for_comparison: bool):
        as_json = self.to_dict()
        suffix = ""
        if for_comparison:
            if self.previous_results is None:
                return
            suffix = "_for_comparison"
        for key in self.variables_type.keys():
            if key in as_json:
                if key == "time_unit_count" and not for_comparison:
                    add_variable(f'../minizinc/data/{self.idx}{suffix}.dzn', key, int(as_json[key]) // self.scaling,
                                 self.variables_type[key])
                else:
                    add_variable(f'../minizinc/data/{self.idx}{suffix}.dzn', key, as_json[key],
                                 self.variables_type[key])
            else:
                warn(key + " is missing in OptimizationRequest")
        if for_comparison:
            add_variable(f'../minizinc/data/{self.idx}{suffix}.dzn', "previous_results", self.previous_results,
                         "array2d")
