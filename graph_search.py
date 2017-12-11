# from copy import copy, deepcopy
import queue
inputpath="input.txt"
outputpath="output.txt"

n=0
p=0
lizard_count=1
algorithm="DFS"
matrix = None
tree_count=0
tree_dictionary={}
lizard_list=[]
new_lizard_list=[]

#********MAIN FUNCTION CALL TO OTHER ALGORITHMS**********#

def solve(inputpath):
    global algorithm
    global n
    global p
    global tree_count
    global matrix
    
    global tree_dictionary
    
    file_object=open(inputpath,'r')
    lines=file_object.read()
    input_data=lines.split("\n")
    
    algorithm=input_data[0]
    n=int(input_data[1])
    p=int(input_data[2])
    matrix = [[0 for x in range(0,n)] for y in range(0,n)] 
    tree_count=0
    
    #read data into matrix
    for i in range(0,n):
        for j in range(0,n):
            matrix[i][j]=int(input_data[i+3][j])
            if(matrix[i][j]==2):
                tree_count+=1
                if(algorithm=="BFS"):
                    if(i in list(tree_dictionary.keys())):
                        col_list=tree_dictionary[i]
                    else:
                        col_list=[]
                        
                    col_list.append(j)
                    tree_dictionary.update({i:col_list})
    file_object.close()
    if(case_avoid_algorithm()==False):
        #no case exists to avoid running search algorithm=> run the algorithm
        if(algorithm=="DFS" and tree_count==0):
            if(dfs_no_tree(0,matrix)==False):
                write_output("FAIL")
        elif(algorithm=="DFS" and tree_count>0):
            if(dfs_tree(0,0,matrix)==False):
                write_output("FAIL")
        elif(algorithm=="BFS"):
            if(bfs()==False): #pass list traversed points
                write_output("FAIL")
        elif(algorithm=="SA"):
            if(dfs_tree(0,0,matrix)==False):
                write_output("FAIL")
    else:
        write_output("FAIL")

#**********FILE WRITE**********#
      
def write_output(message):
    file_object=open(outputpath,'w')
    file_object.write(message)
    file_object.close()

#**********CHECKING CORNER CASES**********#

def case_avoid_algorithm():
    if(p==0):
        return True
    elif(n==0):
        return True
    elif(n==2):
        return True
    elif(p==n^2):
        return True
    elif(tree_count==(n**n)):
        return True
    elif(p+tree_count>(n**n)):
        return True
    elif(tree_count==0 and p>n):
        return True
    else:
        return False

#**********PRINT MATRIX TO FILE**********#

def print_solution(matrix=[[]]):
    temp=""
    message=""
    for i in range(n):
        for j in range(n):
            temp+=str(matrix[i][j])
        if(i<n-1):
            temp+="\n"
    message+=temp
    #print(message)
    message="OK\n"+message
    write_output(message)    

#********DEPTH FIRST SEARCH ALGORITHM WITH NO TREES********#

def dfs_no_tree(col,matrix=[[]]):
    global lizard_count
    if(lizard_count>p):
        print_solution(matrix)
        #print()
        return True
    elif(col>=n and lizard_count<p):
        return False
    for row in range(0,n):
        if(dfs_check_validity_no_tree(row,col,matrix)==True):
                #if valid then place lizard
                matrix[row][col]=1
                lizard_count+=1
                #check next column to place next lizard
                if(dfs_no_tree(col+1,matrix)==True):
                    return True
                #if placing lizard in this cell doesn't produce a valid solution
                matrix[row][col]=0
                lizard_count-=1
    #if the lizard cannot be placed in any cell in this column           
    return False

def dfs_check_validity_no_tree(row,column,matrix=[[]]):
    #check row
        for i in range(column):
            if(matrix[row][i]==1):
                return False
    #check diagonals
        for i in range(1,n):
            if((row-i)>=0 and (column-i)>=0):
                if(matrix[row-i][column-i]==1):
                    return False
            if((row+i)<n and (column-i)>=0):
                if(matrix[row+i][column-i]==1):
                    return False
        return True
        
#********DEPTH FIRST SEARCH ALGORITHM WITH TREES********#

def dfs_tree(row,col,matrix=[[]]):
    global lizard_count
    if(lizard_count>p):
        print_solution(matrix)
        #print()
        return True
    elif(col>=n and lizard_count<p):
        return False
    if(row>=n and col<(n-1)):
        col+=1
        row=0
    elif(row>=n and col>=(n-1)):
        return False
    for row_count in range(row,n):
        if(dfs_check_validity_tree(row_count,col,matrix)==True):
                #if valid then place lizard
                matrix[row_count][col]=1
                lizard_count+=1
                #check next column to place next lizard
                if(dfs_tree(row_count+1,col,matrix)==True):
                    return True
                #if placing lizard in this cell doesn't produce a valid solution
                matrix[row_count][col]=0
                lizard_count-=1
        else:
            if(dfs_tree(row+1,col,matrix)==True):
                    return True
            else:
                return False
    #if the lizard cannot be placed in any cell in this column           
    return False

def dfs_check_validity_tree(row,col,matrix=[[]]):
    #check if position is a tree
    if(matrix[row][col]==2):
            return False
    #check cells in the row, left of this cell
    for i in range(col):
        if(matrix[row][col-i-1]==1):
            return False
        elif(matrix[row][col-i-1]==2):
            condition="true"
            break
    #check cells above the cells in this column
    for i in range(row):
        if(matrix[row-i-1][col]==1):
            return False
        elif(matrix[row-i-1][col]==2):
            condition="true"
            break
    #check north-west diagonal
    for i in range(1,n):
        if((row-i)>=0 and (col-i)>=0):
            if(matrix[row-i][col-i]==1):
                return False
            if(matrix[row-i][col-i]==2):
                condition="true"
                break
    #check south-west diagonal
    for i in range(1,n):   
        if((row+i)<n and (col-i)>=0):
            if(matrix[row+i][col-i]==1):
                return False
            if(matrix[row+i][col-i]==2):
                condition="true"
                break
    return True

#********BREADTH FIRST SEARCH ALGORIHTM**********#

def bfs_check_validity(row,col,state={}):
    matrix = [[0 for x in range(0,n)] for y in range(0,n)] 
    for k,v in tree_dictionary.items():
        for s in v:
            #if this cell contains a tree
            if(k==row and s==col):
                return False
            matrix[k][s]=2
    #populate lizards in matrix
    for k,v in state.items():
        for s in v:
            #if this cell contains a lizard
            if(k==row and s==col):
                return False
            matrix[k][s]=1
    #print()
    #print_solution(matrix)
    #print()
    #check cells in the row,left of this cell
    for i in range(1,n):
        if((col-i)>=0):
            if(matrix[row][col-i]==1):
                return False
            elif(matrix[row][col-i]==2):
                condition="true"
                break
    #check cells above the cells in this column
    for i in range(1,n):
        if((row-i)>=0):
            if(matrix[row-i][col]==1):
                return False
            elif(matrix[row-i][col]==2):
                condition="true"
                break
    #check cells in the row,right of this cell
    for i in range(1,n):
        if((col+i)<n):
            if(matrix[row][col+i]==1):
                return False
            elif(matrix[row][col+i]==2):
                condition="true"
                break
    #check cells below the cells in this column
    for i in range(1,n):
        if((row+i)<n):
            if(matrix[row+i][col]==1):
                return False
            elif(matrix[row+i][col]==2):
                condition="true"
                break
    #check north-west diagonal
    for i in range(1,n):
        if((row-i)>=0 and (col-i)>=0):
            if(matrix[row-i][col-i]==1):
                return False
            if(matrix[row-i][col-i]==2):
                condition="true"
                break
    #check south-west diagonal
    for i in range(1,n):   
        if((row+i)<n and (col-i)>=0):
            if(matrix[row+i][col-i]==1):
                return False
            if(matrix[row+i][col-i]==2):
                condition="true"
                break
    #check north-east diagonal
    for i in range(1,n):
        if((row-i)>=0 and (col+i)<n):
            if(matrix[row-i][col+i]==1):
                return False
            if(matrix[row-i][col+i]==2):
                condition="true"
                break
    #check south-east diagonal
    for i in range(1,n):   
        if((row+i)<n and (col+i)<0):
            if(matrix[row+i][col+i]==1):
                return False
            if(matrix[row+i][col+i]==2):
                condition="true"
                break   
    return True

def populate_bfs_matrix(state={}):
    matrix
    for i in range(n):
        for j in range(n):
            if(bool(state)==True):#not empty
                if(i in state.keys()):
                    if(j in state[i]):
                        matrix[i][j]=1
                        continue
            
            if(bool(tree_dictionary)==True):#not empty
                    if(i in tree_dictionary.keys()):
                        if(j in tree_dictionary[i]):
                            matrix[i][j]=2
                            continue
            matrix[i][j]=0
    print_solution(matrix)

def checkKeyValuePairExistence(key, value, dictionary={}):
    try:
        return value in dictionary[key]
    except KeyError:
        return False

def bfs():
    lizard_count = 0 
    row=0
    col=0
    start_time=time.time()
    #declare queue
    bfs_queue=queue.Queue()
    #initialize queue with root node which is empty 
    dictionary={-1:[-1]} #root node when none of the lizards are placed
    bfs_queue.put(dictionary)#push root node into queue
    lizard_placed=0# temporary lizard count flag
    #check if queue is empty
    while(time.time()-start_time<290):
        while bfs_queue.empty()==False :
            lizard_place=0#reset lizard count flag
            state=bfs_queue.get()
            if(-1 in state.keys()):
                #root node detected, now generate set of states
                state={}
                
            lizard_count=lizard_count_value(state)+1
            #print(lizard_count)
            
            if(lizard_count>p):
                #all lizards placed
                #print("all lizards placed")
                return True
            
            while lizard_placed == 0 : 
                
                if(col>=n):
                    #print("cannot place all lizards")
                    break
                dictionary={}
                for row in range(n):
                    #print("Deepcopying state to dictionary...")
                    dictionary=copy.deepcopy(state)
                    
                    if row in list(dictionary.keys()):
                        list_col=dictionary[row]
                    else:
                        list_col=[]
                    #position row,col is valid in state dictionary   
                    if(bfs_check_validity(row,col,dictionary)==True): 
                        list_col.append(col)
                        dictionary.update({row:list_col})
                        bfs_queue.put(dictionary)
                        #print("Dictionary: ",dictionary)
                       #print("Row: %s Col: %s"% (row,col))
                        #populate_bfs_matrix(dictionary)
                        #print()
                        lizard_placed=1
                        if(lizard_count==p):
                            populate_bfs_matrix(dictionary)
                            return True
                col+=1
            #print("Dictionary: ",dictionary)

            if(lizard_placed==1):
                lizard_placed=0
                if(lizard_count==p):
                    #print("Dictionary: ",dictionary)
                    populate_bfs_matrix(dictionary)
                    return True
            col=0  #reset column value to check all valid positions for next lizard 
     
    return False
def lizard_count_value(state={}):
    count=0
    for k,v in state.items():
        for s in v:
            count+=1
    return count

#**********SIMULATED ANNEALING ALGORITHM**********#

import math
import random
import copy
temperature=50

def sa(state=[[]]):
    
    start_time=time.time()
    
    global lizard_list
    global new_lizard_list
    
    iteration=0
    prob=1
    
    #print("Start Time: ",start_time)
    #print_solution(state)
    global temperature
    
    current_state=sa_initial_state(state)
    
    #print(lizard_list)
    
    while (time.time()-start_time)<290 :
        copy_current_state=copy.deepcopy(current_state)
        iteration+=1
        #print("Iteration : ",iteration)
        #print_solution(current_state)
        if(number_of_attacks(current_state)==0):
            print()
            print_solution(current_state)
            return True
        
        #print()
        temperature=schedule(temperature,iteration)
        #start_flag=1
        #print("Temperature: ",temperature)
        
        #print("Current State:-")
        #print_solution(current_state)
        number_of_attacks_current_state=number_of_attacks(current_state)
        #print("Current State attacks count= ",number_of_attacks_current_state)
        
        next_state=sa_successor_state(current_state)
        
        #print("Next State:-")
        #print_solution(next_state)
        number_of_attacks_next_state=number_of_attacks(next_state)
        #print("Next State attacks count= ",number_of_attacks_next_state)
        
        """
        print("****Testing Current and Next State Before Delta****")
        print_solution(current_state)
        print()
        #print()
        print_solution(next_state)
        print("****Testing Current and Next State Finished****")
        """
        
        delta_energy=number_of_attacks_next_state-number_of_attacks_current_state
        #print("Delta Energy: ",delta_energy)
        
        """
        print("****Testing Current and Next State Aftre Delta****")
        print_solution(current_state)
        print()
        #print()
        print_solution(next_state)
        print("****Testing Current and Next State Finished****")
        """
        
        if(delta_energy<=0):
            current_state=copy.deepcopy(next_state)
            #print("Accept solution")
            lizard_list=list(new_lizard_list)
            #print_solution(current_state)
        else:
            prob=probability(delta_energy,temperature)
            #print("Probability: ",prob)
            if(acceptance(prob)==True):
                current_state=copy.deepcopy(next_state)
                lizard_list=list(new_lizard_list)
                #print("Accept with probability ",prob)
            else:
                current_state=copy.deepcopy(copy_current_state) #reverting to previous
                """
                print("Copy Current State")
                print_solution(current_state)
                print("Next State")
                print_solution(next_state)
                """
                #print("Reject with probability ",prob)
                continue;
    return False
    
def sa_successor_state(state=[[]]):
    
    global new_lizard_list
    new_lizard_list=list(lizard_list)
    direction_list=["east","south east","south","south west","west","north west","north","north east"]
    location=random.randint(0,p-1)
    #print("Lizard location chosen: ",location)
    lizard_row=new_lizard_list[location][0]
    lizard_column=new_lizard_list[location][1]
    #print("Chose liz row,col : %s,%s" % (lizard_row,lizard_column))
    #move this lizard by one incremental steps in a direction
    
    flag_lizard_placed=0
    for i in range(1,n):
        check_direction=[]
        while(flag_lizard_placed==0):
            
            if(len(check_direction)==8):#all directions have been checked for this position for given i
                break
            direction=random.randint(0,7)
            while(direction in check_direction):
                direction=random.randint(0,7)
                
            #print("Direction move= ",direction_list[direction])
            check_direction.append(direction)
            
            
            if(direction_list[direction]=="south"):
                #print("Enter S")
                if(lizard_row+i<n):
                    #print("Considering position: (%s,%s) state: %s" %(lizard_row+i,lizard_column,state[lizard_row+i][lizard_column]))
                    if(state[lizard_row+i][lizard_column]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row+i][lizard_column]=1
                        state[lizard_row][lizard_column]=0
                        #update new_lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row+i,lizard_column])
                        #print("New Lizard list: ",new_lizard_list)
                        lizard_placed=1
                        return state
                
            elif(direction_list[direction]=="south east"):
                #print("Enter SE")
                if(lizard_row+i<n and lizard_column+i<n):
                    ####print("Considering position: (%s,%s) state: %s" %(lizard_row+i,lizard_column+i,state[lizard_row+i][lizard_column+i]))
                    if(state[lizard_row+i][lizard_column+i]==0):
                        ###print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row+i][lizard_column+i]=1
                        state[lizard_row][lizard_column]=0
                        #update lizard_list
                        ##print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row+i,lizard_column+i])
                        #print("New Lizard list: ",new_lizard_list)
                        lizard_placed=1
                        return state

            elif(direction_list[direction]=="east"):
                #print("Enter E")
                if(lizard_column+i<n):
                    #print("Considering position: (%s,%s) state: %s" %(lizard_row,lizard_column+i,state[lizard_row][lizard_column+i]))
                    if(state[lizard_row][lizard_column+i]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row][lizard_column+i]=1
                        state[lizard_row][lizard_column]=0#
                        #update lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row,lizard_column+i])
                        #print("New Lizard list: ",new_lizard_list)
                        lizard_placed=1
                        return state

            elif(direction_list[direction]=="south west"):
                #print("Enter SW")
                if(lizard_row+i<n and lizard_column-i>=0):
                    #print("Considering position: (%s,%s) state: %s" %((lizard_row+i),(lizard_column-i),state[lizard_row+i][lizard_column-i]))
                    if(state[lizard_row+i][lizard_column-i]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row+i][lizard_column-i]=1
                        state[lizard_row][lizard_column]=0
                        #update lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row+i,lizard_column-i])
                        #print("New Lizard list: ",new_lizard_list)
                        return state

            elif(direction_list[direction]=="north"):
                #print("Enter N")
                if(lizard_row-i>=0):
                    #print("Considering position: (%s,%s) with state: %s" %(lizard_row-i,lizard_column,state[lizard_row-i][lizard_column]))
                    if(state[lizard_row-i][lizard_column]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row-i][lizard_column]=1
                        state[lizard_row][lizard_column]=0
                        #update lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row-i,lizard_column])
                        #print("New Lizard list: ",new_lizard_list)
                        return state

            elif(direction_list[direction]=="north west"):
                #print("Enter NW")
                if(lizard_row-i>=0 and lizard_column-i>=0):
                    #print("Considering position: (%s,%s) state: %s" %(lizard_row-i,lizard_column-i,state[lizard_row-i][lizard_column-i]))
                    if(state[lizard_row-i][lizard_column-i]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row-i][lizard_column-i]=1
                        state[lizard_row][lizard_column]=0
                        #update lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row-i,lizard_column-i])
                        #print("New Lizard list: ",new_lizard_list)
                        return state
                    

            elif(direction_list[direction]=="north east"):
               # print("Enter NE")
                if(lizard_row-i>=0 and lizard_column+i<n):
                    #print("Considering position: (%s,%s) state: %s" %((lizard_row-i),(lizard_column+i),state[lizard_row-i][lizard_column+i]))
                    if(state[lizard_row-i][lizard_column+i]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row-i][lizard_column+i]=1
                        state[lizard_row][lizard_column]=0
                        #update lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row-i,lizard_column+i])
                        #print("New Lizard list: ",new_lizard_list)
                        return state
                    

            elif(direction_list[direction]=="west"):
                #print("Enter W")
                if(lizard_column-i>=0):
                    #print("Considering position: (%s,%s) state: %s" %(lizard_row,lizard_column-i,state[lizard_row][lizard_column-i]))
                    if(state[lizard_row][lizard_column-i]==0):
                        #print("State at this position is empty so move lizard")
                        #move lizard right
                        state[lizard_row][lizard_column-i]=1
                        state[lizard_row][lizard_column]=0
                        #update lizard_list
                        #print("Old lizard list: ",new_lizard_list)
                        new_lizard_list.remove([lizard_row,lizard_column])
                        new_lizard_list.append([lizard_row,lizard_column-i])
                        #print("New Lizard list: ",new_lizard_list)
                        return state
                    
    return state

def number_of_attacks(state=[[]]):
    attack_count=0
    #for each cell in the matrix
    for row in range(n):
        for col in range(n):
            if(state[row][col]==1):
                #print("Lizard in cell (%s,%s)" % (row,col))
                #check cells in the row, right of this cell
                for i in range(1,n-col):
                    if(state[row][col+i]==1):
                        attack_count+=1
                        #print("Attack by (%s,%s)" % (row,col+i))
                        break
                    elif(state[row][col+i]==2):
                        condition="true"
                        break
                #check cells below the cells in this column
                for i in range(1,n-row):
                    if(state[row+i][col]==1):
                        attack_count+=1
                        #print("Attack by (%s,%s)" % (row+i,col))
                        break
                    elif(state[row+i][col]==2):
                        condition="true"
                        break
                #check north-east diagonal
                for i in range(1,n):
                    if((row-i)>=0 and (col+i)<n):
                        if(state[row-i][col+i]==1):
                            attack_count+=1
                            #print("Attack by (%s,%s)" % (row-i,col+i))
                            break
                        if(state[row-i][col+i]==2):
                            condition="true"
                            break
                #check south-east diagonal
                for i in range(1,n):   
                    if((row+i)<n and (col+i)<n):
                        if(state[row+i][col+i]==1):
                            attack_count+=1
                            #print("Attack by (%s,%s)" % (row+i,col+i))
                            break
                        if(state[row+i][col+i]==2):
                            condition="true"
                            break
    #print("Attack count total: ",attack_count)                   
    """
    if(attack_count%2 == 0):
        return attack_count/2
    else:
        return (attack_count+1)/2
    """
    return attack_count
        
def acceptance(prob):
    r=random.random()
    #print("Random Probability : ",r)
    if(r<=prob):
        return True
    else:
        return False
    
def probability(delta,temperature):
    return math.exp(-(delta/temperature))

import math
def schedule(temperature,iteration):
    #return 0.989*temperature
    return n/math.log(iteration+1)
    
def sa_initial_state(state=[[]]):
    #randomly generate initial state
    lizard_count=0
    global lizard_list
    #if lizard count is less than or equal to number of rows/columns then one each can be placed per row/column
    if(tree_count==0):
        while(lizard_count<p):
            for row in range(n):
                for col in range(n):
                    
                    if(lizard_count>=p):
                        return state
                    r=int(n*random.random())
                    #r=row
                    c=col
                    #c=int(n*random.random())
                    if(state[r][c]==0):
                        state[r][c]=1
                        lizard_list.append([r,c])
                        lizard_count+=1
                        #break
    else:
        #print("Tree count: ",tree_count)
        while(lizard_count<p):
            for row in range(n):
                for col in range(n):
                    if(lizard_count>=p):
                        return state
                    r=int(n*random.random())
                    #r=row
                    c=int(n*random.random())
                    if(state[r][c]==0):
                        state[r][c]=1
                        lizard_list.append([r,c])
                        lizard_count+=1
                        #print("(row: %s,col: %s) lizard number: " %(r,c),lizard_count)
    return state       

import time
start=time.time()
solve(inputpath)
end=time.time()
#print(end-start)
