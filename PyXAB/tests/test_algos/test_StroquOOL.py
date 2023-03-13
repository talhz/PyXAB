from PyXAB.synthetic_obj import *

from PyXAB.algos.StroquOOL import StroquOOL
from PyXAB.partition.BinaryPartition import BinaryPartition
from PyXAB.utils.plot import compare_regret
import math
import numpy as np
import pdb
import pytest

def test_StroquOOL_ValueError_1():
    partition = BinaryPartition
    with pytest.raises(ValueError):
        algo = StroquOOL(partition=partition)

def test_StroquOOL_ValueError_2():
    domain = [[0, 1]]
    with pytest.raises(ValueError):
        algo = StroquOOL(domain=domain)

def test_StroquOOL_DoubleSine():
    T = 500
    Target = DoubleSine.DoubleSine()
    domain = [[0, 1]]
    partition = BinaryPartition
    algo = StroquOOL(n=T, domain=domain, partition=partition)

    for t in range(1, T + 1):
        point = algo.pull(t)
        reward = Target.f(point) + np.random.uniform(-0.1, 0.1)
        algo.receive_reward(t, reward)

def test_StroquOOL_Ackley():
    T = 500
    Target = Ackley.Ackley_Normalized()
    domain = [[0, 1], [0, 1]]
    partition = BinaryPartition
    algo = StroquOOL(n=T, domain=domain, partition=partition)

    for t in range(1, T + 1):
        point = algo.pull(t)
        reward = Target.f(point) + np.random.uniform(-0.1, 0.1)
        algo.receive_reward(t, reward)
    
def test_StroquOOL_Garland():
    T = 500
    Target = Garland.Garland()
    domain = [[0, 1]]
    partition = BinaryPartition
    algo = StroquOOL(n=T, domain=domain, partition=partition)

    for t in range(1, T + 1):
        point = algo.pull(t)
        reward = Target.f(point) + np.random.uniform(-0.1, 0.1)
        algo.receive_reward(t, reward)
        