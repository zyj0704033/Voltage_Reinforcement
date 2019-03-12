# -*- coding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com

import torch
import numpy as np
from networks import *
from envs import *
from reply import Storage
from utils import *

class A2CAgent(object):
    """docstring for A2CAgent."""
    def __init__(self, usegpu=True):
        super(A2CAgent, self).__init__()
        self.device = torch.device("cuda:0" if (torch.cuda.is_available() and usegpu) else "cpu")
        self.network = ActorCriticNet().to(self.device)
        self.env = Task(envs_num=8)
        self.envs_num =  self.env.envs_num
        self.optimizer = torch.optim.RMSprop(self.network.parameters(), lr=1e-4, alpha=0.99, eps=1e-5)
        self.total_step = 0
        self.env_step = 0
        self.rollout = 10
        _, self.states, _, _ = self.env.step(np.ones((self.env.envs_num, 6)))
        self.state_norm = Normlizer(self.device)
        self.discount = 0.9
        self.gae_lamda = 0.99
        self.value_loss_weight = 1
        self.gradient_clip = 5
        self.episode_rewards = []
        self.online_rewards = np.zeros(self.envs_num)



    def step(self):
        storage = Storage(self.rollout)
        state = self.states
        for _ in range(self.rollout):
            prediction = self.network(self.state_norm.meanstdnorm(state, self.envs_num))
            stepi, next_states, rewards, dones = self.env.step(to_np(prediction['a']).astype(np.int64))
            self.online_rewards += rewards
            for i, done in enumerate(dones):
                if done:
                    self.episode_rewards.append(self.online_rewards[i])
                    self.online_rewards[i] = 0
            storage.add(prediction)
            storage.add({'r': tensor(rewards).unsqueeze(-1).to(self.device),
                         'm': tensor(1 - dones).unsqueeze(-1).to(self.device)})
            states = next_states

        self.states = states
        prediction = self.network(self.state_norm.meanstdnorm(state, self.envs_num))
        storage.add(prediction)
        storage.placeholder()


        advantages = tensor(np.zeros((self.envs_num, 1))).to(self.device)
        returns = prediction['v'].detach()
        for i in reversed(range(self.rollout)):
            returns = storage.r[i] + self.discount * storage.v[i+1]
            td_error = storage.r[i] + self.discount * storage.v[i+1] - storage.v[i]
            advantages = advantages * self.gae_lamda + td_error
            storage.adv[i] = advantages.detach()
            storage.ret[i] = returns.detach()

        log_prob, value, returns, advantages = storage.cat(['log_pi_a', 'v', 'ret', 'adv'])
        policy_loss = -(log_prob * advantages).mean()
        value_loss = 0.5 * (returns - value).pow(2).mean()
        self.optimizer.zero_grad()
        (policy_loss  + self.value_loss_weight * value_loss).backward()
        nn.utils.clip_grad_norm_(self.network.parameters(), self.gradient_clip)
        self.optimizer.step()

        self.total_step = self.env.all_step
        self.env_step = self.env.total_step


    def close(self):
        self.env.close()


    def pretrain(self):
        pass

    def eval(self):
        pass


if __name__ == '__main__':
    agent = A2CAgent(envs_num=8)

# class PPOAgent(object):
#     """docstring for A2CAgent."""
#     def __init__(self):
#         super(PPOAgent, self).__init__()
#         self.network = ActorCriticNet()
#         self.env = Task()
#         self.envs_num =  self.env.envs_num
#         self.optimizer = torch.optim.RMSprop(self.network.parameters(), lr=1e-4, alpha=0.99, eps=1e-5)
#         self.total_step = 0
#         self.rollout = 15
#         stepi, self.states, reward = Task().step(np.ones((self.env.envs_num, 6)))
#         self.state_norm = Normlizer()
#         self.discount = 0.9
#         self.gae_lamda = 0.99
#         self.value_loss_weight = 1
#         self.gradient_clip = 5
#         self.episode_rewards = []
#
#         self.reward_store = []
#         self.state_value = 0
#         self.prediction_store = []
#         for i in range(self.rollout):
#             self.reward_store.append(reward)
#             prediction = self.network(self.state_norm.meanstdnorm(state))
#             self.prediction_store.append(prediction)
#             stepi, next_states, reward = self.env.step(to_np(prediction['a']))
#             self.states = next_states
#
#
#     def step(self):
#         storage = Storage(self.rollout)
#         state = self.states
#         for _ in range(self.rollout):
#             prediction = self.network(self.state_norm.meanstdnorm(state))
#             stepi, next_states, rewards = self.env.step(to_np(prediction['a']))
#             self.online_rewards += rewards
#             for i, done in enumerate(dones):
#                 if done:
#                     self.episode_rewards.append(self.online_rewards[i])
#                     self.online_rewards[i] = 0
#             storage.add(prediction)
#             storage.add({'r': tensor(rewards).unsqueeze(-1),
#                          'm': tensor(1 - dones).unsqueeze(-1)})
#             states = next_states
#
#         self.states = states
#         prediction = self.network(self.state_norm.meanstdnorm(state))
#         storage.add(prediction)
#         storage.placeholder()
#
#
#         advantages = tensor(np.zeros((self.envs_num, 1)))
#         returns = prediction['v'].detach()
#         for i in reversed(range(self.rollout)):
#             returns = storage.r[i] + self.discount * returns
#             td_error = storage.r[i] + self.discount * storage.v[i+1] - storage.v[i]
#             advantages = advantages * self.gae_lamda + td_error
#             storage.adv = advantages.detach()
#             storage.ret = returns.detach()
#
#         log_prob, value, returns, advantages, entropy = storage.cat(['log_pi_a', 'v', 'ret', 'adv', 'ent'])
#         policy_loss = -(log_prob * advantages).mean()
#         value_loss = 0.5 * (returns - value).pow(2).mean()
#         self.optimizer.zero_grad()
#         (policy_loss  + self.value_loss_weight * value_loss).backward()
#         nn.utils.clip_grad_norm_(self.network.parameters(), self.gradient_clip)
#         self.optimizer.step()
#
#
#     def pretrain(self):
#         pass
#
#     def eval(self):
#         pass
