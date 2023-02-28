from PyXAB.synthetic_obj import *

from PyXAB.algos.SOO import SOO
from PyXAB.partition.BinaryPartition import BinaryPartition
from PyXAB.utils.plot import compare_regret

import math
import numpy as np
import pdb
import pytest


def test_SOO_1():
    partition = BinaryPartition
    domain = [[0, 1]]
    with pytest.raises(ValueError):
        algo = SOO(domain=domain, partition=partition)


def test_SOO_2():
    partition = BinaryPartition
    domain = [[0, 1]]
    with pytest.raises(ValueError):
        algo = SOO(domain=domain, partition = partition)


def test_SOO_3():
    domain = [[0, 1]]
    partition = BinaryPartition
    with pytest.raises(ValueError):
        algo = SOO(domain=domain, partition=partition)


def test_SOO_4():
    T = 100
    Target = Garland.Garland()
    domain = [[0, 1]]
    partition = BinaryPartition
    algo = SOO(n=T, h_max=100, domain=domain, partition=partition)

    for t in range(1, T + 1):
        point = algo.pull(t)
        reward = Target.f(point)
        algo.receive_reward(t, reward)

    algo.get_last_point()
    # plot the regret
    # regret_dic = {"POO": np.array(POO_regret_list)}
    # compare_regret(regret_dic)


def test_SOO_5():
    T = 100
    Target = Ackley.Ackley_Normalized()
    domain = [[0, 1], [0, 1]]
    partition = BinaryPartition
    algo = SOO(n=T, h_max=100, domain=domain, partition=partition)

    for t in range(1, T + 1):
        point = algo.pull(t)
        reward = Target.f(point)
        algo.receive_reward(t, reward)

    algo.get_last_point()
    # plot the regret
    # regret_dic = {"POO": np.array(POO_regret_list)}
    # compare_regret(regret_dic)
