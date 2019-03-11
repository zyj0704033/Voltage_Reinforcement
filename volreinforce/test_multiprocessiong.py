# -*- encoding=utf-8 -*-
import matlab
import matlab.engine
from multiprocessing import Process,Pipe
import os
import time

def env_step(pipe):
    eng = matlab.engine.start_matlab()  #start matlab in python
    print("start matlab in subprocess!")
    eng.addpath("/home/t630/Voltage_Control/test3", nargout=0)  #add voltage control path to the matlab workspace
    eng.start_matpower()  #start up matpower
    eng.load_data(nargout = 0)
    eng.env_init(nargout = 0)
    while True:
        try:
            step_index =  pipe.recv()
            if int(step_index) == 0:
                break
            step_index = int(step_index)
            eng.workspace['i'] = step_index
            eng.action(nargout = 0)
            print("PID %s get step_index: %s  , workspace i: %s" %(os.getpid(), step_index, eng.workspace['i']))
        except EOFError:
            break
    print("PID %s finish!" %os.getpid())
    eng.quit()




if __name__ == '__main__':
    send_pipe, receive_pipe = Pipe(True)
    send_pipe2, receive_pipe2 = Pipe(True)
    p1 = Process(target=env_step, args=(receive_pipe,))
    p2 = Process(target=env_step, args=(receive_pipe2,))
    start1 = time.time()
    p1.start()
    p2.start()
    receive_pipe.close()
    for i in range(1,1000):
        send_pipe.send(i)
        send_pipe2.send(i)
    send_pipe.send(0)
    send_pipe2.send(0)
    send_pipe.close()
    send_pipe2.close()
    p1.join()
    p2.join()
    print("close send pipe")
    end1 = time.time()


    start = time.time()
    eng = matlab.engine.start_matlab()  #start matlab in python
    eng.addpath("/home/t630/Voltage_Control/test3", nargout=0)  #add voltage control path to the matlab workspace
    eng.start_matpower()  #start up matpower
    eng.load_data(nargout = 0)
    N = 1000
    eng.env_init(nargout = 0)
    for i in range(1, N):
    	eng.workspace['i'] = i
    	eng.action(nargout = 0)
    	eng.save_result(nargout = 0)
    	print(i)
    eng.quit()
    end = time.time()
    print("using time %s for multiprocessing" %(end1 -start1))
    print("using time %s for one processing" %(end - start))
