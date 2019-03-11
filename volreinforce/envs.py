# -*- coding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com

import matlab
import matlab.engine
import numpy as np
from multiprocessing import Pool,Pipe,Process
import multiprocessing
import time


class Task:
    EXIT = -2
    RESET = -1
    MAX_STEP = 24480
    EXIT_SEND = [EXIT, 0]
    RESET_SEND = [RESET, 0]

    def __init__(self, name='graduate', envs_num=2, reset_flag = True, episode_length = 1440):
        self.name = name
        self.envs_num = envs_num
        self.start_index = np.arange(envs_num) * 1440
        self.total_step = 0
        self.all_step = 0
        self.reset_flag = reset_flag
        self.episode_length = episode_length
        if envs_num > 16:
            print("# WARNING: TOO MUCH ENVS, NOTICE MEMORY!")
        if envs_num > multiprocessing.cpu_count():
            print("# WARNING: MORE ENVS THAN CPU CORES!")
        self.envs_pool = []
        self.pipes = []
        for i in range(envs_num):
            sp, rp = Pipe(True)
            sp2, rp2 = Pipe(True)
            self.pipes.append([sp, rp, sp2, rp2])
            p = Process(target=self.eng_step, args=([rp, sp2], self.start_index[i], self.episode_length))
            self.envs_pool.append(p)
            p.start()


    def step(self, action):
        '''
        input:
            action: ndarray envs_num * 6
        return:
            message['PQV']: ndarray envs_num * 28 * 6
            message['step_index']: ndarray envs_num * 1
            message['reward']: ndarray envs_num * 1
        '''
        print("envs_num: %d" %self.envs_num)
        for i, pipe in enumerate(self.pipes):
            sp, rp, sp2, rp2 = pipe
            sp.send([self.total_step, action[i,:]])
        PQV = []
        step_index = []
        reward = []
        for pipe in self.pipes:
            sp, rp, sp2, rp2 = pipe
            message_recv = rp2.recv()
            PQV.append(message_recv['PQV'])
            step_index.append(message_recv['step_index'])
            reward.append(message_recv['reward'])
        self.total_step += 1
        self.all_step = self.total_step * self.envs_num
        message = {
            'PQV': np.array(PQV),
            'step_index': np.array(step_index),
            'reward': np.array(reward)
        }
        return message['step_index'], message['PQV'], message['reward'], message['dones']

    def get_stepnum(self):
        return self.total_step, self.all_step

    def reset(self):
        self.total_step = 0
        self.all_step = 0
        for pipe in self.pipes:
            sp, rp, sp2, rp2 = pipe
            sp.send(self.RESET_SEND)

    def close(self):
        for pipe in self.pipes:
            sp, rp, sp2, rp2 = pipe
            sp.send(self.EXIT_SEND)
        for p in self.envs_pool:
            p.join()

    def eng_step(self, pipe, start_index=1, episode_length=1440):
        eng = matlab.engine.start_matlab()  #start matlab in python
        print("start matlab in subprocess!")
        eng.addpath("/home/t630/Voltage_Control/test3", nargout=0)  #add voltage control path to the matlab workspace
        eng.start_matpower()  #start up matpower
        eng.load_data(nargout = 0)
        eng.env_init(nargout = 0)
        rp, sp2 = pipe
        while True:
            try:
                step_index, action =  rp.recv()
                if step_index == self.EXIT:
                    break
                if step_index == self.RESET:
                    eng.envreset(nargout = 0)
                step_index = int(step_index)
                step_index += start_index
                step_index = step_index % self.MAX_STEP
                if step_index == start_index and self.reset_flag:
                    eng.envreset(nargout = 0)
                step_index += 1
                eng.workspace['action_flag'] = list(action)
                eng.workspace['i'] = step_index
                eng.action(nargout = 0)
                eng.save_result(nargout = 0)
                message_send = {'step_index': np.array(eng.workspace['i']),
                                'PQV': np.array(eng.workspace['PQV']),
                                'reward': np.array(eng.workspace['reward'])
                }
                sp2.send(message_send)

            except EOFError:
                break

        eng.quit()


if __name__ == '__main__':
    task = Task(envs_num=10)
    start = time.time()
    step_num = 10
    for i in range(step_num):
        stepi, states, reward = task.step(np.random.binomial(1, 0.7, size=(task.envs_num,6)))
        print(stepi)
        print(states.shape)
        print(reward)
    task.close()
    end = time.time()
    print("TOTAL USE TIME %s" %(end-start))
    print("%s STEPS/s" %(step_num * task.envs_num / (end-start)))
