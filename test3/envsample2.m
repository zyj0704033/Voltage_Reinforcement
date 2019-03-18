% add control to chaoliu cal
start_matpower;
isSample = 1

%setup V_ref
mpc = loadcase('envcase');
load('PV.mat');
load('Vbase.mat');
load('Pdload.mat');
PV = PV / 1;
opt = mpoption('ENFORCE_Q_LIMS',1,'PF_ALG',1,'VERBOSE',0,'OUT_ALL',0);
Vref_29 = [];
N=2880;
Vref_29 = ones(1,N);

dQ = [];
dV = [];
dQ_list = [];
dQpv_list = [];

PVnode = [53, 46, 66, 59, 62, 42] - 40;
PVnum = 6;

dQsum = zeros(1,7);
dQpvsum = zeros(1, 6);
dQsum2 = 0;
cscv = 0;
%get the load
% Pdload = [];
% Pdload = [P_load10 P_load3 P_load15 P_load28];
m = (max(Pdload));
Pdload(:,1) = Pdload(:,1) / m(1);
Pdload(:,2) = Pdload(:,2) / m(2);
Pdload(:,3) = Pdload(:,3) / m(3);
Pdload(:,4) = Pdload(:,4) / m(4);
useful_nodes = [2 3 4 5 6 7 8 9 11 13 14 15 16 17 18 19 20 22 23 24 25 26 27 28 29 30 31 32];
load_node = [3 4 5 7 8 9 11 14 15 16 17 18 20 23 24 25 27 28 29 30 31 32];
Pd = Pdload(:,[1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4 1 2]);
pori = mpc.bus(load_node',3)';
qori = mpc.bus(load_node',4)';
pori = repmat(pori, 24480, 1);
qori = repmat(qori, 24480, 1);
Pd1 = Pd.*pori;
Qd1 = Pd.*qori;
% Qd1 = Qd1./pori;

dQsave = [];
arsave = 0;
vrsave = 0;
allr = 0;
allrsave = [];

for i=1:N
%     dQpvsum
    mpc.gen(1, 6) = Vbase(29, i);
    mpc.bus(PVnode , 3) = - PV(i, [1,2,3,1,2,3])/10';
    mpc.bus(load_node, 3) = Pd1(i,:)';
    mpc.bus(load_node, 4) = Qd1(i,:)';


    result = runpf(mpc,opt);
    %cal c
    if cscv == 0
        if i == 1
            for k = 1:PVnum
                pvn = PVnode(k);
                mpc2 = mpc;
                mpc2.bus(pvn, 4) = mpc.bus(pvn, 4) + 0.1;
                result2 = runpf(mpc2, opt);
                cpvq(k) = -(result2.bus(pvn,8) - result.bus(pvn,8))/0.1;
                for m = 1:PVnum
                    cpvm(k,m) = -(result2.bus(PVnode(m),8) - result.bus(PVnode(m), 8)) / 0.1;
                end
                mpc2 = mpc;
                mpc2.bus(pvn, 3) = mpc.bus(pvn, 3) + 0.1;
                result2 = runpf(mpc2, opt);
                cpvp(k) = -(result2.bus(pvn,8) -result.bus(pvn,8))/0.1;

            end
        end

%下垂控制
% add for action isSample
        if isSample == 1
          action_flag = binornd(1, 0.3, 1, PVnum);
        else
          action_flag = ones(1, PVnum);
        end
        final_action = zeros(1,6);
        if rem(i,1)==0 %control for the distribute network
            for k = 1:PVnum
                pvn = PVnode(k);
                dV = (1 - result.bus(pvn, 8));

                if (abs(dV)<0.01) | (action_flag(k)==0)
                    dQ = 0;
                else
                    if dV > 0.01
                        final_action(k) = 1;
                        %dQ = (dV-0.01) * -5 / 0.05;
                        dQ = -0.1;
                    else
                        final_action(k) = 1;
                        %dQ = (dV+0.01) * -5 / 0.05;
                        dQ = 0.1;
                    end
                end
                dQsave(i, k) = dQ;
                mpc.bus(pvn, 4) = mpc.bus(pvn, 4) + dQ;
                %result = runpf(mpc, opt);
            end
            % result = runpf(mpc, opt);
        end
    end
    V1(:,i) = result.bus(:,8);
    QOPV(i,:) = result.bus(:,4)';
    POPV(i,:) = result.bus(:,3)';
    VOPV(i,:) = result.bus(:,8)';
    PQV = result.bus(useful_nodes,[3 4 8]);
    [ar,vr] = cal_return(final_action, PQV);
    arsave = arsave + ar;
    vrsave = vrsave + vr;
    allr = 0.6 * arsave + vrsave
    allrsave(i,1) = arsave;
    allrsave(i,2) = vrsave;
    allrsave(i,3) = allr;
    i
end
