###############################################################################################
#                                                                                             #
#                 Welcome to Compiler Utility Tools Program                                   #
#                 Author: Adhesh Reghu Kumar (COE18B001)  IIITDM                              #
#                                                                                             #
#  Instructions to Use: The program is evident. However there is a format                     #
#            to enter the productions. Refer to the example here:                             #
#                    A -> A B d | A a                                                         #
#                    A -> c                                                                   #
#                    B -> b | EPSILON                                                         #
#                                                                                             #
#  Note: 1. There must be a space after each symbol or separator in the productions.          #
#        2. Use 'EPSILON' to represent empty string in the production.                        #
#        3. The program doesnt check for validity of grammar.                                 #
#                                                                                             #
#  Features Implemented:                                                                      #
#        1. Check if the grammar contains left recursion for any production.                  #
#        2. Eliminate the left recursions if any.                                             #
#        3. Find the First of each Non Terminal in the given grammar.                         #
#        4. Find the Follow of each Non Terminal in the given grammar.                        #
#                                                                                             #
###############################################################################################

import sys

TERMINALS = []
NON_TERMINALS = []
SYMBOLS = []
START_SYMBOL = ""

PRODUCTIONS = {}
FIRST = {}
FOLLOW ={}

# Define a function that computes the first of a input symbol
def computeFirst(symbol):
    global FIRST, TERMINALS, NON_TERMINALS, PRODUCTIONS

    # stores the first temporarily
    local_first = []

    if(symbol in TERMINALS):
        # Cond-1: First(terminal) = {terminal}
        local_first.append(symbol)
    else:
        # Cond-2: First(Y1 Y2 ... | EPSILON)
        RHS = PRODUCTIONS[symbol]
        for elem in RHS:
            if elem == ['EPSILON']:
                # Case: X -> EPSILON; First(X) == {EPSILON}
                local_first.append(elem[0])
            else:
                # Case: X -> Y1 Y2 ...;
                for item in elem:
                    if item not in FIRST.keys():
                        computeFirst(item)

                    first_item = FIRST[item].copy()
                    if 'EPSILON' not in first_item:
                        # Case : First(Y1) doesnt contain EPSILON; First(X) += {First(Y1)}
                        local_first.extend(first_item)
                        break
                    else:
                        # Case: First(Y1) contains EPSILON; First(X) += {First(Y1) - EPSILON} + First(Y2 Y3 ...)
                        if elem.index(item) != len(item) - 1:
                            first_item.remove('EPSILON')
                        local_first.extend(first_item)

    # Finally update the first in the dictionary 
    local_first = list(dict.fromkeys(local_first))
    FIRST[symbol] = local_first

# Define utility function to compute first of a string
def findFirst_list(input_list):

    # stores return value
    local_first = []

    # Iterate through each symbol in the list - Y1 Y2 ...
    for elem in input_list:
        first_elem = FIRST[elem].copy()
        if "EPSILON" not in first_elem:
            # Case: First(Y1) doesnt contain EPSILON; First(Y1 Y2 ..) = First(Y1)
            local_first.extend(first_elem)
            break
        else:
            # Case: First(Y1) doesnt contain EPSILON; First(Y1 Y2 ..) += First(Y1) - EPSILON + FIRST(Y2 Y3 ..)
            if(input_list.index(elem) != len(input_list) - 1):
                first_elem.remove("EPSILON")
            local_first.extend(first_elem)

    # Remove duplicates and return
    local_first = list(dict.fromkeys(local_first))
    return local_first

# Define function to compute follow of input symbol
def computeFollow(symbol):
    global PRODUCTIONS, FIRST, START_SYMBOL
    global FOLLOW

    # stores follow temporarily
    local_follow = []

    # update local follow for start symbol
    if symbol == START_SYMBOL:
        local_follow.append('$')

    # Go through all productions
    for key in PRODUCTIONS.keys():
        prod = PRODUCTIONS[key]
        # For each production go through each LHS
        for elem in prod:
            if symbol in elem:
                indices = [index for index, item in enumerate(elem) if item == symbol]
                # In each LHS go through all occurences of symbol
                for indx in indices:
                    if indx == (len(elem) - 1):
                        # Case: A -> aB; Follow(B) += Follow(A)
                        if key == symbol:
                            # Sub-case: To prevent infinite recursion when A -> aA
                            continue
                        if key not in FOLLOW.keys():
                            computeFollow(key)
                        follow_item = FOLLOW[key].copy()
                        local_follow.extend(follow_item)            
                    else:
                        # Case: A -> aBX
                        local_first = findFirst_list(elem[indx+1:])
                        if "EPSILON" not in local_first:
                            # Sub-case: if First(X) doesnt contain EPSILON; Follow(B) += First(X)
                            local_follow.extend(local_first)
                        else:
                            # Sub-case: if First(X) contains EPSILON; Follow(B) +=  First(X) - EPSILON + FOLLOW(A)
                            local_first.remove('EPSILON')
                            if len(local_first) > 0:
                                local_follow.extend(local_first)
                            if key not in FOLLOW.keys():
                                computeFollow(key)
                            local_follow.extend(FOLLOW[key])
    
    # Remove duplicates
    local_follow = list(dict.fromkeys(local_follow))
    FOLLOW[symbol] = local_follow

# Define function that identifies the keys that have left recursion
def findLeftRecursion():
    global PRODUCTIONS

    prods_with_left_recr = []
    flag = 0

    # Iterate through all productions to test for presence of left recursion
    for key in PRODUCTIONS.keys():
        prod = PRODUCTIONS[key]

        # Iterate through each RHS of the production
        for elem in prod:
            if elem[0] == key:
                prods_with_left_recr.append(key)
                break

    return prods_with_left_recr

# Define a function that given a list of keys' whose production contains left recr, we eliminate and convert them to right recr
def eliminateLeftRecursion(keys_with_left_recur):
    global PRODUCTIONS, TERMINALS, NON_TERMINALS, SYMBOLS

    # Iterate through each key
    for key in keys_with_left_recur:
        prod = PRODUCTIONS[key]

        # Initialize variables to store the alpha and beta values of the grammar; A -> A alpha | beta
        alpha = []
        beta = []

        # Update alpha and beta value
        for elem in prod:
            if elem[0] == key:
                alpha.append(elem[1:])
            else:
                beta.append(elem)

        # Update actual production
        products = []
        new_key = key + "'"
        NON_TERMINALS.append(new_key)
        SYMBOLS.append(new_key)
        for elem in beta:
            elem.append(new_key)
            products.append(elem)
        PRODUCTIONS[key] = products

        # Update new production
        products = []
        for elem in alpha:
            elem.append(new_key)
            products.append(elem)
        products.append(['EPSILON'])
        PRODUCTIONS[new_key] = products

def main():
    global SYMBOLS, TERMINALS, NON_TERMINALS, FIRST, FOLLOW, START_SYMBOL

    # Print welcome message
    print("###############################################################################################")
    print("#                                                                                             #")
    print("#                 Welcome to Compiler Utility Tools Program                                   #")
    print("#                 Author: Adhesh Reghu Kumar (COE18B001)  IIITDM                              #")
    print("#                                                                                             #")
    print("#  Instructions to Use: The program is evident. However there is a format                     #")
    print("#            to enter the productions. Refer to the example here:                             #")
    print("#                    A -> A B d | A a                                                         #")
    print("#                    A -> c                                                                   #")
    print("#                    B -> b | EPSILON                                                         #")
    print("#                                                                                             #")
    print("#  Note: 1. There must be a space after each symbol or separator in the productions.          #")
    print("#        2. Use 'EPSILON' to represent empty string in the production.                        #")
    print("#        3. The program doesnt check for validity of grammar.                                 #")
    print("#                                                                                             #")
    print("#  Features Implemented:                                                                      #")
    print("#        1. Check if the grammar contains left recursion for any production.                  #")
    print("#        2. Eliminate the left recursions if any.                                             #")
    print("#        3. Find the First of each Non Terminal in the given grammar.                         #")
    print("#        4. Find the Follow of each Non Terminal in the given grammar.                        #")
    print("#                                                                                             #")
    print("###############################################################################################")

    # Accept the number of productions
    print("\nEnter the number of productions")
    NUM_PRODS = int(input().strip())

    # Accpet the productions_str
    print("\nEnter the productions")
    production_str = []
    for i in range(0,NUM_PRODS):
        production_str.append(input().strip())

    # print(production_str)
    print("\n[PARSING]\n")

    # Obtain the NT first from the production_str
    for prod in production_str:
        # Split production based on '->'
        prod = prod.split("->")

        # Obtain  the NT
        nt = prod[0].strip()
        if nt not in NON_TERMINALS:
            NON_TERMINALS.append(nt)

        # Update SYMBOLS list
        if nt not in SYMBOLS:
            SYMBOLS.append(nt)

        RHS = prod[1].strip().split('|')
        for elem in RHS:
            SYMBOLS.extend(list(dict.fromkeys(elem.strip().split(" "))))
            SYMBOLS = list(dict.fromkeys(SYMBOLS))

    # Update the TERMINALS list
    for symbol in SYMBOLS:
        if((symbol not in NON_TERMINALS) and (symbol != "EPSILON")):
            if symbol not in TERMINALS:
                TERMINALS.append(symbol) 

    START_SYMBOL = SYMBOLS[0]

    print("%-20s %-25s" %("Symbols:",SYMBOLS))
    print("%-20s %-25s" %("Non Terminals:",NON_TERMINALS))
    print("%-20s %-25s" %("Terminals:",TERMINALS))

    # Build the production dictionary
    for nt in NON_TERMINALS:
        key = nt
        value = []

        for prod in production_str:
            prod = prod.split("->")
            LHS = prod[0].strip()
            
            if(nt != LHS):
                continue
            else:
                RHS = prod[1].strip().split('|')
                for elem in RHS:
                    value.append(elem.strip().split(" "))

        PRODUCTIONS[nt] = value

    # print(PRODUCTIONS)

    # Find left recursion in the productions
    print("\n[TESTING FOR LEFT RECURSION]\n")
    keys_with_left_recur = findLeftRecursion()
    if(len(keys_with_left_recur) > 0):  
        print("Given Grammar CONTAINS Left Recursion\n")
        # print(keys_with_left_recur)

        # If the grammar contains left recursion, let us eliminate them
        print("[ELIMINATING LEFT RECURSIVE PRODUCTIONS]\n")
        eliminateLeftRecursion(keys_with_left_recur)

        # Print the productions
        print("Grammar after eliminating Left Recursion is:")
        for key in PRODUCTIONS.keys():
            prod = PRODUCTIONS[key]
            prod_val = [" ".join(i) for i in prod]
            prod_val = "| ".join(prod_val)
            print(key,"->",prod_val)
        # print(PRODUCTIONS)
    else:
        print("Given Grammar DOES NOT CONTAIN Left Recursion\n")

    # Update the FIRST dict
    print("\n[COMPUTING FIRST]\n")
    for symbol in SYMBOLS:
        if symbol not in FIRST.keys() and symbol != 'EPSILON':
            computeFirst(symbol)
    
    print("%-20s %-25s" %("NON TERMINAL","FIRST"))
    for nt in NON_TERMINALS:
        print("%-20s %-25s" %(nt,FIRST[nt]))

    # Update the FOLLOW dict
    print("\n[COMPUTING FOLLOW]\n")
    for symbol in SYMBOLS:
        if symbol not in FOLLOW.keys() and symbol != 'EPSILON':
            computeFollow(symbol)

    print("%-20s %-25s" %("NON TERMINAL","FOLLOW"))
    for nt in NON_TERMINALS:
        print("%-20s %-25s" %(nt,FOLLOW[nt]))

if __name__ == '__main__':
    main()