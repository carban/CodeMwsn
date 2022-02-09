% Parameters
int: N; %3
int: Di; %20
float: time_slot_val;
float: battery;

set of int: s = 1..N;
set of int: t = 0..Di;
set of float: set_bat = 0..battery;

% array[s] of int: b = [80,100,95]; %100
array[s] of float: b;
% array[s] of float: c = [0.9778, 0.5107, 0.6215]; % Assuming a cost per time slot
% array[s] of int: c = [10, 5, 6];% Assuming a cost per time slot
array[s] of float: c;
% Variables
array[s] of var t: x;

% Constraints
constraint sum(x) >= 1 /\ sum(x) <= Di;
% constraint sum(x) == Di;
% constraint sum(x) <= Di;
constraint forall(i in s where max(b) = b[i] /\ min(c) = c[i])(max(x) = x[i]);
constraint forall(i in s where min(b) = b[i] /\ max(c) = c[i])(min(x) = x[i]); %%%%%%

array[s] of var set_bat: er;
constraint er = [b[i] - (c[i]*x[i]*time_slot_val) | i in s];

% Objective Function
% solve maximize min([b[i] - c[i]*x[i] | i in s]);
% solve maximize min(er);
solve minimize max(er);

output(["[",show(x),",", show(er),"]"]);

% output[
%     "X          = ", show(x), "\n",
%     "c          = ", show(c), "\n",
%     "Cost c*x   = ", show([c[i] * x[i] | i in s]), "\n",
%     "Old Energy = ", show(b), "\n",
%     "New Energy = ", show([b[i] - (c[i]*x[i])/Di | i in s]), "\n",
%     "% loss     = ", show(100-(sum(er)*100/sum(b)))
% ]
