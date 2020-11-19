'''
Authors:    Yongyang Liu <liuyongyang@gatech.edu>
            
Date:       3 Oct 2020
'''

def BFS_Yes_paths(graph, start, goal): 
    # for each edge, t = 2s, split into 100 piece with 100 nodes, then each small segment, 
    # the length is constant l = v*t = 1*0.02 = 0.2 meter. With unit length, BFS return optimal result
    
    Visited=[start]
    Queue = [(start, [start])]
    
    while Queue:
        (vertex, path) = Queue.pop(0)                            # pop the first - FiFO
        if vertex == goal:
            return path
        else:
            temp = [item for item in graph[vertex].neighbours]
            for i in temp:  # in alphabetical order
                j = i.index
                if Visited.count(j) == 0:                        # not in visited
                    Queue.append((j, path + [j]))
                    Visited.append(j)
    return None

