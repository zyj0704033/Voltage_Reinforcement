# -*- coding:utf-8 -*-
# author: zhangyujing@tsinghua
# email: zyj0704033@163.com
import scipy.io
import numpy
import torch


class Normlizer(object):
    def __init__(self, file_path='../test3/', filename='PVQ'):
        super(Normlizer, self).__init__()
        self.dmean = scipy.io.loadmat(file_path+'meanstate.mat')['meanstate']
        self.dstd = scipy.io.loadmat(file_path+'stdstate.mat')['stdstate']

    def meanstdnorm(self, state, batch_size):
        normtensor = torch.tensor(((state - self.dmean) / (self.dstd)).T, dtype=torch.float)
        return normtensor.view(batch_size, 1, 3, -1)

def to_np(t):
    return t.cpu().detach().numpy()


def tensor(x):
    if isinstance(x, torch.Tensor):
        return x
    x = torch.tensor(x, dtype=torch.float32)
    return x
