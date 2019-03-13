# -*- coding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com
import numpy as np
import os
import torch
from agents import A2CAgent
import time

max_steps = 2e8
log_interval = 1440

def run_steps(agent):
    global max_steps
    global log_interval
    agent_name = agent.__class__.__name__
    t0 = time.time()
    while True:
        if log_interval and not (agent.env_step-1) % log_interval:
            rewards = agent.online_rewards
            agent.online_rewards = np.zeros(agent.envs_num)
            if len(rewards) > 0:
                print('total steps %d, returns %.2f/%.2f/%.2f/%.2f (mean/median/min/max), %.2f steps/s' % (
                    agent.env_step, np.mean(rewards), np.median(rewards), np.min(rewards), np.max(rewards),
                    log_interval / (time.time() - t0)))
                t0 = time.time()
        if max_steps and agent.total_step >= max_steps:
            agent.close()
            break
        agent.step()
        # print(agent.env_step)

if __name__ == '__main__':
    agent = A2CAgent(usegpu=True)
    run_steps(agent)
