import subprocess


def main():
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """

    body = """
    import datetime
    
    phi_operands = {
        "S": [],    # S = list of project attributes for the query output 
        "n": 0,     # N = number of grouping variables 
        "v": [],    # V = list of grouping attributes 
        "F": [],      # F-VECT (list/vector of agg. functions)
        "pred_list": []        # list of predicate variables 
    } 

    # define our schema data in a dictionary
    schema = {
        "cust": str,
        "prod": str,
        "day": int,
        "month": int, 
        "year": int, 
        "state": str,
        "quant": int, 
        "date": datetime    
    }

    # read our file to get the phi operands
    op_list = []
    with open('input3.txt', 'r') as file:
        for line in file: 
            op_list.append(line.strip())

    count = 0
    for key in phi_operands: # goes thru the file and puts the inputs into the phi_operands dictioanry
        if key == "S":
            s_list = op_list[count].split(", ")
            phi_operands[key].extend(s_list)
            count += 1
        elif key == "n":
            phi_operands[key] += int(op_list[count])
            count += 1
        elif key == "v":
            if op_list[count].find(",") != -1:
                v_list = op_list[count].split(", ")
                phi_operands[key].extend(v_list)
            else:
                phi_operands[key].append(op_list[count])
            count += 1 
        elif key == "F": 
            f_list = op_list[count].split(", ")
            phi_operands[key].extend(f_list)
            count += 1 
        elif key == "pred_list":
            p_list = op_list[count].split("; ")
            phi_operands[key].extend(p_list)
            count += 1 

    print(phi_operands)
    
    # create lists for our grouping attributes and aggregates 
    gA_list = phi_operands.get("v")
    agg_list = phi_operands.get("F")

    print(gA_list)
    print(agg_list)

    count_gA = 1
    count_agg = 1
    for i in gA_list: # sees what how many and what our grouping attributes are 
        result = "groupingAttribute{} = {}".format(count_gA, i)
        print(result)
        count_gA += 1
    for i in agg_list: 
        result = "aggregate{} = {}".format(count_agg, i)
        print(result)
        count_agg += 1

    count = 0
    while count != 10000: # creates an initial table - mf struct
        for row in cur: 
            stuff = []
            for attrib in gA_list:
                if attrib == "cust":
                    stuff.append(row[0])
                elif attrib == "prod":
                    stuff.append(row[1])
                elif attrib == "day":
                    stuff.append(row[2])
                elif attrib == "month":
                    stuff.append(row[3])
                elif attrib == "year":
                    stuff.append(row[4])
                elif attrib == "state":
                    stuff.append(row[5])
                elif attrib == "quant":
                    stuff.append(row[6])
                elif attrib == "date":
                    stuff.append(row[7])
            if stuff in _global:
                continue
            else:
                _global.append(stuff)     
        count += 1

    # helper function to split predicate list into each defining condition 
    p_list = phi_operands.get("pred_list")
    pred_dict = {}
    def get_predicates(p_list):
        for i in p_list:
            if " and " in i:
                temp_str = i.split(".")[1]
                pred_dict[i.split(".")[0]] = temp_str.split(" and ")
            else:
                pred_dict[i.split(".")[0]] = [i.split(".")[1]]
        print(pred_dict)
        
            
    get_predicates(p_list)
    n = phi_operands.get("n") # assigns the number of grouping variables to n 

    
    # gets the defining conditions and breaks it down into the index of the column we're comparing, the operation, and what we're comparing it to (inputting in a dictionary, outputting a 2D list)
    indexes_and_ops = []
    operations = "<>=" # used to get the operator
    for i in range(1, n+1):
        defining_cond = pred_dict.get(str(i))
        that_dc = [] # that specific defining condition we'll need to append at the end to our indexes_and_ops list 
        for x in defining_cond:
            if "cust" in x:
                operator = ''.join(filter(lambda b: b in operations, x)) # this filter only takes the operator (i.e referencing the operations string)
                that_dc.append(0)
                that_dc.append(operator)
            if "prod" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(1)
                that_dc.append(operator)
            if "day" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(2)
                that_dc.append(operator)
            if "month" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(3)
                that_dc.append(operator)
            if "year" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(4)
                that_dc.append(operator)
            if "state" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(5)
                that_dc.append(operator)
            if "quant" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(6)
                that_dc.append(operator)
            if "date" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
                that_dc.append(7)
                that_dc.append(operator)

            # the defining condition is comparing against itself (e.g. prod=prod, month=month, etc.)
            operator = ''.join(filter(lambda b: b in operations, x))
            if x.split(operator)[0] == x.split(operator)[1]:
                that_dc.append("buff") # append "buff" so later on, when we get our grouping predicates, we know what our table wants to compare with

            # the defining condition is comparing against an int or str (e.g month=1, state='NY', etc.)
            if x.split(operator)[0] != x.split(operator)[1]:
                that_dc.append(x.split(operator)[1])
        indexes_and_ops.append(that_dc)
        
    print(indexes_and_ops)
    
    def get_only_indexes(index_list): # grab only the indexes from the indexes_and_ops list 
        final_indexes = []
        for x in index_list:
            only_indexes = []
            for inner_element in x:
                if isinstance(inner_element, int):
                    only_indexes.append(inner_element)
            final_indexes.append(only_indexes)
        return final_indexes 

    sole_indexes = get_only_indexes(indexes_and_ops)
    print(sole_indexes)

    def get_only_operations(ops_list): # grab only the operations from the indexes_and_ops list 
        final_operations = []
        for x in ops_list:
            only_ops = []
            for inner_element in x:
                if inner_element == "=" or inner_element == ">" or inner_element == "<" or inner_element == "<>" or inner_element == ">=" or inner_element == "<=":
                    only_ops.append(inner_element)
            final_operations.append(only_ops)
        return final_operations

    sole_operations = get_only_operations(indexes_and_ops)
    print(sole_operations) 

    def get_only_specifics(ops_list): # grab only what we're comparing to the indexes
        final_specs= []
        for x in ops_list:
            only_specs = []
            for inner_element in x:
                if isinstance(inner_element, str):
                    if inner_element != "=" and inner_element != ">" and inner_element != "<" and inner_element != "<>" and inner_element != ">=" and inner_element != "<=":
                        if inner_element.isdigit(): # if the element is a digit but in string format, cast it into an int before appending
                            only_specs.append(int(inner_element))
                        else:
                            only_specs.append(inner_element)
            final_specs.append(only_specs)
        return final_specs 

    sole_specs = get_only_specifics(indexes_and_ops)
    print(sole_specs) 

    # helper function to see if we have a duplicate row 
    def lookup(mf_struct, current_row, indexes, operations, specifics):  
        result = False
        if len(mf_struct) == len(indexes): 
            if all(x in current_row for x in mf_struct): # check if the mf_struct is in our current_row
                for g in range(len(operations)): # i.e g=1
                    small_index = indexes[g] # i.e 3
                    small_ops = operations[g] # i.e <
                    small_specs = specifics[g] # i.e NY or buff
                    if small_ops == "=":
                        if small_specs == "buff": # this means there's no specifics when comparing just this: i.e. prod=prod, month=month
                            if current_row[small_index] == mf_struct[g]: # this is a duplicate!
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<":
                        if small_specs == "buff":
                            if current_row[small_index] < mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == ">":
                        if small_specs == "buff":
                            if current_row[small_index] >mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<>":
                        if small_specs == "buff":
                            if current_row[small_index] != mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == ">=":
                        if small_specs == "buff":
                            if current_row[small_index] >= mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<=":
                        if small_specs == "buff":
                            if current_row[small_index] <= mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
        if len(mf_struct) > len(indexes): # when our indexes list is shorter than our mf_struct 
            if any(x in current_row for x in mf_struct): # at least one the elements in our mf struct is in our current row
                # if so, then check if it's in the correct indexes
                for g in range(len(operations)): 
                    small_index = indexes[g] # i.e 3
                    small_ops = operations[g] # i.e <
                    small_specs = specifics[g] # i.e NY or buff
                    if small_ops == "=":
                        if small_specs == "buff": # this means there's no specifics when comparing just this: i.e. prod=prod, month=month
                            if current_row[small_index] == mf_struct[g]: # this is a duplicate!
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<":
                        if small_specs == "buff":
                            if current_row[small_index] < mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == ">":
                        if small_specs == "buff":
                            if current_row[small_index] >mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<>":
                        if small_specs == "buff":
                            if current_row[small_index] != mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == ">=":
                        if small_specs == "buff":
                            if current_row[small_index] >= mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<=":
                        if small_specs == "buff":
                            if current_row[small_index] <= mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
        if len(mf_struct) < len(indexes): # when our indexes list is longer than our mf_struct
            if all(x in current_row for x in mf_struct):
                # if so, then check if it's in the correct indexes 
                for g in range(len(operations)):
                    small_index = indexes[g] # i.e 3
                    small_ops = operations[g] # i.e <
                    small_specs = specifics[g] # i.e NY or buff
                    if small_ops == "=":
                        if small_specs == "buff": # this means there's no specifics when comparing just this: i.e. prod=prod, month=month
                            if current_row[small_index] == mf_struct[g]: # this is a duplicate!
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] == small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<":
                        if small_specs == "buff":
                            if current_row[small_index] < mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] < small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == ">":
                        if small_specs == "buff":
                            if current_row[small_index] >mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] > small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<>":
                        if small_specs == "buff":
                            if current_row[small_index] != mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] != small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == ">=":
                        if small_specs == "buff":
                            if current_row[small_index] >= mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] >= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                    if small_ops == "<=":
                        if small_specs == "buff":
                            if current_row[small_index] <= mf_struct[g]: 
                                result = True
                            else:
                                result = False
                        else:
                            if "cust" in gA_list:
                                if current_row[g] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "prod" in gA_list:
                                if current_row[g+1] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "day" in gA_list:
                                if current_row[g+2] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "month" in gA_list:
                                if current_row[g+3] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "year" in gA_list:
                                if current_row[g+4] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "state" in gA_list:
                                if current_row[g+5] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "quant" in gA_list:
                                if current_row[g+6] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
                            if "date" in gA_list:
                                if current_row[g+7] == mf_struct[g] and current_row[small_index] <= small_specs: # there's a specific one we have to compare i.e. month=1
                                    result = True
                                else:
                                    result = False
        return result 
    
    def get_aggregates(aggregate_list): # grab the aggregates, put in a dictionary, then use the dictionary so we can access the aggregates easier (i.e. for our get_dups function)
        agg_dict = {}
        for agg in aggregate_list:
            agg_dict[agg.split(".")[0].split("(")[1]] = []
            op = str(agg.split(".")[0].split("(")[0])
            attr = agg.split(".")[1].split(")")[0]
            agg_dict[agg.split(".")[0].split("(")[1]].append(op)
            agg_dict[agg.split(".")[0].split("(")[1]].append(attr)
        return agg_dict

    def the_operand(the_aggs, running_result, new_num): # do the aggerate's operand to keep track (i.e. the new min, max, sum)
        if "sum" == the_aggs:
            running_result = running_result+new_num
        elif "min" == the_aggs:
            if running_result == 0:
                running_result = new_num
            if new_num < running_result:
                running_result = new_num
        elif "max" == the_aggs:
            if new_num > running_result:
                running_result = new_num
        elif "count" == the_aggs:
            running_result += 1
        return running_result
        

    agg_dict = get_aggregates(agg_list)
    print(agg_dict)


    def get_dups(my_indexes, my_ops, my_specs, my_key): # find the rows that match the grouping attributes
        for i in _global: # get the current table we have so far 
            
            cur.execute("SELECT * FROM sales")
            rows = cur.fetchall()

            running_sum = 0 # for average aggregate
            running_count = 0 # for average aggregate
            running_total = 0
            decider = False
            aggregates = agg_dict.get(str(my_key))
            
            for row in rows: # go through every row in the database 
                if lookup(i, list(row), my_indexes, my_ops, my_specs): 
                    if "cust" in aggregates:
                        temp_total = the_operand(aggregates[0], running_total, row[0])
                        running_total = temp_total
                    if "prod" in aggregates:
                        temp_total = the_operand(aggregates[0], running_total, row[1])
                        running_total = temp_total
                    if "day" in aggregates:
                        temp_total = the_operand(aggregates[0], running_total, row[2])
                        running_total = temp_total
                    if "month" in aggregates: 
                        temp_total = the_operand(aggregates[0], running_total, row[3])
                        running_total = temp_total
                    if "year" in aggregates: 
                        temp_total = the_operand(aggregates[0], running_total, row[4])
                        running_total = temp_total
                    if "state" in aggregates: 
                        temp_total = the_operand(aggregates[0], running_total, row[5])
                        running_total = temp_total
                    if "quant" in aggregates:
                        if "avg" in aggregates:
                            temp_sum = the_operand("sum", running_sum, row[6])
                            running_sum = temp_sum 

                            temp_count = the_operand("count", running_count, row[6])
                            running_count = temp_count

                            running_total = running_sum/running_count
                        elif "count" in aggregates:
                            temp_count = the_operand("count", running_count, row[6])
                            running_count = temp_count
                            running_total = running_count
                        else: 
                            temp_total = the_operand(aggregates[0], running_total, row[6])
                            running_total = temp_total 
                    if "date" in aggregates:
                        temp_total = the_operand(aggregates[0], running_total, row[7])
                        running_total = temp_total 
                    
                    decider = True
            
            if decider == True: # if the row is a duplicate, append the result of the aggregate into our new table (mf_struct)
                i.append(running_total)

                              
    for i in range(len(sole_indexes)):  # Use the length of the list to get the duplicates for each of our defining conditions
        cur_index = sole_indexes[i]
        cur_op = sole_operations[i]
        cur_spec = sole_specs[i]
        k = i + 1
        test_num = get_dups(cur_index, cur_op, cur_spec, k)   

    """

    # Note: The f allows formatting with variables.
    #       Also, note the indentation is preserved.
    tmp = f"""
import os
import psycopg2
import psycopg2.extras
import tabulate
from dotenv import load_dotenv

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

def query():
    load_dotenv()

    # user = os.getenv('USER')
    # password = os.getenv('PASSWORD')
    # dbname = os.getenv('DBNAME')

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="Win.yu25")
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    
    _global = []
    {body}
    
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    """

    # Write the generated code to a file
    open("_generated.py", "w").write(tmp)
    # Execute the generated code
    subprocess.run(["python", "_generated.py"])


if "__main__" == __name__:
    main()
