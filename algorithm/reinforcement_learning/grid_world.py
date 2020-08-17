#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top
#

'''
策略迭代:（随机策略）策略评估（贝尔曼方程）+策略改进（贪婪）
值迭代：某个策略的最大值，不断迭代直到值收敛（贝尔曼最优方程）

'''
#######################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.table import Table

matplotlib.use('Agg')

WORLD_SIZE = 5
A_POS = [0, 1]
A_PRIME_POS = [4, 1]
B_POS = [0, 3]
B_PRIME_POS = [2, 3]
DISCOUNT = 0.9

##初始状态(0,0)变到(0,-1)是向左，
# left, up, right, down
ACTIONS = [np.array([0, -1]),
           np.array([-1, 0]),
           np.array([0, 1]),
           np.array([1, 0])]
ACTION_PROB = 0.25


def step(state, action):
    if state == A_POS:
        return A_PRIME_POS, 10
    if state == B_POS:
        return B_PRIME_POS, 5

    #当前状态，采取动作后转移到下一个状态的概率为1，所以直接转移到下一个状态
    next_state = (np.array(state) + action).tolist()
    x, y = next_state
    if x < 0 or x >= WORLD_SIZE or y < 0 or y >= WORLD_SIZE:
        reward = -1.0
        #越界后恢复当前状态
        next_state = state
    else:
        reward = 0
    return next_state, reward


def draw_image(image):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox=[0, 0, 1, 1])

    nrows, ncols = image.shape
    width, height = 1.0 / ncols, 1.0 / nrows

    # Add cells
    for (i, j), val in np.ndenumerate(image):
        tb.add_cell(i, j, width, height, text=val,
                    loc='center', facecolor='white')

    # Row and column labels...
    for i in range(len(image)):
        tb.add_cell(i, -1, width, height, text=i+1, loc='right',
                    edgecolor='none', facecolor='none')
        tb.add_cell(-1, i, width, height/2, text=i+1, loc='center',
                    edgecolor='none', facecolor='none')

    ax.add_table(tb)


def figure_3_2():
    '''
    策略评估：得到收敛的值函数
    采用等概率随机策略进行，状态值函数最终收敛
    This value function was computed by solving the system of linear equations (3.14).
    通过解状态值函数线性方程组，求解值函数（也就是求解每个状态的值函数，然后对随机策略进行评估）
    :return:
    '''
    value = np.zeros((WORLD_SIZE, WORLD_SIZE))
    times=0
    while True:
        times=times+1
        print('times={}'.format(times))
        # keep iteration until convergence
        new_value = np.zeros_like(value)
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                #(i,j)为给定的当前状态，然后将策略走完
                # 一个策略会走完，总共4种可能性，上下左右都为0.25
                for action in ACTIONS:
                    # 当前状态，采取一步行动之后，得到下一步状态和奖励
                    # 状态(0,0)，采取向左（向上）行动，得到奖励-1，下一个状态仍为（0,0）；
                                # 向右行动，状态变为(0,1),向下行动，状态变为（1,0）

                    (next_i, next_j), reward = step([i, j], action)
                    print('当前状态{}，采取行动{}，获得奖励{}，下一个状态{}'.format((i,j),action,reward,(next_i,next_j)))
                    # bellman equation
                    #value初始值全为0
                    #当前状态值new_value[i, j]不断得到更新；会用到后面的状态值，但是后面的状态值初始化全为0
                    #两个循环会把所有的当前状态值都更新一遍
                    new_value[i, j] += ACTION_PROB * (reward + DISCOUNT * value[next_i, next_j])
        if np.sum(np.abs(value - new_value)) < 1e-4:
            draw_image(np.round(new_value, decimals=2))
            plt.savefig('figure_3_2.png')
            plt.close()
            break
        value = new_value


def figure_3_5():
    '''
    （策略改善：值函数收敛之后，进行策略改善，寻找每个状态的最优动作。实际上不一定等到值函数收敛，
    策略改善可能已经是最优策略；但是这个地方是通过贝尔曼最优方程求最优策略）

    解贝尔曼方程获取最优值函数和最优策略
    状态值函数最优（存在最优策略），动作状态值函数最优（最优策略下的最优动作）；此时最优状态值函数和最优动作-状态值函数相等
    :return:
    '''
    value = np.zeros((WORLD_SIZE, WORLD_SIZE))
    while True:
        # keep iteration until convergence
        new_value = np.zeros_like(value)
        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                values = []
                #一个策略会走完，总共4种可能性，上下左右
                for action in ACTIONS:
                    #当前状态，采取一步行动之后，得到下一步状态和奖励
                    (next_i, next_j), reward = step([i, j], action)
                    # value iteration
                    values.append(reward + DISCOUNT * value[next_i, next_j])
                #选择最优动作；通过迭代找到最优策略
                #只选择状态值最大的那个策略
                new_value[i, j] = np.max(values)
        if np.sum(np.abs(new_value - value)) < 1e-4:
            draw_image(np.round(new_value, decimals=2))
            plt.savefig('figure_3_5.png')
            plt.close()
            break
        value = new_value


if __name__ == '__main__':
    # figure_3_2()
    figure_3_5()

'''
当前状态(0, 0)，采取行动[ 0 -1]，获得奖励-1.0，下一个状态(0, 0)
当前状态(0, 0)，采取行动[-1  0]，获得奖励-1.0，下一个状态(0, 0)
当前状态(0, 0)，采取行动[0 1]，获得奖励0，下一个状态(0, 1)
当前状态(0, 0)，采取行动[1 0]，获得奖励0，下一个状态(1, 0)

当前状态(0, 1)，采取行动[ 0 -1]，获得奖励10，下一个状态(4, 1)
当前状态(0, 1)，采取行动[-1  0]，获得奖励10，下一个状态(4, 1)
当前状态(0, 1)，采取行动[0 1]，获得奖励10，下一个状态(4, 1)
当前状态(0, 1)，采取行动[1 0]，获得奖励10，下一个状态(4, 1)

当前状态(0, 2)，采取行动[ 0 -1]，获得奖励0，下一个状态(0, 1)
当前状态(0, 2)，采取行动[-1  0]，获得奖励-1.0，下一个状态(0, 2)
当前状态(0, 2)，采取行动[0 1]，获得奖励0，下一个状态(0, 3)
当前状态(0, 2)，采取行动[1 0]，获得奖励0，下一个状态(1, 2)

当前状态(0, 3)，采取行动[ 0 -1]，获得奖励5，下一个状态(2, 3)
当前状态(0, 3)，采取行动[-1  0]，获得奖励5，下一个状态(2, 3)
当前状态(0, 3)，采取行动[0 1]，获得奖励5，下一个状态(2, 3)
当前状态(0, 3)，采取行动[1 0]，获得奖励5，下一个状态(2, 3)
当前状态(0, 4)，采取行动[ 0 -1]，获得奖励0，下一个状态(0, 3)
当前状态(0, 4)，采取行动[-1  0]，获得奖励-1.0，下一个状态(0, 4)
当前状态(0, 4)，采取行动[0 1]，获得奖励-1.0，下一个状态(0, 4)
当前状态(0, 4)，采取行动[1 0]，获得奖励0，下一个状态(1, 4)
当前状态(1, 0)，采取行动[ 0 -1]，获得奖励-1.0，下一个状态(1, 0)
当前状态(1, 0)，采取行动[-1  0]，获得奖励0，下一个状态(0, 0)
当前状态(1, 0)，采取行动[0 1]，获得奖励0，下一个状态(1, 1)

'''