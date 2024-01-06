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


%%%%% Variables

% whether the light is on
array[Light, Time] of var 0..1: is_light_on;

% whether the connection is passable
array[Connection, Time] of var 0..1: is_connection_on;
constraint forall(T in Time, C in Connection)(
        sum(L in [connection_lights[C, L] | L in 1..3 where connection_lights[C, L]>0])(is_light_on[L, T])<2
        );
constraint forall(T in Time, C in Connection)(is_connection_on[C, T] = (
        sum(L in [connection_lights[C, L] | L in 1..3 where connection_lights[C, L]>0])(is_light_on[L, T])
        ));

% how much connection is open for cars (what are the chances it will be chosen)

array[Connection, Time] of var 0..4: how_much_connection_on;
constraint forall(T in Time, C in Connection where is_connection_on[C, T]=1)(how_much_connection_on[C, T] = 
        4 - sum(L in [connection_lights[C, L] | L in 1..3])(if L>0 then is_light_on[L, T] else 0 endif)
        );
        
constraint forall(T in Time, C in Connection where is_connection_on[C, T]=0)(how_much_connection_on[C, T] = 0);

% what is the summarized passable connection time
array[Connection] of var 0..time_unit_count*4: connection_on;
constraint forall(C in Connection)(connection_on[C] = sum(T in Time)(how_much_connection_on[C, T]));


% make sure there is only one light_on sequence per light
array[Light, Time] of var -1..1: lights_change;
constraint forall(L in Light, T in 1..time_unit_count-1)(lights_change[L, T] = is_light_on[L, T]-is_light_on[L, T+1]);
constraint forall(L in Light)(lights_change[L, time_unit_count] = is_light_on[L, time_unit_count]-is_light_on[L, 1]);
constraint forall(L in Light)(count(T in Time)(lights_change[L, T]!=0)<=2);

constraint forall(L in Light)
                    (is_light_on[L, time_unit_count] <= is_light_on[L, time_unit_count-1]+is_light_on[L, 1]);
constraint forall(L in Light)
                    (is_light_on[L, 1] <= is_light_on[L, time_unit_count]+is_light_on[L, 2]);
constraint forall(L in Light, T in 2..time_unit_count-1)
                    (is_light_on[L, T] <= is_light_on[L, T-1]+is_light_on[L, T+1]);

% whether intermediate has entrance/exit car in given moment of time
predicate has_entrance(var Road: R, var Time: T) = (road_connections_in[R, 1]!=0 /\ is_connection_on[road_connections_in[R, 1], T]==1) \/
                                                   (road_connections_in[R, 2]!=0 /\ is_connection_on[road_connections_in[R, 2], T]==1) \/
                                                   (road_connections_in[R, 3]!=0 /\ is_connection_on[road_connections_in[R, 3], T]==1);
predicate has_exit(var Road: R, var Time: T) = (road_connections_out[R, 1]!=0 /\ is_connection_on[road_connections_out[R, 1], T]==1) \/
                                               (road_connections_out[R, 2]!=0 /\ is_connection_on[road_connections_out[R, 2], T]==1) \/
                                               (road_connections_out[R, 3]!=0 /\ is_connection_on[road_connections_out[R, 3], T]==1);
                                               
% whether intermediate is filling up
array[Road, Time] of var -1..1: road_filling_state;
constraint forall(R in Road where road_capacities[R] == 0, T in Time)(road_filling_state[R, T]=0);
constraint forall(R in Road where road_capacities[R] > 0, T in Time)(road_filling_state[R, T]=has_entrance(R, T)-has_exit(R, T));
constraint forall(R in Road where road_capacities[R] > 0)(sum(T in Time)(road_filling_state[R, T])<=0);

array[Road, Timex2] of var -1..1: road_filling_state_extended;
constraint forall(R in Road where road_capacities[R] > 0, T in Time)
                  (road_filling_state_extended[R, T] = road_filling_state[R, T]);
constraint forall(R in Road where road_capacities[R] > 0, T in Time)
                  (road_filling_state_extended[R, T+time_unit_count] = road_filling_state[R, T]);
                  
% how many cars are currently waiting
array[Road, Time] of var 0..time_unit_count: waiting_cars_counter;
constraint forall(R in Road where road_capacities[R] > 0)
                    (waiting_cars_counter[R, 1] = road_filling_state[R, 1]);
constraint forall(R in Road where road_capacities[R] > 0, T in 2..time_unit_count)
                    (waiting_cars_counter[R, T] = waiting_cars_counter[R, T-1] + road_filling_state[R, T]);
constraint forall(R in Road where road_capacities[R] > 0)
                  (max([waiting_cars_counter[R, T] | T in Time])<=road_capacities[R]);

array[Road, Timex2] of var 0..time_unit_count*2: waiting_cars_counter_extended;
constraint forall(R in Road where road_capacities[R] > 0)
                  (waiting_cars_counter_extended[R, 1] = road_filling_state_extended[R, 1]);
constraint forall(R in Road where road_capacities[R] > 0, T in 2..time_unit_count*2)
                  (waiting_cars_counter_extended[R, T] = max(0, waiting_cars_counter_extended[R, T-1]+road_filling_state_extended[R, T]));
constraint forall(R in Road where road_capacities[R] > 0)
                  (max([waiting_cars_counter_extended[R, T] | T in Timex2])<=road_capacities[R]);


%%%%% Constraints

% make sure there are no colissions
constraint forall(C in Collision, T in Time)
          (is_connection_on[collision_connections[C, 1], T]+is_connection_on[collision_connections[C, 2], T]<2);

% breaking symmetry
constraint is_light_on[1, 1] = 1;
constraint is_light_on[1, time_unit_count] = 0;


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

output ["{\"is_light_on\": [\n"] ++
        [join(",\n", [ "[" ++ join(", ", [show(is_light_on[L, T]) | T in Time]) ++ "]"| L in Light])] ++ ["],"] ++
        ["\n\"is_connection_on\": [\n"] ++
        [join(",\n", [ "[" ++ join(", ", [show(is_connection_on[C, T]) | T in Time]) ++ "]"| C in Connection])] ++ ["],"] ++
        ["\n\"road_filling_state\": [\n"] ++
        [join(",\n", [ "[" ++ join(", ", [show(road_filling_state[R, T]) | T in Time]) ++ "]"| R in Road])] ++ ["],"] ++
        ["\n\"waiting_cars_counter\": [\n"] ++
        [join(",\n", [ "[" ++ join(", ", [show(waiting_cars_counter[R, T]) | T in Time]) ++ "]"| R in Road])] ++ ["],"] ++
        ["\n\"connection_on_time\": [\n"] ++
        [join(",\n", [ show(connection_on[C]) | C in Connection])] ++ ["]"] ++
        ["\n\"expected_car_flow\": [\n"] ++
        [join(",\n", [ show(expected_car_flow[C]) | C in Connection])] ++ ["]"] ++
        ["\n\"flow_normalized_no_intermediate\": [\n"] ++
        [join(",\n", [ show(flow_normalized_no_intermediate[C]) | C in Connection])] ++ ["]"] ++
        ["\n\"flow_normalized_intermediate\": [\n"] ++
        [join(",\n", [ show(flow_normalized_intermediate[C]) | C in Connection])] ++ ["]"] ++
        ["\n\"score\": " ++ show(score)] ++
        ["}"]