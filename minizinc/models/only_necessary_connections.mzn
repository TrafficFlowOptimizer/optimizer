% static data
int: time_units_in_minute;
int: number_of_time_units;
int: number_of_in_lights;
int: number_of_out_roads;
int: conflicts_no;

set of int: Conflicts_no = 1..conflicts_no;
set of int: In_light = 1..number_of_in_lights;
set of int: In_light_no_green_arrow;
set of int: In_light_green_arrow;
set of int: Out_road = 1..number_of_out_roads;
set of int: Time = 1..number_of_time_units;
set of float: Flow = 0.0..number_of_time_units;

array[Out_road, In_light] of 0..infinity: roads_connections;
array[Conflicts_no, 1..2] of int: roads_conflicts;
array[In_light] of int: car_flow_per_min;

% variables
var Flow: minimum_flow;
array[In_light, Time] of var 0..1: light_states;

% breaking symmetry
constraint light_states[2, 1] = 1;
constraint light_states[2, number_of_time_units] = 0;


% utility functions
array[In_light] of var 0..number_of_time_units: light_on;
constraint forall(I in In_light_no_green_arrow)(light_on[I] = sum(T in Time)(light_states[I, T]));
constraint forall(I in In_light_green_arrow)(light_on[I] = 0);

array[In_light] of var Flow: flow_normalized = [light_on[I]/car_flow_per_min[I]| I in In_light];

array[In_light, 1..number_of_time_units-1] of var -1..1: lights_change;
constraint forall(I in In_light, T in 1..number_of_time_units-1)(lights_change[I, T] = light_states[I, T]-light_states[I, T+1]);


% there are no colision on crossing with green light_states
constraint forall(C in Conflicts_no, T in Time)(light_states[roads_conflicts[C, 1], T]+light_states[roads_conflicts[C, 2], T]<2);
% there is only one period of light_states on (green arrow ignored)
constraint forall(I in In_light_no_green_arrow)(count(T in 1..number_of_time_units-1)(lights_change[I, T]!=0)<=2);

% looking for highest flow from lowest flows (green arrow ignored)
constraint forall(I in In_light_no_green_arrow)(flow_normalized[I]>=minimum_flow);

solve maximize minimum_flow;

output [show(T) ++ " " ++ join(" ", [show(light_states[I, T]) | I in In_light]) ++ "\n" | T in Time]
++ [join(" ", [show(flow_normalized[I])| I in In_light]) ++ "\n"]
++ [show(minimum_flow)]
;
