import subprocess


def main():
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """

    body = """
    import datetime
    # import pandas as pd
    # import numpy as np
    # for row in cur:
    #     if row['quant'] > 10:
    #         _global.append(row)

    phi_operands = {
        "S": [],    # S = list of project attributes for the query output 
        "n": 0,     # N = number of grouping variables 
        "v": [],    # V = list of grouping attributes 
        "F": [],      # F-VECT (list/vector of agg. functions)
        "pred_list": []        # list of predicate variables 
    } 

    # define our schema data in a dictionary - don't need this for the algorithm sake. Just check the values as you go for the algorithms
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

    # ask for input from user and specify data type 
    # read our file to get the phi operands
    op_list = []
    with open('testing.txt', 'r') as file:
        for line in file: 
            op_list.append(line.strip())

    count = 0
    for key in phi_operands:
        # current_value = phi_operands[key]
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
    
    # create our mf structure to store grouping attributes and aggregate functions 
    # use list of grouping attributes (v) and list of aggregate functions (F) to get list of all possible cust combinations 
    
    gA_list = phi_operands.get("v")
    agg_list = phi_operands.get("F")
    # S_list = whole_select.split(", ")

    print(gA_list)
    print(agg_list)

    count_gA = 1
    count_agg = 1
    
    for i in gA_list:
        result = "groupingAttribute{} = {}".format(count_gA, i)
        print(result)
        count_gA += 1
    for i in agg_list: 
        result = "aggregate{} = {}".format(count_agg, i)
        print(result)
        count_agg += 1

    # create a 2d list (for the mf struct) of the grouping attributes and aggregates
    # for the first scan of the sales table, only add the values for the grouping attributes 
    # next scan, use the data from the rest of the row that was added to the mf struct to fill in the aggregates 

    count = 0
    while count != 10000:
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
    
    # print(_global)

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
    n = phi_operands.get("n")

   
    indexes_and_ops = []
    operations = "!<>="
    for i in range(1, n+1):
        defining_cond = pred_dict.get(str(i))
        that_dc = [] #that specific defining condition
        for x in defining_cond:
            if "cust" in x:
                operator = ''.join(filter(lambda b: b in operations, x))
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
        indexes_and_ops.append(that_dc)
        
    print(indexes_and_ops)
    
    def get_only_indexes(index_list): # grab only the indexes from the indexes list 
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

    # helper function to see if we have a duplicate row 
    def lookup(mf_struct, current_row, indexes):  
        g = 0 
        result = False
        # check if the mf_struct is in our cur_row
        if all(x in current_row for x in mf_struct):
            # if so, then check if it's in the correct indexes 
            for i in indexes:
                while g < len(mf_struct):
                    if current_row[i] == mf_struct[g]:
                        g += 1
                        result = True
                    else:
                        result = False
                    break
        return result  

    def get_aggregates(aggregate_list):
        agg_dict = {}
        for agg in aggregate_list:
            agg_dict[agg.split(".")[0].split("(")[1]] = []
            op = str(agg.split(".")[0].split("(")[0])
            attr = agg.split(".")[1].split(")")[0]
            agg_dict[agg.split(".")[0].split("(")[1]].append(op)
            agg_dict[agg.split(".")[0].split("(")[1]].append(attr)
        return agg_dict

    # print(get_aggregates(agg_list))
    
    def the_operand(the_aggs, running_result, new_num):
        if "sum" in the_aggs:
            running_result = running_result+new_num
        elif "min" in the_aggs:
            if new_num < running_result:
                running_result = new_num
        elif "max" in the_aggs:
            if new_num > running_result:
                running_result = new_num
        elif "count" in the_aggs:
            running_result += 1
        return running_result
        

    def get_dups(my_indexes):
        for i in _global: # get the current table we have so far 
            cur.execute("SELECT * FROM sales")
            running_total = 0
            for row in cur: # go thru every row in the database 
                if lookup(i, list(row), my_indexes) == True: 
                    for i in range(1, n+1):
                        aggregates = agg_dict.get(str[i])
                        if "cust" in aggregates:
                            if "avg" in aggregates: 
                                
                            the_operand(aggregates[0], running_total, row[0])
                        if "prod" in aggregates:
                            the_operand(aggregates[0], running_total, row[1])
                        if "day" in aggregates:
                            the_operand(aggregates[0], running_total, row[2])
                        if "month" in aggregates: 
                            the_operand(aggregates[0], running_total, row[3])
                        if "year" in aggregates: 
                            the_operand(aggregates[0], running_total, row[4])
                        if "state" in aggregates: 
                            the_operand(aggregates[0], running_total, row[5])
                        if "quant" in aggregates: 
                            the_operand(aggregates[0], running_total, row[6])
                        if "date" in aggregates:
                            the_operand(aggregates[0], running_total, row[7])
                       # if "avg" in aggregates:
                        

                            
                    
    
    # for cur_index in sole_indexes: # gets the duplicates for each of our defining conditions
    #     get_dups(cur_index)
            
        


                
    # print(_global)

                
           
            

    # for row in cur: 
    #     new_row = list(row)
    #     print(new_row)

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
