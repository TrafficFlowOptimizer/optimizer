import json
import random


def update_json(json_path: str, name: str, value):
    with open(json_path, 'r+') as f:
        json_file = json.load(f)
        json_file.update({name: value})
        f.seek(0)
        json.dump(json_file, f, indent=0)


def init_data(data_path: str = "../input_data/data_kijowska.json"):
    update_json(data_path, "time_units_in_minute", 60)
    update_json(data_path, "number_of_time_units", 60)
    update_json(data_path, "number_of_lights", 12)
    update_json(data_path, "number_of_roads", 12)
    update_json(data_path, "number_of_connections", 12)


def lights_kijowska(data_path: str = "../input_data/data_kijowska.json"):
    lights = []
    for i in range(4):
        lights.append("heavy")
        lights.append("light")
        lights.append("light")
    update_json(data_path, "lights", lights)


def roads_connections_kijowska(data_path: str = "../input_data/data_kijowska.json"):
    f = open(data_path)
    data = json.load(f)
    number_of_lights = data["number_of_lights"]
    number_of_roads = data["number_of_roads"]
    number_of_connections = data["number_of_connections"]
    f.close()

    roads_connections = []
    for i in range(4):
        roads_connections.append([(i * 3 + 1 + 1) % number_of_roads,
                                  ((i * 3 + 1) + 8 + 1) % number_of_roads,
                                  (i * 3) + 1, -1])
        roads_connections.append([(i * 3 + 2 + 1) % number_of_roads,
                                  ((i * 3 + 1) + 4 + 1) % number_of_roads,
                                  (i * 3 + 1) + 1, -1])
        roads_connections.append([(i * 3 + 2 + 1) % number_of_roads,
                                  ((i * 3 + 1 + 1) + 1) % number_of_roads,
                                  (i * 3 + 1) + 1, (i * 3 + 2) + 1])

    lights_type = []
    for light in range(number_of_lights):
        if light % 3 == 0:
            lights_type.append(" < ")
        elif light % 3 == 1:
            lights_type.append(" O ")
        else:
            lights_type.append("-> ")

    update_json(data_path, "lights_type", lights_type)
    update_json(data_path, "roads_connections", roads_connections)


def roads_conflicts_kijowska(data_path: str = "../input_data/data_kijowska.json"):
    f = open(data_path)
    data = json.load(f)
    number_of_lights = data["number_of_lights"]
    number_of_roads = data["number_of_roads"]
    roads_connections = data["roads_connections"]
    lights = data["lights"]
    f.close()

    lights_heavy_conflicts = []
    lights_light_conflicts = []
    for light_1 in range(number_of_lights):
        for light_2 in range(light_1, number_of_lights):
            if light_1 % 3 == 0:
                if light_2 == (light_1 + 3) % number_of_lights or \
                        light_2 == (light_1 + 4) % number_of_lights or \
                        light_2 == (light_1 + 7) % number_of_lights or \
                        light_2 == (light_1 + 8) % number_of_lights or \
                        light_2 == (light_1 + 9) % number_of_lights or \
                        light_2 == (light_1 + 10) % number_of_lights:
                    if lights[light_1] == 'heavy' or lights[light_2] == 'heavy':
                        lights_heavy_conflicts.append([light_1 + 1, light_2 + 1])
                    else:
                        lights_light_conflicts.append([light_1 + 1, light_2 + 1])
            if light_1 % 3 == 1:
                if light_2 == (light_1 + 2) % number_of_lights or \
                        light_2 == (light_1 + 3) % number_of_lights or \
                        light_2 == (light_1 + 4) % number_of_lights or \
                        light_2 == (light_1 + 5) % number_of_lights or \
                        light_2 == (light_1 + 8) % number_of_lights or \
                        light_2 == (light_1 + 9) % number_of_lights:
                    if lights[light_1] == 'heavy' or lights[light_2] == 'heavy' or \
                            light_2 == (light_1 + 3) % number_of_lights or \
                            light_2 == (light_1 + 9) % number_of_lights:
                        lights_heavy_conflicts.append([light_1 + 1, light_2 + 1])
                    else:
                        lights_light_conflicts.append([light_1 + 1, light_2 + 1])
            if light_1 % 3 == 2:
                if light_2 == (light_1 + 4) % number_of_lights or \
                        light_2 == (light_1 + 8) % number_of_lights:
                    if lights[light_1] == 'heavy' or lights[light_2] == 'heavy':
                        lights_heavy_conflicts.append([light_1 + 1, light_2 + 1])
                    else:
                        lights_light_conflicts.append([light_1 + 1, light_2 + 1])

    update_json(data_path, "lights_heavy_conflicts", lights_heavy_conflicts)
    update_json(data_path, "heavy_conflicts_no", len(lights_heavy_conflicts))
    update_json(data_path, "lights_light_conflicts", lights_light_conflicts)
    update_json(data_path, "light_conflicts_no", len(lights_light_conflicts))


def car_flow_kijowska(data_path: str = "../input_data/data_kijowska.json"):
    f = open(data_path)
    data = json.load(f)
    number_of_connections = data["number_of_connections"]
    f.close()

    car_flow_per_min = []
    for in_light in range(number_of_connections):
        if in_light % 3 == 0:
            car_flow_per_min.append(random.randint(5, 10))
        elif in_light % 3 == 1:
            car_flow_per_min.append(random.randint(10, 15))
        else:
            car_flow_per_min.append(random.randint(15, 20))

    update_json(data_path, "car_flow_per_min", car_flow_per_min)


init_data()
roads_connections_kijowska()
lights_kijowska()
roads_conflicts_kijowska()
car_flow_kijowska()
