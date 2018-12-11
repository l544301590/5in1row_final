# -*-coding:utf-8-*-
import json
import random

RIVAL, SELF, NONE = 0, 1, -1
# EMPTY = 7
# W = 35
# WW = 800
# WWW = 15000
# WWWW = 800000
CRT_SELF = [7, 35, 800, 15000, 800000, 0]
# B = 15
# BB = 400
# BBB = 1800
# BBBB = 100000
CRT_RIVAL = [7, 15, 400, 1800, 100000, 0]


def value_(board, x, y, crt, side):
    res = 0

    for i in range(5):
        o, n = 0, 0
        for o in range(-4 + i, -4 + i + 5):
            if 0 <= x + o < 15:
                if board[x + o][y] == side:
                    n += 1
                elif board[x + o][y] == 1 - side:
                    n = -1
                    break
        res += crt[n]

    for i in range(5):
        o, n = 0, 0
        for o in range(-4 + i, -4 + i + 5):
            if 0 <= y + o < 15:
                if board[x][y + o] == side:
                    n += 1
                elif board[x][y + o] == 1 - side:
                    n = -1
                    break
        res += crt[n]

    for i in range(5):
        o, n = 0, 0
        for o in range(-4 + i, -4 + i + 5):
            if 0 <= x + o < 15 and 0 <= y < 15:
                if board[x + o][y + o] == side:
                    n += 1
                elif board[x + o][y + o] == 1 - side:
                    n = -1
                    break
        res += crt[n]

    for i in range(5):
        o, n = 0, 0
        for o in range(-4 + i, -4 + i + 5):
            if 0 <= x + o < 15 and 0 <= y - o < 15:
                if board[x + o][y - o] == side:
                    n += 1
                elif board[x + o][y - o] == 1 - side:
                    n = -1
                    break
        res += crt[n]

    return res


def evaluation_table(board, side):
    res = [[0 for j in range(15)] for i in range(15)]

    for i in range(15):
        for j in range(15):
            if board[i][j] != -1:
                self_value = value_(board, i, j, CRT_SELF, side)
                rival_value = value_(board, i, j, CRT_RIVAL, 1 - side)
                res[i][j] = self_value + rival_value

    return res


def decide(board, side):
    table = evaluation_table(board, side)
    res, vm = [], -99999999

    for i in range(15):
        for j in range(15):
            if table[i][j] > vm:
                res = [(i, j)]
                vm = table[i][j]
            elif table[i][j] == vm:
                res.append((i, j))

    return random.sample(res, 1)[0]


def feasible_actions(board, side, k):
    pass


def is_win(board):
    pass


class Node:
    def __init__(self, board, x, y, side):
        self.n_visited = 0
        self.n_victory = 0
        self.board = board
        self.children = []
        self.side = side
        self.x, self.y = x, y

    def is_leaf(self):
        if self.children:
            return False
        return True


class Game:
    def __init__(self, input_data):
        self.board = [[NONE for j in range(15)] for i in range(15)]
        self.full_input = json.loads(input_data)
        self.reconstruct_board()

    def reconstruct_board(self):
        # 分析自己收到的输入和自己过往的输出，并恢复状态
        all_requests = self.full_input["requests"]
        all_responses = self.full_input["responses"]

        for i in range(len(all_responses)):
            my_input = all_requests[i]  # i回合我的输入
            my_output = all_responses[i]  # i回合我的输出
            self.board[my_input["y"]][my_input["x"]] = RIVAL
            self.board[my_output["y"]][my_output["x"]] = SELF

        curr_input = all_requests[-1]
        if curr_input["x"] >= 0 and curr_input["y"] >= 0:
            self.board[curr_input["y"]][curr_input["x"]] = RIVAL

    def decide(self):
        x, y = 0, 0
        mcts = Mcts(Node(self.board, -1, -1, RIVAL))
        mcts.selection()
        leaf_node = mcts.cur_path[-1]
        if leaf_node.n_visited > 0:
            mcts.expansion(leaf_node, 3)
        my_action = {"x": x, "y": y}
        print(json.dumps({
            "response": my_action
        }))
        return x, y


class Mcts:
    def __init__(self, root, n=1000):
        self.root = root
        self.cur_path = []  # 不包括root结点

    def selection(self):
        nodes = []

        self.cur_path = nodes

    def expansion(self, node, k):
        nodes = feasible_actions(node.board, node.side, k)
        node.children = nodes
        self.cur_path.append(nodes[random.randint(0, 2)])

    def simulation(self):
        final_node = self.cur_path[-1]  # 当前路径上最后一个结点
        board = final_node.board        # 当前棋局
        side = final_node.side        # 上一次落子方

        while True:
            side = 1 - side     # 当前执子方
            x, y = decide(board, side)  # 决策落子
            board[x][y] = side  # 落子
            res = is_win(board)  # 己方胜利返回SELF，对手胜利返回RIVAL，尚未结果返回NONE
            if res == SELF:  # 若己方胜利
                for node in self.cur_path:
                    node.n_victory += 1
                    node.n_visited += 1
                break
            elif res == RIVAL:
                for node in self.cur_path:
                    node.n_visited += 1
                break


if __name__ == '__main__':
    Game(input())
