from synthetic_obj import *

from algos.VHCT import VHCT, VHCT_tree

from partition.BinaryPartition import BinaryPartition
from utils import plot_regret, compare_regret
import numpy as np
import pdb

T = 1000
Target = DoubleSine.DoubleSine()
domain = [[0, 1]]
partition = BinaryPartition(domain)
algo = VHCT(partition=partition)

cumulative_regret = 0
cumulative_regret_list = [0]


VHCT_regret_list = []
regret = 0
tree = VHCT_tree(1, 0.75, domain, bound=1)

for t in range(1, T+1):

    # T-HOO
    point = algo.pull(t)
    reward = Target.f(point) + np.random.uniform(-0.1, 0.1)
    algo.receive_reward(t, reward)
    inst_regret = Target.fmax - Target.f(point)
    cumulative_regret += inst_regret
    cumulative_regret_list.append(cumulative_regret)

    # print('t: ', t,'VHCT: ', point)

regret_dic = {'VHCT': np.array(cumulative_regret_list),
              'VHCT_old': np.array(VHCT_regret_list)}
compare_regret(regret_dic)