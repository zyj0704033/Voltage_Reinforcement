%% plot figure

% fig = figure(1)
% plot(sum(QOPV(:,load_node),2))
% saveas(fig, 'afigure.png')
% close(fig)
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

fig = figure(1)
subplot(3,1,1)
plot(V1(7,:))
hold on
plot(V0(7,:))
ylabel('14节点电压')
legend('优化后','优化前')
subplot(3,1,2)
plot(V1(13,:))
hold on
plot(V0(13,:))
ylabel('20节点电压')
subplot(3,1,3)
plot(V1(22,:))
hold on
plot(V0(22,:))
ylabel('27节点电压')
saveas(fig, 'afigure.png')
close(fig)

% meanstate = zeros(length(useful_nodes),3);
% meanstate(:,1) = mean(POPV(:,useful_nodes));
% meanstate(:,2) = mean(QOPV(:,useful_nodes));
% meanstate(:,3) = mean(VOPV(:,useful_nodes));
% stdstate(:,1) = std(POPV(:,useful_nodes));
% stdstate(:,2) = std(QOPV(:,useful_nodes));
% stdstate(:,3) = std(VOPV(:,useful_nodes));
