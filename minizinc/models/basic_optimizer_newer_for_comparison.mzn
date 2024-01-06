%%%%% Input data
int: time_units_in_minute;
int: time_unit_count;

int: light_count;
int: road_count;
int: connection_count;
int: collision_count;

set of int: Time = 1..time_unit_count;
set of int: Timex2 = 1..time_unit_count*2;
set of int: Light_ = 0..light_count;
set of int: Light = 1..light_count;
set of int: Road = 1..road_count;
set of int: Connection_ = 0..connection_count;
set of int: Connection = 1..connection_count;
set of int: Collision = 1..collision_count;

array[Road] of 0..infinity: road_capacities;

array[Connection] of int: expected_car_flow;
array[Connection] of int: is_connection_from_intermediate;
array[Connection, 1..3] of Light_: connection_lights;

array[Collision] of 0..1: is_collision_important;
array[Collision, 1..2] of Connection: collision_connections;

array[Road, 1..3] of Connection_: road_connections_in;
array[Road, 1..3] of Connection_: road_connections_out;


array[Light, Time] of 0..1: previous_results;


%%%%% Variables

% whether the connection is passable
array[Connection, Time] of var 0..1: is_connection_on;
constraint forall(T in Time, C in Connection)(
        sum(L in [connection_lights[C, L] | L in 1..3 where connection_lights[C, L]>0])(previous_results[L, T])<2
        );
constraint forall(T in Time, C in Connection)(is_connection_on[C, T] = (
        sum(L in [connection_lights[C, L] | L in 1..3 where connection_lights[C, L]>0])(previous_results[L, T])
        ));

% how much connection is open for cars (what are the chances it will be chosen)

array[Connection, Time] of var 0..4: how_much_connection_on;
constraint forall(T in Time, C in Connection where is_connection_on[C, T]=1)(how_much_connection_on[C, T] = 
        4 - sum(L in [connection_lights[C, L] | L in 1..3])(if L>0 then previous_results[L, T] else 0 endif)
        );
        
constraint forall(T in Time, C in Connection where is_connection_on[C, T]=0)(how_much_connection_on[C, T] = 0);

% what is the summarized passable connection time
array[Connection] of var 0..time_unit_count*4: connection_on;
constraint forall(C in Connection)(connection_on[C] = sum(T in Time)(how_much_connection_on[C, T]));


%%%%% Objective function

% counters of connections flows
set of float: Flow = 0.0..time_unit_count*4;
array[Connection] of var Flow: flow_normalized_no_intermediate;
constraint forall(C in Connection where is_connection_from_intermediate[C]=0)(flow_normalized_no_intermediate[C] = connection_on[C]/expected_car_flow[C]);
constraint forall(C in Connection where is_connection_from_intermediate[C]=1)(flow_normalized_no_intermediate[C] = 0);

array[Connection] of var Flow: flow_normalized_intermediate;
constraint forall(C in Connection where is_connection_from_intermediate[C]=0)(flow_normalized_intermediate[C] = 0);
constraint forall(C in Connection where is_connection_from_intermediate[C]=1)(flow_normalized_intermediate[C] = connection_on[C]/expected_car_flow[C]);

var Flow: minimum_flow_no_intermediate = min(flow_normalized_no_intermediate);
var Flow: minimum_flow_intermediate = min(flow_normalized_intermediate);

var float: score = minimum_flow_no_intermediate+minimum_flow_intermediate;

solve maximize score;


%%%%% Print output

output ["{\"score\": " ++ show(score)] ++
        ["}"]