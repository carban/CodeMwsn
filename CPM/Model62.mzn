% Parameters
int: N = 3; %3
int: Di = 20; %20


set of int: s = 1..N;
set of int: t = 1..Di;

array[s] of int: b = [70, 100, 80]; %100
% array[s] of int: b = [100, 70, 80]; %100

% array[s] of float: b;
array[s] of float: c = [0.9778, 0.5107, 0.6215]; % Assuming a cost per time slot
% array[s] of int: c = [10, 5, 6];% Assuming a cost per time slot
% array[s] of float: c;
% Variables
array[s] of var t: x;
% var t: k;
% var t: l;

% Constraints
constraint sum(x) >= N /\ sum(x) <= Di;
% constraint sum(x) == Di;

% constraint forall(i in {0} where max(b) = b[i] /\ min(c) = c[i])(max(x) = x[i]);
% constraint forall(i in s where max(b) = b[i] /\ min(c) = c[i])(max(x) = x[i]);
% constraint forall(i in s where min(b) = b[i] /\ max(c) = c[i])(min(x) = x[i]);
var s: big;
var s: small;

constraint forall(i in s where max(b) = b[i] /\ min(c) = c[i])(big == i);
constraint forall(i in s where min(b) = b[i] /\ max(c) = c[i])(small == i);

constraint x[big] != x[small];
constraint x[big] == max(x);
constraint x[small] == min(x);

array[s] of var 0..100.0: er;
constraint er = [b[i] - (c[i]*x[i]) | i in s];

% Objective Function
% solve maximize min([b[i] - c[i]*x[i] | i in s]);
solve maximize min(er);

% output(["[",show(x),",", show(er),"]"]);

output[
    "X          = ", show(x), "\n",
    "c          = ", show(c), "\n",
    "Cost c*x   = ", show([c[i] * x[i] | i in s]), "\n",
    "Old Energy = ", show(b), "\n",
    "New Energy = ", show([b[i] - (c[i]*x[i])/Di | i in s]), "\n",
    "% loss     = ", show(100-(sum(er)*100/sum(b)))
]