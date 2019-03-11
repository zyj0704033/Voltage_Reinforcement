# -*- coding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com

import torch.nn as nn
import torch

class ConvBody(nn.Module):
    def __init__(self):
        super(ConvBody, self).__init__()
        self.conv1 = nn.Conv2d(1,16,kernel_size=(2,9),padding=(0,4))
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16,32,(2,7),padding=(0,3))
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32,32,(1,7),padding=(0,3))
        self.bn3 = nn.BatchNorm2d(32)
        self.fc = nn.Linear(896, 200)
        self.relu = nn.ReLU()

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')

    def forward(self, x):
        y = self.bn1(self.conv1(x))
        y = self.relu(y)
        y = self.bn2(self.conv2(y))
        y = self.relu(y)
        y = self.bn3(self.conv3(y))
        y = self.relu(y)
        y = y.view(-1, 896)
        y = self.fc(y)
        y = self.relu(y)
        return y



class ActorCriticNet(nn.Module):
    def __init__(self):
        super(ActorCriticNet, self).__init__()
        self.ConvBody = ConvBody()
        self.actornet = nn.Linear(200, 6)
        self.valuenet = nn.Linear(200, 1)
        self.sigmoid = nn.Sigmoid()
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')

    def forward(self, x, action=None):
        y = self.ConvBody(x)
        a = self.sigmoid(self.actornet(y))
        v = self.valuenet(y)
        action_dist = torch.distributions.bernoulli.Bernoulli(probs=a)
        if action is None:
            action = action_dist.sample()
        log_prob = torch.sum(action_dist.log_prob(action), 1)
        entropy = torch.sum(action_dist.entropy(), 1)

        return {
            'a': action,
            'log_pi_a': log_prob,
            'ent': entropy,
            'v': v
        }
