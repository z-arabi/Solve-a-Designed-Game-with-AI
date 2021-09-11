import queue

# global variable
parent={}
frontier=queue.Queue()
explored=[]
k=m=n=0

# k number of columns , m number of colors m <= k , n number of cards of same color
def generator(s):
    next_states=[]
    for i in range(len(s)):
        if s[i]:
            for j in range(len(s)):
                s_mid = [x[:] for x in s]
                if i != j:
                    if s[j]:
                        if (s_mid[i][-1][0] < s_mid[j][-1][0]):
                            s_mid[j].append(s_mid[i][-1])
                            s_mid[i].pop()
                            if s_mid not in list(frontier.queue) and s_mid not in explored:
                                parent[tuple(tuple(x) for x in s_mid)] = [tuple(tuple(x) for x in s),f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                                next_states.append(s_mid)
                    else:
                        s_mid[j].append(s_mid[i][-1])
                        s_mid[i].pop()
                        if s_mid not in list(frontier.queue) and s_mid not in explored:
                            parent[tuple(tuple(x) for x in s_mid)] = [tuple(tuple(x) for x in s),f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                            next_states.append(s_mid)
    return next_states

def check(states):
    for state in states:
        for i,column in enumerate(state):
            if column:
                color = state[i][0][1]
                lst = [f"{x}{color}" for x in range(n,0,-1)]
                if column != lst:
                    return False
        return state

def backtrace(parent, start, end):
    start = tuple([tuple(x) for x in start])
    end = tuple([tuple(x) for x in end])
    path = [end]
    actions = []
    while path[-1] != start:
        actions.append(parent[path[-1]][1])
        path.append(parent[path[-1]][0])
    path.reverse()
    actions.reverse()
    return path , actions

welcome='''please enter your primary state like below
3 2 2 , 2g 1g , 2y 1y , 2r 1r :\n'''
inp = input(welcome).split(',')
s0 = []
for col in inp:
    s0.append(col.strip().split())
s0[0] = [int(x) for x in s0[0]]

# variables
levels = [1]
growing = []

# each state is one node, frontier is a FIFO queue
k,m,n = s0[0]
target = check([s0[1:]])
if target:
    print("Primary state is Final state: ",target," the depth is:",1)
else:
    frontier.put(s0[1:])
    while (not frontier.empty()):
        s_now = frontier.get()
        explored.append(s_now)
        ss_nextlevel = generator(s_now)
        growing.append(len(ss_nextlevel))
        if (len(growing) == levels[-1]):
            levels.append(sum(growing))
            growing = []
        target = check(ss_nextlevel)
        if target:
            path , actions = backtrace(parent,explored[0],target)
            print("The nodes in the path:\n",path)
            print("These are the actions:\n",actions)
            print("Target in bfs: ",target," The Depth is:",len(levels))
            print("Explored Nodes: ",len(explored))
            print("Frontier Nodes: ",frontier.qsize())
            break
        else:
            for i in ss_nextlevel:
                frontier.put(i)
    if (frontier.empty()):
        print("It has no solution")

