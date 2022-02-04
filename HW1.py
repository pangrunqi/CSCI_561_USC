import os
from queue import PriorityQueue
import math

           
f = open('input.txt', 'r')
file_content = []
line = f.readline()

while line:   
    file_content.append(line.split())
    line = f.readline() 
f.close() 


move_dic = {
    1: (1, 0 ,0),
    2: (-1, 0, 0),
    3: (0, 1, 0),
    4: (0, -1, 0),
    5: (0, 0, 1),
    6: (0, 0, -1),
    7: (1, 1, 0),
    8: (1, -1, 0),
    9: (-1, 1, 0),
    10: (-1, -1, 0),
    11: (1, 0 ,1),
    12: (1, 0 ,-1),
    13: (-1, 0, 1),
    14: (-1, 0, -1),
    15: (0, 1, 1),
    16: (0, 1, -1),
    17: (0, -1, 1),
    18: (0 , -1, -1),
}

def format_content(contents):
    
    connect = dict()
    for i in range(len(contents)):
        content = contents[i]
        if i == 0:
            algorithm = content[0]
        elif i == 1:
            border = [int(content[0]), int(content[1]), int(content[2])]
        elif i == 2:
            start = ' '.join(content)
        elif i == 3:
            end = ' '.join(content)
        elif i == 4:
            points = int(content[0])
        else:
            k = ' '.join(content[:3])
            v = [int(content[i]) for i in range(3,len(content))]
            connect[k] = v
        
    return algorithm, border, start, end, connect

def string2num(s):
    return [int(num) for num in s.split()]

def BFS(border, start, end, connect):
    
    ans = []

    queue = []
    father = {}
    count = {}
    
    queue.append(start)
    count[start] = 1
    father[start] = [start, '0']
    
    while queue:
        current_node_str = queue.pop(0)
        
        if current_node_str == end:
            path = []
            cost = 0
            begin_node_str = current_node_str
            while begin_node_str!= start:

                cost += int(father[begin_node_str][1])
                path.append(begin_node_str+' '+father[begin_node_str][1])
                begin_node_str = father[begin_node_str][0]

            path.append(' '.join(father[start]))
            ans.append(cost)
            ans.append(len(path))
            ans.append(path[::-1])
            return ans
        
        for move_num in connect[current_node_str]:
            move = move_dic[move_num]
            current_node_num = string2num(current_node_str)
            next_node_num = [move[i]+current_node_num[i] for i in range(len(current_node_num))]
            next_node_str = ' '.join([str(num) for num in next_node_num])
            if next_node_num[0] <= border[0] and next_node_num[1]<= border[1] and next_node_num[2] <= border[2] :
                if next_node_str not in father:
                    father[next_node_str] = [current_node_str,'1']
                    queue.append(next_node_str)
                    count[next_node_str] = count[current_node_str] + 1
        
    return -1
                
def UCS(border, start, end, connect):
    
    ans = []
    
    queue = PriorityQueue()
    father = {}
    count = {}

    father[start] = [start, '0']
    queue.put((0, start))
    
    while not queue.empty():
        
        dis, current_node_str = queue.get()
        
        if current_node_str == end:
            path = []
            cost = 0
            begin_node_str = current_node_str
            while begin_node_str!= start:

                cost += int(father[begin_node_str][1])
                path.append(begin_node_str+' '+father[begin_node_str][1])
                begin_node_str = father[begin_node_str][0]

            path.append(' '.join(father[start]))
            ans.append(cost)
            ans.append(len(path))
            ans.append(path[::-1])
            return ans
            
        for move_num in connect[current_node_str]:
            
            move = move_dic[move_num]
            distance = 10 if move_num <= 6 else 14
            current_node_num = string2num(current_node_str)
            
            next_node_num = [move[i]+current_node_num[i] for i in range(len(current_node_num))]
            next_node_str = ' '.join([str(num) for num in next_node_num])
            
            if next_node_num[0] <= border[0] and next_node_num[1]<= border[1] and next_node_num[2] <= border[2]:
                if next_node_str not in father:
                    
                    father[next_node_str] = [current_node_str, str(distance)]
                    queue.put((distance+dis, next_node_str))
        
    return -1

def E_Dist(A,B):
    return math.sqrt(sum([(a - b)**2 for (a,b) in zip(A,B)]))

def A(border, start, end, connect):
    
    ans = []
    
    queue = PriorityQueue()
    father = {}
    count = {}
    
    father[start] = [start, '0']
    num_end = string2num(end)
    queue.put((E_Dist(string2num(start), num_end), start, 0))
    
    while not queue.empty():
        _, current_node_str, dis = queue.get()
        
        if current_node_str == end:
            path = []
            cost = 0
            begin_node_str = current_node_str
            while begin_node_str!= start:

                cost += int(father[begin_node_str][1])
                path.append(begin_node_str+' '+father[begin_node_str][1])
                begin_node_str = father[begin_node_str][0]

            path.append(' '.join(father[start]))
            ans.append(cost)
            ans.append(len(path))
            ans.append(path[::-1])
            return ans
            
        for move_num in connect[current_node_str]:
            
            move = move_dic[move_num]
            distance = 10 if move_num <= 6 else 14
            current_node_num = string2num(current_node_str)
            
            next_node_num = [move[i]+current_node_num[i] for i in range(len(current_node_num))]
            next_node_str = ' '.join([str(num) for num in next_node_num])
            
            if next_node_num[0] <= border[0] and next_node_num[1]<= border[1] and next_node_num[2] <= border[2]:
                if next_node_str not in father:
                    
                    father[next_node_str] = [current_node_str, str(distance)]
                    queue.put((dis+E_Dist(next_node_num, num_end), next_node_str, dis+distance))

        
    return -1

algorithm, border, start, end, connect = format_content(file_content)



if algorithm == 'BFS':
    final_ans = BFS(border, start, end, connect)
elif algorithm == 'UCS':
    final_ans = UCS(border, start, end, connect)
elif algorithm == 'A*':
    final_ans = A(border, start, end, connect)

if final_ans == -1:
    with open('output.txt', 'w') as f:
        f.write('FAIL')
else:
    with open('output.txt', 'w') as f:
        f.write(str(final_ans[0])+'\n')
        f.write(str(final_ans[1])+'\n')
        for p in final_ans[2]:
            f.write(p+'\n')
