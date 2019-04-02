%% plot figure
close all
fig = figure(1)
plot(sum(QOPV(:,load_node),2))
hold on
plot(sum(POPV(:,load_node),2))
hold on
plot(sum(QOPV(:,PVnode),2))
hold on
plot(sum(POPV(:,PVnode),2))
saveas(fig, 'pic/afigure.png')
close(fig)
fig = figure(2)
plot(VOPV(:,13))
saveas(fig, 'pic/afigure2.png')

fig = figure(3)
% plot(Ploss(:,2))
% hold on
plot(Ploss(:,8))
hold on
plot(Ploss(:,7))
hold on
% plot(Ploss(:,5))
legend('2','3')
saveas(fig, 'pic/afigure3.png')
sum(Ploss)

fig = figure(4)
plot(1:1440, sclist(1:1440,1), 1:1440, sclist(1:1440,2),1:1440, sclist(1:1440,3))
saveas(fig, 'pic/afigure4.png')

scsum = [0 0 0];
for i = 2:1440
  scsum = scsum + (sclist(i,:) ~= sclist(i-1,:));
  if sum(sclist(i,:) ~= sclist(i-1,:))>0
    i
    % sclist(i,:)
    % sclist(i-1,:)
    % sclist(i,:) ~= sclist(i-1,:)
  end
end
scsum

%
%
% sum(sum(abs(dQsave)>0))
% dQsum = cumsum(dQsave,1);
% fig = figure(1)
% for i = 1:2
%   plot(dQsum(:,i))
%   hold on
% end
% saveas(fig, 'afigure2.png')
% close(fig)

% fig = figure()
% plot(Pd1(1:10000, 1))
% hold on
% plot(Qd1(1:10000, 1))
% saveas(fig, 'afigure.png')
% close(fig)


% close all
% fig = figure(2)
% plot(allrsave(:,1))
% hold on
% plot(allrsave(:,2))
% hold on
% plot(allrsave(:,3))
% ylim([-3000 0])
% saveas(fig, 'pic/reward0.4.png')

% fig = figure(1)
% subplot(3,1,1)
% plot(V1(7,:))
% hold on
% plot(V0(7,:))
% ylabel('14节点电压')
% legend('优化后','优化前')
% subplot(3,1,2)
% plot(V1(13,:))
% hold on
% plot(V0(13,:))
% ylabel('20节点电压')
% subplot(3,1,3)
% plot(V1(22,:))
% hold on
% plot(V0(22,:))
% ylabel('27节点电压')
% saveas(fig, 'afigure.png')
% close(fig)

% meanstate = zeros(length(useful_nodes),3);
% meanstate(:,1) = mean(POPV(:,useful_nodes));
% meanstate(:,2) = mean(QOPV(:,useful_nodes));
% meanstate(:,3) = mean(VOPV(:,useful_nodes));
% stdstate(:,1) = std(POPV(:,useful_nodes));
% stdstate(:,2) = std(QOPV(:,useful_nodes));
% stdstate(:,3) = std(VOPV(:,useful_nodes));
j = 1;
for sc = 0:0.1:1.5
  mpc.bus(17, 4) = Qd1(1, 17) * 1.7 - sc;
  result = runpf(mpc, opt);
  loss(j) = sum(result.branch(:,14) + result.branch(:,16));
  j = j + 1;
end
