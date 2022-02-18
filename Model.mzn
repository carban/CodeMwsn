% Parameters
int: N;
int: Di;
float: time_slot_val;
float: battery;
int: cv;

set of int: s = 1..N;
set of int: t = 0..Di;
set of float: set_bat = 0..battery;

array[s] of float: b;
array[s] of float: c;

% Variables
array[s] of var t: x;
array[s] of var set_bat: ReEn;

% Constraints

% Option 1
% constraint sum(x) >= N /\ sum(x) <= Di;
% Option 2
% constraint sum(x) >= 1 /\ sum(x) <= Di;

constraint sum(x) >= cv /\ sum(x) <= Di;

constraint forall(i in s where max(b) = b[i] /\ min(c) = c[i])(max(x) = x[i]);
constraint forall(i in s where min(b) = b[i] /\ max(c) = c[i])(min(x) = x[i]);

constraint ReEn = [b[i] - (c[i]*x[i]*time_slot_val) | i in s];

% Objective Function

solve minimize max(ReEn);

output(["[",show(x),",", show(ReEn),"]"]);