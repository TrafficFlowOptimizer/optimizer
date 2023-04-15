% static data
int: time_units_in_minute;
int: number_of_time_units;
int: number_of_in_lights;
int: number_of_out_roads;

set of int: Conflicts_no;
set of int: In_light = 1..number_of_in_lights;
set of int: In_light_no_green_arrow;
set of int: In_light_green_arrow;
set of int: Out_road = 1..number_of_out_roads;
set of int: Time = 1..number_of_time_units;
set of float: Length_of_light_on = 0.0..number_of_time_units;

array[Out_road, In_light] of 0..infinity: roads_connections;
array[Conflicts_no, 1..2] of int: roads_conflicts;
array[In_light] of int: car_flow_per_min;


array[In_light, Time] of 0..1: light_states_without_green_arrows;

% variables
array[In_light, Time] of var 0..1: light_states;


constraint forall(C in Conflicts_no, T in Time)(light_states[roads_conflicts[C, 1]+1, T]+light_states[roads_conflicts[C, 2]+1, T]<2);


array[In_light, 1..number_of_time_units-1] of var -1..1: lights_change;
constraint forall(I in In_light, T in 1..number_of_time_units-1)(lights_change[I, T] = light_states[I, T]-light_states[I, T+1]);
constraint forall(I in In_light_green_arrow)(count(T in 1..number_of_time_units-1)(lights_change[I, T]!=0)<=2);


constraint forall(I in In_light_no_green_arrow, T in Time)(light_states[I, T] = light_states_without_green_arrows[I, T]);

var int: objective = sum([light_states[I, T] | T in Time, I in In_light_green_arrow]);

solve maximize objective;


output [show(T) ++ " " ++ join(" ", [show(light_states[I, T]) | I in In_light]) ++ "\n" | T in Time];