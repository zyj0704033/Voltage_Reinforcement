
final_action = zeros(1,6);
mpc.gen(1, 6) = Vbase(29, i);
mpc.bus(PVnode , 3) = - PV(i, [1,2,3,1,2,3])/10';
mpc.bus(load_node, 3) = Pd1(i,:)';
mpc.bus(load_node, 4) = Qd1(i,:)';


result = runpf(mpc,opt);
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
action_flag = cell2mat(action_flag);
%下垂控制
if rem(i,1)==0 %control for the distribute network
    for k = 1:PVnum
        pvn = PVnode(k);
        dV = (1 - result.bus(pvn, 8));
        if (abs(dV)<0.01) | (action_flag(k) == 0)
            dQ = 0;
        else
            final_action(k) = 1;
            if dV > 0.01
                %dQ = (dV-0.01) * -5 / 0.05;
                dQ = -0.05;

            else
                %dQ = (dV+0.01) * -5 / 0.05;
                dQ = 0.05;
            end
        end
        dQsave(i, k) = dQ;
        mpc.bus(pvn, 4) = mpc.bus(pvn, 4) + dQ;
    end
%    result = runpf(mpc, opt);
end
