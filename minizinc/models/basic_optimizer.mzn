% static data
int: time_units_in_minute;
int: number_of_time_units;
int: number_of_lights;
int: number_of_roads;
int: number_of_connections;
int: heavy_collisions_no;
int: light_collisions_no;

set of int: Light = 1..number_of_lights;
set of int: Connection = 1..number_of_connections;
set of int: Heavy_collisions_no = 1..heavy_collisions_no;
set of int: Light_collisions_no = 1..light_collisions_no;

set of int: Time = 1..number_of_time_units;
set of float: Flow = 0.0..number_of_time_units;

array[Connection, 1..4] of -1..infinity: roads_connections;
array[Heavy_collisions_no, 1..2] of Light: lights_heavy_collisions;
array[Light_collisions_no, 1..2] of Light: lights_light_collisions;
array[Connection] of int: car_flow_per_min;

% variables
var Flow: minimum_flow;
var Flow: maximum_flow;
array[Light, Time] of var 0..1: light_states;

% breaking symmetry
constraint light_states[1, 1] = 1;
constraint light_states[1, number_of_time_units] = 0;


% utility functions
array[Connection] of var 0..number_of_time_units: light_on;
constraint forall(C in Connection)(light_on[C] = sum(T in Time)(if roads_connections[C, 4]= -1 
                    then light_states[roads_connections[C, 3], T]
                    else max(light_states[roads_connections[C, 3], T], light_states[roads_connections[C, 4], T]) endif));



array[Connection] of var Flow: flow_normalized = [light_on[C]/car_flow_per_min[C] | C in Connection];

array[Light, 1..number_of_time_units-1] of var -1..1: lights_change;
constraint forall(L in Light, T in 1..number_of_time_units-1)(lights_change[L, T] = light_states[L, T]-light_states[L, T+1]);

constraint forall(C in Connection where roads_connections[C, 4]!=-1, T in Time)
                              (light_states[roads_connections[C, 3], T] + light_states[roads_connections[C, 4], T]<2);
% there are no colision on crossing with green light_states
constraint forall(C in Heavy_collisions_no, T in Time)(light_states[lights_heavy_collisions[C, 1], T]+light_states[lights_heavy_collisions[C, 2], T]<2);
% there is only one period of light_states on (green arrow ignored)
constraint forall(L in Light)(count(T in 1..number_of_time_units-1)(lights_change[L, T]!=0)<=2);

% looking for highest flow from lowest flows (green arrow ignored)
constraint forall(L in Light)(flow_normalized[L]>=minimum_flow);
constraint forall(L in Light)(flow_normalized[L]<=maximum_flow);

constraint maximum_flow-minimum_flow>=0;
constraint maximum_flow-minimum_flow<=0.5;

solve maximize minimum_flow;
% solve maximize maximum_flow*minimum_flow;

output ["{\"results\": ["] ++
        [join(", ", [ "[" ++ join(", ", [show(light_states[L, T]) | T in Time]) ++ "]" | L in Light])] ++ ["]}"]

% output 
% ["{\"results\": ["] ++
%   ["{\"lightId\": " ++ show(lights_IDs[L]) ++ 
%   ",\n\"sequence\": [" ++ join(", ", [show(light_states[L, T]) | T in Time]) 
%   ++ "],\n\"flow\": " ++ show(flow_normalized[L]) ++ "}" ++ if L<number_of_lights then "," else "" endif ++ "\n" | L in Light] ++ ["],\n"] ++
% ["\"minimum_flow\": " ++ show(minimum_flow) ++ "}"]
% ;
