% static data
int: time_units_in_minute;
int: number_of_time_units;
int: lights_count;
int: roads_count;
int: connections_count;
int: heavy_collisions_count;
int: light_collisions_count;
int: max_connections_from_one_entrance;

set of int: Light = 1..lights_count;
set of int: Connection = 1..connections_count;
set of int: Road = 1..roads_count;
set of int: Heavy_collisions_no = 1..heavy_collisions_count;
set of int: Light_collisions_no = 1..light_collisions_count;

set of int: Time = 1..number_of_time_units;
set of float: Flow = 0.0..number_of_time_units;

array[Connection, 1..4] of -1..infinity: roads_connections;
array[Road, 1..max_connections_from_one_entrance] of -1..connections_count: connections;
array[Heavy_collisions_no, 1..2] of Light: heavy_collisions;
array[Light_collisions_no, 1..2] of Light: light_collisions;
array[Connection] of int: car_flow_per_minute;

% variables
var Flow: minimum_flow;
var Flow: maximum_flow;
array[Light, Time] of var 0..1: light_states;
array[Connection, Time] of var 0..1: connection_state;

% breaking symmetry
constraint light_states[1, 1] = 1;
constraint light_states[1, number_of_time_units] = 0;


% utility functions
%array[Connection] of var 0..number_of_time_units: light_on;
%constraint forall(C in Connection)(light_on[C] = sum(T in Time)(if roads_connections[C, 4]= -1
%                    then light_states[roads_connections[C, 3], T]
%                    else light_states[roads_connections[C, 3], T] + light_states[roads_connections[C, 4], T] endif));

array[Connection] of var 0..number_of_time_units: connection_on;
constraint forall(C in Connection)(connection_on[C] = sum(T in Time)(if roads_connections[C, 4]= -1
                    then light_states[roads_connections[C, 3], T]
                    else light_states[roads_connections[C, 3], T] + light_states[roads_connections[C, 4], T] endif));
constraint forall(T in Time, R in Road)(
                    sum(C in 1..max_connections_from_one_entrance where connections[R, C] > 0)(connection_state[C, T])<=1);


array[Connection] of var Flow: flow_normalized = [connection_on[C]/car_flow_per_minute[C] | C in Connection];

array[Light, 1..number_of_time_units-1] of var -1..1: lights_change;
constraint forall(L in Light, T in 1..number_of_time_units-1)(lights_change[L, T] = light_states[L, T]-light_states[L, T+1]);

constraint forall(C in Connection where roads_connections[C, 4]!=-1, T in Time)
                              (light_states[roads_connections[C, 3], T] + light_states[roads_connections[C, 4], T]<2);

% there are no collision on crossing with green light_states
constraint forall(C in Heavy_collisions_no, T in Time)(light_states[heavy_collisions[C, 1], T]+light_states[heavy_collisions[C, 2], T]<2);
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
%   ++ "],\n\"flow\": " ++ show(flow_normalized[L]) ++ "}" ++ if L<lights_count then "," else "" endif ++ "\n" | L in Light] ++ ["],\n"] ++
% ["\"minimum_flow\": " ++ show(minimum_flow) ++ "}"]
% ;
