start_matpower;
mpc = loadcase('envcase');
PV = PV / 1;
opt = mpoption('ENFORCE_Q_LIMS',1,'PF_ALG',1,'VERBOSE',0,'OUT_ALL',0);
Vref_29 = [];
N=20;
Vref_29 = ones(1,N);

dQ = [];
dV = [];
dQ_list = [];
dQpv_list = [];

PVnode = [46, 53, 66, 59, 62, 42] - 40;
PVnum = 6;
arsave = 0;
vrsave = 0;
dQsum = zeros(1,7);
dQpvsum = zeros(1, 6);
dQsum2 = 0;
cscv = 0;
useful_nodes = [2 3 4 5 6 7 8 9 11 13 14 15 16 17 18 19 20 22 23 24 25 26 27 28 29 30 31 32];
%get the load
% Pdload = [];
% Pdload = [P_load10 P_load3 P_load15 P_load28];
m = (max(Pdload));
Pdload(:,1) = Pdload(:,1) / m(1);
Pdload(:,2) = Pdload(:,2) / m(2);
Pdload(:,3) = Pdload(:,3) / m(3);
Pdload(:,4) = Pdload(:,4) / m(4);

load_node = [3 4 5 7 8 9 11 14 15 16 17 18 20 23 24 25 27 28 29 30 31 32];
Pd = Pdload(:,[1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2]);
save_node = [];
pori = mpc.bus(load_node',3)';
qori = mpc.bus(load_node',4)';
pori = repmat(pori, 24480, 1);
qori = repmat(qori, 24480, 1);
Pd1 = Pd.*pori;
Qd1 = Pd.*qori;

dQsave = [];
