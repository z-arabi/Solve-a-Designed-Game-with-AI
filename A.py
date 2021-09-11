# global variables
parent={}
frontier={}
explored={}
k=m=n=0
target=0

def Cost(state):
    c = 0
    for i,column in enumerate(state):
        if column:
            color = state[i][0][1]
            lst = [f"{x}{color}" for x in range(n,0,-1)]
            for ind in range(len(column)):
                c += abs(-(ind-n+int(column[ind][0])))*1
                if ind<n:
                    if column[ind]==lst[ind]:
                        c -= 1
                    else:
                        c += 1
    return c


def generator(s,depth):
    next_states={}
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
                            cost = Cost(s_mid)
                            depth_child = depth+1
                            his = cost+depth_child
                            if s_mid not in frontier and s_mid not in explored:
                                parent[s_mid] = [s,f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                                next_states[s_mid]=(cost,depth_child,his)
                            elif s_mid in frontier:
                                target = check(s_mid)
                                if target and frontier[s_mid][2] > his:
                                    frontier.pop(s_mid)
                                    frontier[s_mid]=(cost,depth_child,his)
                                    parent[s_mid] = [s,f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                                    next_states[s_mid]=(cost,depth_child,his)
                    else:
                        s_mid[j].append(s_mid[i][-1])
                        s_mid[i].pop()
                        s_mid = tuple(tuple(x) for x in s_mid)
                        cost = Cost(s_mid)
                        depth_child = depth+1
                        his = cost+depth_child
                        if s_mid not in frontier and s_mid not in explored:
                            parent[s_mid] = [s,f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                            next_states[s_mid]=(cost,depth_child,his)
                        elif s_mid in frontier:
                            target = check(s_mid)
                            if target and frontier[s_mid][2] > his:
                                frontier.pop(s_mid)
                                frontier[s_mid]=(cost,depth_child,his)
                                parent[s_mid] = [s,f"move {s_mid[j][-1]} from col {i+1} to col {j+1}"]
                                next_states[s_mid]=(cost,depth_child,his)                     
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

welcome='''please enter your primary state like below
3 2 2 , 2g 1g , 2y 1y , 2r 1r\n'''
inp = input(welcome).split(',')
s0 = []
for col in inp:
    s0.append(col.strip().split())
s0[0] = [int(x) for x in s0[0]]

k,m,n = s0[0]
s0=tuple(tuple(x) for x in s0)[1:]

min=Cost(s0)
c,d,h=0,0,0
s_now = s0

target=check(s0)
if target:
    print("Primary state is Final state: ",target," the depth is:",1)
else:
    c,d,h = Cost(s0),0,Cost(s0)
    frontier[s0]=(c,d,h)
    explored={}
    while frontier:
        ss_nextlevel = generator(s_now,d)
        for k,v in ss_nextlevel.items():
            frontier[k]=v
        frontier.pop(s_now)
        explored[s_now]=(c,d,h)
        min = 100000
        for k,v in frontier.items():
            if abs(min)>abs(v[2]):
                min=v[2]
                s_now = k
                c,d,h = v
        target = check(s_now)
        if target:
            path , actions = backtrace(parent,s0,target)
            print("the path is:\n",path)
            print("the actions are:\n",actions)
            print("Final state: ",target," the depth is:",d)
            print("Explored Nodes: ",len(explored))
            print("Frontier Nodes: ",len(frontier))
            break
    print("End while")
