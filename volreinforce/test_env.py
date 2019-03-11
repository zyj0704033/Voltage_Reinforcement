#-*- encoding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com
# test for the reinforcement learning voltage control env
import matlab
import matlab.engine

eng = matlab.engine.start_matlab()  #start matlab in python
eng.addpath("/home/t630/Voltage_Control/test3", nargout=0)  #add voltage control path to the matlab workspace
eng.start_matpower(nargout = 0)  #start up matpower
eng.load_data(nargout = 0)
N = 3000
eng.env_init(nargout = 0)
for i in range(1, N):
	eng.workspace['i'] = i
	eng.action(nargout = 0)
	eng.save_result(nargout = 0)
	print(i)
eng.quit()
print("finish test matlab!")
