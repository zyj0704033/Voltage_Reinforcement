function [action_return, voltage_return] = cal_return(action_flag, PQV)
% function: calculate the return for an state
%
% Extended description

% %% return 1
% return_idx = [1 5 10 16 18 22];
% Vpv = PQV(return_idx, 3);
% action_return = -sum(action_flag);
% if max(abs(Vpv-1)) < 0.01
%   voltage_return = 1;
% elseif max(abs(Vpv-1)) < 0.02
%   voltage_return = 0;
% elseif max(abs(Vpv-1)) < 0.03
%   voltage_return =  -3*(sum(max(abs(Vpv-1) - 0.02, 0) * 200))^2;
% else
%   voltage_return = -200;
% end

%% return 2
return_idx = [1 5 10 16 18 22];
Vpv = PQV(return_idx, 3);
action_return = -sum(action_flag)/6;
if max(abs(Vpv-1)) > 0.03
  voltage_return = -10;
else
  voltage_return = 0;
end



end  % function
