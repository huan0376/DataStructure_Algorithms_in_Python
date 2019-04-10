
import pandas as pd
import numpy as np
import array


df = pd.read_csv('***/data_Problem2.csv')
df.head()




print(df.shape)
print(df.dtypes)
# check whether the dataset contains the missing values. 
index = df[df.isnull()['FROM_NODE'] == True]
print(index)
# drop the missing values. 
df = df.dropna()



# Ignore the node that in FROM_NODE but not in NOT_NODE. 
from_list_temp, to_list = set(df['FROM_NODE']), set(df['TO_NODE'])
from_list = set([int(x) for x in from_list_temp])
need_node = (from_list & to_list)
need_node_float = set([float(x) for x in need_node])
df = df[(df['FROM_NODE'].isin(need_node_float)) & (df['TO_NODE'].isin(need_node))]



df = df.sort_values(by=['FROM_NODE'])
df = df.reset_index()
n, m = df.shape
df.head()



# Build a directed graph using dictionary data structure. 
dict_node = {}
from_node = df['FROM_NODE']
to_node = df['TO_NODE']
for i in range(n):
    key = int(from_node[i])
    if key not in dict_node:
        dict_node[key] = set()
    if to_node[i] not in dict_node[key]:
            dict_node[key].add(to_node[i])
print(dict_node)
for key in dict_node:
    list_values = dict_node[key]
    temp = []
    for value in list_values:
        if value in dict_node:
            temp.append(value)
    dict_node[key] = temp

print(dict_node)
            

# define the bfs function to search for the maximal accumulate values and corresponding cycle. 

def bfs(search_key, key, visited, path, weight, max_weight, cycle_path):
    
    if key not in dict_node or len(dict_node[key]) <1:        
        return max_weight, cycle_path

    for value in dict_node[key]:
        #print(key, value)

        path.append(value)
        temp_weight = df[(df['FROM_NODE'] == key) & (df['TO_NODE'] == value)]['VALUE'].iloc[0]
        weight += temp_weight
        if value == search_key:
            re_path = path
            re_weight = weight
            #print('Found the path: ', path, weight)
            
            node1 = path.pop()
            weight -= temp_weight
            node2 = path.pop()    
            try: 
                weight -= df[(df['FROM_NODE'] == path[-1]) & (df['TO_NODE'] == key)]['VALUE'].iloc[0]
            except:
                print('')
                
            visited.pop()
            return re_weight, re_path+[node2, node1]
        elif value in visited:
            path.pop()
            weight -= temp_weight
            continue
        else: 
            visited.append(value)
            pre_weight, pre_path = bfs(search_key, value, visited, path, weight, max_weight, cycle_path)
            #print(pre_weight, pre_path)
            if pre_weight > max_weight:
                max_weight = pre_weight
                cycle_path = pre_path
        
    return max_weight, cycle_path
            


# search for the cycles. 
search_cycle = {}
max_cycle_weight = 0
max_cycle_path = []
#for key in dict_node:
for key in dict_node:    
    path = list()
    path.append(key)
    weight = 0
    visited = list()
    visited.append(key)  
    cycle_path = list()
    search_cycle[key] = bfs(key, key, visited, path, weight, weight, cycle_path)
    if search_cycle[key][0] > max_cycle_weight: 
        max_cycle_weight = search_cycle[key][0]
        max_cycle_path = search_cycle[key][1]
    
#print(search_cycle)
print('The maximal accumulated transaction value: ', max_cycle_weight)
print('The cycle that has the max accumulated transaction value: ', max_cycle_path)

