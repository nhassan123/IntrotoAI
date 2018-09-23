<!DOCTYPE html>
<!-- saved from url=(0165)https://markus.teach.cs.toronto.edu/csc384-2018-01/en/assignments/2/submissions/download?file_name=heuristics.py&grouping_id=511&id=2&path=%2F&revision_identifier=15 -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>
<pre>'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods
'''

import random
from copy import deepcopy

def ord_dh(csp):
    
    maxnum = -10000
    result = None
    for v in csp.get_all_unasgn_vars():
        if (len(csp.get_cons_with_var(v)) &gt; maxnum):
            maxnum = len(csp.get_cons_with_var(v))
            result = v     

    return result

def ord_mrv(csp):

    minnum = 10000
    result = None
    for v in csp.get_all_unasgn_vars():
        if (v.cur_domain_size() &lt; minnum):
            minnum = v.cur_domain_size()
            result = v 

    return result


def val_lcv(csp, var):
    lcvList= {}
    domain = var.cur_domain
    checkCon = (csp.get_cons_with_var(var))

    for i in domain:
        var.assign(i)
        count = 0

        for con in checkCon:

            for v in con.get_unasgn_vars():
                for m in v.cur_domain():

                    if con.has_support(v,t) == False:
                        count += 1
        var.unassign()
        lcvList[i] = count

    return sorted(lcvList, key = final.get, reverse = False) 


   
</pre>


</body></html>