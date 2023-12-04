import json
import random


def update_json(json_path: str, name: str, value):
    with open(json_path, 'r+') as f:
        json_file = json.load(f)
        json_file.update({name: value})
        f.seek(0)
        json.dump(json_file, f, indent=2)


def init_data(data_path: str = "../data_kijowska.json"):
    update_json(data_path, "time_units_in_minute", 60)
    update_json(data_path, "number_of_time_units", 60)
    update_json(data_path, "lights_count", 12)
    update_json(data_path, "roads_count", 12)
    update_json(data_path, "connections_count", 12)


def lights_kijowska(data_path: str = "../data_kijowska.json"):
    lights = []
    for i in range(4):
        lights.append("heavy")
        lights.append("light")
        lights.append("light")
    update_json(data_path, "lights", lights)


def roads_connections_lights_kijowska(data_path: str = "../data_kijowska.json"):
    f = open(data_path)
    data = json.load(f)
    lights_count = data["lights_count"]
    roads_count = data["roads_count"]
    connections_count = data["connections_count"]
    f.close()

    roads_connections_lights = []
    for i in range(4):
        roads_connections_lights.append([(i * 3 + 1 + 1) % roads_count,
                                  ((i * 3 + 1) + 8 + 1) % roads_count,
                                  (i * 3) + 1, -1])
        roads_connections_lights.append([(i * 3 + 2 + 1) % roads_count,
                                  ((i * 3 + 1) + 4 + 1) % roads_count,
                                  (i * 3 + 1) + 1, -1])
        roads_connections_lights.append([(i * 3 + 2 + 1) % roads_count,
                                  ((i * 3 + 1 + 1) + 1) % roads_count,
                                  (i * 3 + 1) + 1, (i * 3 + 2) + 1])

    lights_type = []
    for light in range(lights_count):
        if light % 3 == 0:
            lights_type.append(" < ")
        elif light % 3 == 1:
            lights_type.append(" O ")
        else:
            lights_type.append("-> ")

    update_json(data_path, "lights_types", lights_type)
    update_json(data_path, "roads_connections_lights", roads_connections_lights)


def roads_collisions_kijowska(data_path: str = "../data_kijowska.json"):
    f = open(data_path)
    data = json.load(f)
    lights_count = data["lights_count"]
    roads_count = data["roads_count"]
    roads_connections_lights = data["roads_connections_lights"]
    lights = data["lights"]
    f.close()

    heavy_collisions = []
    light_collisions = []
    for light_1 in range(lights_count):
        for light_2 in range(light_1, lights_count):
            if light_1 % 3 == 0:
                if light_2 == (light_1 + 3) % lights_count or \
                        light_2 == (light_1 + 4) % lights_count or \
                        light_2 == (light_1 + 7) % lights_count or \
                        light_2 == (light_1 + 8) % lights_count or \
                        light_2 == (light_1 + 9) % lights_count or \
                        light_2 == (light_1 + 10) % lights_count:
                    if lights[light_1] == 'heavy' or lights[light_2] == 'heavy':
                        heavy_collisions.append([light_1 + 1, light_2 + 1])
                    else:
                        light_collisions.append([light_1 + 1, light_2 + 1])
            if light_1 % 3 == 1:
                if light_2 == (light_1 + 2) % lights_count or \
                        light_2 == (light_1 + 3) % lights_count or \
                        light_2 == (light_1 + 4) % lights_count or \
                        light_2 == (light_1 + 5) % lights_count or \
                        light_2 == (light_1 + 8) % lights_count or \
                        light_2 == (light_1 + 9) % lights_count:
                    if lights[light_1] == 'heavy' or lights[light_2] == 'heavy' or \
                            light_2 == (light_1 + 3) % lights_count or \
                            light_2 == (light_1 + 9) % lights_count:
                        heavy_collisions.append([light_1 + 1, light_2 + 1])
                    else:
                        light_collisions.append([light_1 + 1, light_2 + 1])
            if light_1 % 3 == 2:
                if light_2 == (light_1 + 4) % lights_count or \
                        light_2 == (light_1 + 8) % lights_count:
                    if lights[light_1] == 'heavy' or lights[light_2] == 'heavy':
                        heavy_collisions.append([light_1 + 1, light_2 + 1])
                    else:
                        light_collisions.append([light_1 + 1, light_2 + 1])

    update_json(data_path, "heavy_collisions", heavy_collisions)
    update_json(data_path, "heavy_collisions_count", len(heavy_collisions))
    update_json(data_path, "light_collisions", light_collisions)
    update_json(data_path, "light_collisions_count", len(light_collisions))


def car_flow_kijowska(data_path: str = "../data_kijowska.json"):
    f = open(data_path)
    data = json.load(f)
    connections_count = data["connections_count"]
    f.close()

    car_flow_per_minute = []
    for in_light in range(connections_count):
        if in_light % 3 == 0:
            car_flow_per_minute.append(random.randint(5, 10))
        elif in_light % 3 == 1:
            car_flow_per_minute.append(random.randint(10, 15))
        else:
            car_flow_per_minute.append(random.randint(15, 20))

    update_json(data_path, "car_flow_per_minute", car_flow_per_minute)


init_data()
roads_connections_lights_kijowska()
lights_kijowska()
roads_collisions_kijowska()
car_flow_kijowska()
