<!DOCTYPE html>
<!-- saved from url=(0165)https://markus.teach.cs.toronto.edu/csc384-2018-01/en/assignments/2/submissions/download?file_name=kenken_csp.py&grouping_id=511&id=2&path=%2F&revision_identifier=15 -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>
<pre>import itertools
from cspbase import *
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

def binary_ne_grid(kenken_grid):
    #print(kenken_grid)
    domain = []
    
    dimension = kenken_grid[0][0]

    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)
    
    grid = []
    for i in domain:
        row = []
        for j in domain:
            row.append(Variable('V{}{}'.format(i, j), domain))
        grid.append(row)
    

    cons = []
    for i in range(len(domain)):
        for j in range(len(domain)):
            ## row
            binary_constraints = []

            for k in range(len(grid[i])):
                if( k &lt;= j):
                    continue
                var1 = grid[i][j]
                var2 = grid[i][k]
                con = Constraint("C(V{}{},V{}{})".format(i+1, j+1, i+1, k+1), [var1, var2])
                    
                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if t[0] != t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                binary_constraints.append(con)
            cons.extend(binary_constraints)
            ## col
            binary_constraints = []
            for k in range(len(grid[i])):
                if( k &lt;= i):
                    continue
                var1 = grid[i][j]
                var2 = grid[k][j]        
                con = Constraint("C(V{}{},V{}{})".format(i+1, j+1, k+1, j+1), [var1, var2])
                    
                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if t[0] != t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                binary_constraints.append(con)
            cons.extend(binary_constraints)



    csp = CSP("Kenken")

    # adding variables to csp
    for row in grid:
        for i in row:
            csp.add_var(i)
    
    # adding constraints to csp
    for c in cons:
        csp.add_constraint(c)
    
     

    return csp, grid


def nary_ad_grid(kenken_grid):
    
    domain = []
    grid = list()
    dimension = kenken_grid[0][0]

    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)
    
    vars = []
    for i in domain:
        row = []
        for j in domain:
            row.append(Variable('V{}{}'.format(i, j), domain))
        vars.append(row)
    

    cons = []
    for i in range(len(domain)):
       newCon = Constraint("Narycons{}".format(i+1), vars[i])
       newCon.add_satisfying_tuples(AllDifferent(vars[i], len(domain)))
       cons.append(newCon)

    
    varcol = transposematrix(vars, dimension)
    for j in range(len(domain)):
       newCon = Constraint("Narycons{}".format(j+1),varcol[i])
       newCon.add_satisfying_tuples(AllDifferent(varcol[i], len(domain)))
       cons.append(newCon) 
       

    csp = CSP("Kenken")

    # adding variables to csp
    for row in vars:
        for i in row:
            csp.add_var(i)
    
    # adding constraints to csp
    for c in cons:
        csp.add_constraint(c)
    
     
    return csp, vars

    

def transposematrix(vars, dim):
    col = []
    while i &lt; dim:
        j = 0 
        newCol = [vars[j][i]]
        j += 1
        while j &lt; dim:
            newCol.append(vars[j][i])
            j += 1
        col.append(newCol)
        i += 1
    return col

def AllDifferent(row, dim):
    permute =[]
    for num in range(1, dim +1):
        permute.append(num)
    permutations = itertools.permutations(permute)

    tupleList = []

    for perm in permutations:
        tupleCopy = row[:]
        for p in perm:
            tupleCopy[tupleCopy.index[0]] = p 

        tupleList.append(tupleCopy)
    return tupleList

def kenken_csp_model(kenken_grid):

    kenkencsp, vars = binary_ne_grid(kenken_grid)

    cons = []


    for cage in range(1, len(kenken_grid)):
        if(len(kenken_grid[cage]) &gt; 2):
            operate = kenken_grid[cage][-1]  
            target_num = kenken_grid[cage][-2]
            cageVar = []
            cageVardomain = []
            for cell in range(len(kenken_grid[cage]) - 2):

                i = int(str(kenken_grid[cage][cell])[0]) - 1
                j = int(str(kenken_grid[cage][cell])[1]) - 1
                
                cageVar.append(vars[i][j])
                cageVardomain.append(vars[i][j].domain())
            
            con = Constraint("C(Cage{})".format(cage), cageVar)
            
            sat_tuples = []
            
            for t in itertools.product(*cageVardomain):
               
                if(operate == 0):
                    total = 0
                    for num in t:
                        total += num
                    if (total == target_num):
                        sat_tuples.append(t)
                
                elif(operate == 1):
                    for num in itertools.permutations(t):
                        res = num[0]
                        for n in range(1, len(num)):
                            res -= num[n]
                        if(res == target_num):
                            sat_tuples.append(t)
               
                elif(operate == 2):
                    for num in itertools.permutations(t):
                        res = num[0]
                        for n in range(1, len(num)):
                            res /= num[n]
                        if(res == target_num):
                            sat_tuples.append(t)
                
                elif(operate == 3):
                    total = 1
                    for num in t:
                        total *= num
                    if (total == target_num):
                        sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)
        
        # If a list has two elements, the first element represents a cell,
        # and the second element is the value imposed to that cell.
        else:
            i = int(str(kenken_grid[cage][0])[0]) - 1
            j = int(str(kenken_grid[cage][0])[1]) - 1
            dom = kenken_grid[cage][1]
            vars[i][j] = Variable('V{}{}'.format(i, j), [dom])
    
    for c in cons:
        kenkencsp.add_constraint(c)

    return kenkencsp, vars


</pre>


</body></html>