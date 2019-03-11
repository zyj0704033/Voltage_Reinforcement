# -*- coding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com
import numpy as np
import os
import torch
from agents import A2CAgent
import time

max_steps = 2e8
log_interval = 24480

def run_steps(agent):
    global max_steps
    global log_interval
    agent_name = agent.__class__.__name__
    t0 = time.time()
    while True:
        if log_interval and not agent.total_step % log_interval:
            rewards = agent.episode_rewards
            agent.episode_rewards = []
            print('total steps %d, returns %.2f/%.2f/%.2f/%.2f (mean/median/min/max), %.2f steps/s' % (
                agent.total_step, np.mean(rewards), np.median(rewards), np.min(rewards), np.max(rewards),
                log_interval / (time.time() - t0)))
            t0 = time.time()
        if max_steps and agent.total_step >= max_steps:
            agent.close()
            break
        agent.step()

if __name__ == '__main__':
    agent = A2CAgent()
    run_steps(agent)
