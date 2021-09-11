import itertools

# global variables
parent={}
frontier=[]
explored=[]
k=m=n=l0=0
target=0

def generator(s):
    next_states=[]
    for i in range(len(s)):
        if s[i]:
            for j in range(len(s)):
                s_mid = [list(x[:]) for x in s]
                if i != j:
                    if s[j]:
                        if (s_mid[i][-1][0] < s_mid[j][-1][0]):
                            s_mid[j].append(s_mid[i][-1])
                            s_mid[i].pop()
                            s_mid = tuple(tuple(x) for x in s_mid)
                            if s_mid not in frontier and s_mid not in explored:
                                parent[s_mid] = [s,f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                                next_states.append(s_mid)
                    else:
                        s_mid[j].append(s_mid[i][-1])
                        s_mid[i].pop()
                        s_mid = tuple(tuple(x) for x in s_mid)
                        if s_mid not in frontier and s_mid not in explored:
                            parent[s_mid] = [s,f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                            next_states.append(s_mid)                       
    return next_states

def check(state):
    for i,column in enumerate(state):
        if column:
            color = state[i][0][1]
            lst = tuple(f"{x}{color}" for x in range(n,0,-1))
            if column != lst:
                return False
    return state

def backtrace(parent, start, end):
    path = [end]
    actions = []
    while path[-1] != start:
        actions.append(parent[path[-1]][1])
        path.append(parent[path[-1]][0])
    path.reverse()
    actions.reverse()
    return path , actions

def recDLS(state,limit,depth):
    target=check(state)
    if target:
        path , actions = backtrace(parent,s0,target)
        print("The path is :\n",path)
        print("The actions are :\n",actions)
        print(f"The depth is {depth+1}")
        print("Explored Nodes in last depth: ",len(explored))
        print("Frontier Nodes in last depth: ",len(frontier))
        return target
    elif limit==0:
        print("cutoff occured")
        return False
    elif not frontier:
        print("no solution")
        return False
    else:
        st=frontier.pop()
        explored.append(st)
        ss_nextlevel = generator(st)
        for s in ss_nextlevel:
            frontier.append(s)
        for s in reversed(ss_nextlevel):
            outcome = recDLS(s,limit-1,depth+1)
            if outcome:
                return outcome
    return False


def IDS(initialState,initialLimit):
    for limit in itertools.count(start=l0):
        parent.clear()
        explored.clear()
        frontier.clear()
        frontier.append(initialState)
        depth=0
        result = recDLS(initialState,limit,depth)
        if result:
            return result
    return False

welcome='''please enter your primary state like below
3 2 2 , 2g 1g , 2y 1y , 2r 1r\n'''
inp = input(welcome).split(',')
s0 = []
for col in inp:
    s0.append(col.strip().split())
s0[0] = [int(x) for x in s0[0]]
l0 = int(input("Enetr your primary limit to start "))

k,m,n = s0[0]
s0=tuple(tuple(x) for x in s0)[1:]

result = IDS(s0,l0)