# -*- coding: utf-8 -*-
"""Implementation of HCT (Azar et al, 2014)
"""
# Author: Wenjie Li <li3549@purdue.edu>
# License: MIT


import math
import numpy as np
import pdb
from algos.Algo import Algorithm


def compute_t_plus(x):
    return np.power(2, np.ceil(np.log(x) / np.log(2)))


class HCT(Algorithm):

    def __init__(self, nu=1, rho=0.75, delta=0.01, partition=None):
        super(HCT, self).__init__(partition)

        self.iteration = 0
        self.nu = nu
        self.rho = rho
        self.delta = delta
        self.c = 0.1
        self.c1 = np.power(rho/(3 * nu), 1.0/8)

        # List of values that are important

        self.Bvalues = [[np.inf]]
        self.Uvalues = [[np.inf]]
        self.Rewards = [[0]]
        self.visitedTimes = [[0]]
        self.visited = [[True]]
        self.tau_h = [0] # Threshold on each layer
        self.expand(self.partition.get_root())


    def optTraverse(self):

        # Update the thresholds

        t_plus = compute_t_plus(self.iteration)
        delta_tilde = np.minimum(1.0/2, self.c1 * self.delta / t_plus)
        self.tau_h = [0.0]
        for i in range(1, len(self.list)):

            self.tau_h.append(np.ceil(self.c ** 2 * math.log(1/delta_tilde) * self.rho ** (-2 * i) / self.nu ** 2))


        curr_node = self.partition.get_root()
        path = [curr_node]

        while self.visitedTimes[curr_node.get_depth()][curr_node.get_index()-1] >= self.tau_h[curr_node.get_depth()] \
           and curr_node.get_children() is not None:
            children = curr_node.get_children()
            maxchild = children[0].get_index()  # temporarily set the maxchild to be the first child

            for child in children:
                c_depth = child.get_depth()
                c_index = child.get_index()

                # If the child is never visited or prepared to be visited, denote maxchild = -1 and break
                if not self.visited[c_depth][c_index - 1]:
                    maxchild = -1
                    break
                elif self.Bvalues[c_depth][c_index - 1] >= self.Bvalues[c_depth][maxchild - 1]:
                    maxchild = c_index

            # If we find that the child is never visited, stop going deeper
            if maxchild == -1:
                break
            else:
                curr_node = self.partition.get_node(curr_node.get_depth() + 1, maxchild)
                path.append(curr_node)

        return curr_node, path
    

    def updateRewardTree(self, path, reward):

        node = path[-1]
        node.updateReward(reward)

        self.iteration += 1

    def updateUvalueTree(self):
        t_plus = self.compute_t_plus(self.iteration)
        delta_tilde = np.minimum(1, self.c1 * self.delta / t_plus)
        for layer in self.list:
            for node in layer:

                if node.visitedTimes == 0:
                    continue
                else:
                    node.Uvalue = node.meanReward + math.sqrt(self.c ** 2 * math.log(1/delta_tilde) / node.visitedTimes) + \
                              self.nu * (self.rho ** node.depth)



    def updateBackwardTree(self):

        for i in range(1, len(self.list)+1):

            layer = self.list[-i]
            for node in layer:
                node.updateBackward()

    def expand(self, parent):

        dim = np.random.randint(0, len(parent.range))
        selected_dim = parent.range[dim]

        range1 = parent.range.copy()
        range2 = parent.range.copy()

        range1[dim] = [selected_dim[0], (selected_dim[0] + selected_dim[1])/2]
        range2[dim] = [(selected_dim[0] + selected_dim[1])/2, selected_dim[1]]

        node1 = HCT_Node(parent.depth+1, 2 * parent.index, parent, range1)
        node2 = HCT_Node(parent.depth+1, 2 * parent.index - 1, parent, range2)

        parent.children = [node1, node2]

        if len(self.list) <= parent.depth + 1:
            self.list.append([node1, node2])
        else:
            self.list[parent.depth + 1].append(node1)
            self.list[parent.depth + 1].append(node2)

    def updateAllTree(self, path, end_node, reward):

        t_plus = self.compute_t_plus(self.iteration)
        delta_tilde = np.minimum(1, self.c1 * self.delta / t_plus)


        if self.iteration == self.compute_t_plus(self.iteration):

            self.updateUvalueTree()
            self.updateBackwardTree()

        path.append(end_node)

        self.updateRewardTree(path, reward)

        end_node = path[-1]

        end_node.Uvalue = end_node.meanReward + math.sqrt(self.c ** 2 * math.log(1/delta_tilde) / end_node.visitedTimes) + \
                              self.nu * (self.rho ** end_node.depth)

        self.updateBackwardTree()


        # print(self.tau_h)
        # Expand or not

        if end_node.children is None and end_node.visitedTimes >= self.tau_h[end_node.depth]:
            self.expand(end_node)







### Implementation of HCT (Azar et al, 2014)

class HCT_Node:
    def __init__(self, depth, index, parent, range):
        self.depth = depth
        self.index = index
        self.meanReward = 0
        self.visitedTimes = 0
        self.parent = parent
        self.children = None
        self.Uvalue = np.inf
        self.Bvalue = np.inf
        self.range = range

    def updateReward(self, reward):

        self.visitedTimes += 1
        self.meanReward = ((self.visitedTimes - 1) / self.visitedTimes * self.meanReward) + (reward / self.visitedTimes)

    def updateBackward(self):

        if self.children is None:
            self.Bvalue = self.Uvalue
        else:
            tempB = 0
            for child in self.children:
                tempB = np.maximum(tempB, child.Bvalue)
            self.Bvalue = np.minimum(self.Uvalue, tempB)



class HCT_tree:

    def __init__(self, nu, rho, range, delta=0.01):
        self.root = HCT_Node(0, 1, None, range)
        self.list = [[self.root]]
        self.iteration = 0
        self.nu = nu
        self.rho = rho
        self.delta = delta
        self.c = 0.1
        self.c1 = np.power(rho/(3 * nu), 1.0/8)
        self.createNewNodes(self.root)
        self.tau_h = [0]

    def optTraverse(self):

        # Update the thresholds
        self.iteration += 1

        t_plus = self.compute_t_plus(self.iteration)
        delta_tilde = np.minimum(1.0/2, self.c1 * self.delta / t_plus)
        self.tau_h = [0.0]
        for i in range(1, len(self.list)):

            self.tau_h.append(np.ceil(self.c ** 2 * math.log(1/delta_tilde) * self.rho ** (-2 * i) / self.nu ** 2))

        curr_node = self.root
        path = []
        while curr_node.visitedTimes >= self.tau_h[curr_node.depth] and curr_node.children is not None:

            path.append(curr_node)

            child1 = curr_node.children[0]
            child2 = curr_node.children[1]
            if child1.Bvalue >= child2.Bvalue:
                curr_node = child1
            else:
                curr_node = child2

        return curr_node, path

    def updateRewardTree(self, path, reward):

        node = path[-1]
        node.updateReward(reward)


    def updateUvalueTree(self):
        t_plus = self.compute_t_plus(self.iteration)
        delta_tilde = np.minimum(1, self.c1 * self.delta / t_plus)
        for layer in self.list:
            for node in layer:

                if node.visitedTimes == 0:
                    continue
                else:
                    node.Uvalue = node.meanReward + math.sqrt(self.c ** 2 * math.log(1/delta_tilde) / node.visitedTimes) + \
                              self.nu * (self.rho ** node.depth)

    def compute_t_plus(self, x):

        return np.power(2, np.ceil(np.log(x) / np.log(2)))


    def updateBackwardTree(self):

        for i in range(1, len(self.list)+1):

            layer = self.list[-i]
            for node in layer:
                node.updateBackward()

    def createNewNodes(self, parent):

        dim = np.random.randint(0, len(parent.range))
        selected_dim = parent.range[dim]

        range1 = parent.range.copy()
        range2 = parent.range.copy()

        range1[dim] = [selected_dim[0], (selected_dim[0] + selected_dim[1])/2]
        range2[dim] = [(selected_dim[0] + selected_dim[1])/2, selected_dim[1]]

        node1 = HCT_Node(parent.depth+1, 2 * parent.index, parent, range1)
        node2 = HCT_Node(parent.depth+1, 2 * parent.index - 1, parent, range2)

        parent.children = [node1, node2]

        if len(self.list) <= parent.depth + 1:
            self.list.append([node1, node2])
        else:
            self.list[parent.depth + 1].append(node1)
            self.list[parent.depth + 1].append(node2)

    def updateAllTree(self, path, end_node, reward):

        t_plus = self.compute_t_plus(self.iteration)
        delta_tilde = np.minimum(1, self.c1 * self.delta / t_plus)


        if self.iteration == self.compute_t_plus(self.iteration):

            self.updateUvalueTree()
            self.updateBackwardTree()

        path.append(end_node)

        self.updateRewardTree(path, reward)

        end_node = path[-1]

        end_node.Uvalue = end_node.meanReward + math.sqrt(self.c ** 2 * math.log(1/delta_tilde) / end_node.visitedTimes) + \
                              self.nu * (self.rho ** end_node.depth)

        self.updateBackwardTree()


        # print(self.tau_h)
        # Expand or not

        if end_node.children is None and end_node.visitedTimes >= self.tau_h[end_node.depth]:
            self.createNewNodes(end_node)









