import queue
import copy
import numpy as np

class node:
    def __init__(self, init_state, parent= None):
        self.state= init_state
        self.parent = parent
        self.goal = np.array([[1, 2, 3],
                              [4, 5, 6],
                              [7, 8, 0]])
        self.root = 0
    def set_root(self,r):
        self.root = r
    def isGoalState(self):
        return np.array_equal(self.state,self.goal)

    def fetch(self):
        r, c = np.squeeze(np.where((self.state==self.root)))
        move = [(r+1, c),(r-1, c), (r, c+1), (r, c-1)]
        valid_move = []

        for i in move:
            if (i[0] >= 0) and (i[0] < 3) and (i[1] >= 0) and (i[1] < 3):
                valid_move.append(i)

        child = []
        for move in valid_move:
            new = copy.deepcopy(self.state)
            new[r, c], new[move] = new[move], new[r,c]
            child.append(new)
        return child

class BFS:
    def __init__(self, init_state):
        self.init_state = init_state
        self.visited = set()

    def reconstruct_path(self, Node):
        sol_path = []
        while Node is not None:
            sol_path.append(Node.state)
            Node = Node.parent
        sol_path.reverse() 
        return sol_path

    def solve(self, r=0):
        init_node = node(self.init_state)
        init_node.set_root(r)
        q = queue.Queue()
        q.put(init_node)
        while not q.empty():
            current_node = q.get()
            if current_node.isGoalState():
                solution_path = self.reconstruct_path(current_node)
                return solution_path
            if tuple(current_node.state.flatten()) in self.visited:
                continue

            child_states = current_node.fetch()
            self.visited.add(tuple(current_node.state.flatten()))

            for child_state in child_states:
                if tuple(child_state.flatten()) not in self.visited:
                    child_node = node(child_state, parent=current_node)
                    q.put(child_node)

        return None

fake_state = np.array([[1, 5, 0],
                       [4, 6, 3],
                       [2, 7, 8]])
solver = BFS(fake_state)
result = solver.solve()

if result:
    print('solution steps :')
    for index, state in enumerate(result):
        print(f'step {index+1}')
        print(state)
        print('-----------------')
else:
    print('no result found ')