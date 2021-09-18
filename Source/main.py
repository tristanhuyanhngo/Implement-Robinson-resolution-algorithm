import copy
#_________________________________________________________________________________
def ReadFileInput(file_name):
    # Read Alpha
    f = open(file_name, 'r')
    alpha = f.readline().strip()
    # Read KB
    KB = []
    line_text = f.readline().strip()
    
    while (line_text):      # If line_text is empty -> Get out of loop
        KB.append(line_text)
        line_text = f.readline().strip()
        
    f.close()
    
    return KB, alpha

#_________________________________________________________________________________
def WriteFileOutput(file_name, list_resolution, result, clause, alpha, full_clause):
    f = open(file_name, 'w')
    # Alpha
    f.write(alpha)
    f.write('\n')
    
    # Original full Clause
    for i in range(0, len(full_clause)):
        f.write(full_clause[i])
        if (i != len(full_clause) - 1):
            f.write(',')
    f.write('\n')
    
    # Resolution Clause
    for i in list_resolution:
        f.write(i)
        f.write('\n')
    
    # Result
    if result == True:
        temp = 'True ' + clause
    else:
        temp = 'False ' + clause
        
    f.write(temp)
    print("Write result to output.txt successfully ! ")
    f.close()
    
    return 

#_________________________________________________________________________________
# Phu dinh lai mot menh de
def NegateClause(alpha):
    negated_clause = ""
    temp = alpha.split('&')
    
    # Negate the Clause
    for i in range(0,len(temp)):
        if (len(temp[i]) == 1):
            temp[i] = '~' + temp[i]
        else:
            temp[i] = temp[i][1]
            
        # Make Negated Clause
        if (i != len(temp) - 1):
            negated_clause += temp[i] + '|'
        else:
            negated_clause += temp[i]
    
    return negated_clause

#_________________________________________________________________________________
# Check if a clause has Tautology or not
def IsHasTautology(clause):
    list_clause = clause.split('|')
    
    for i in list_clause:
        if len(i) == 1:
            for j in list_clause:
                if len(j) == 2:
                    if j[1] == i[0]:
                        return True
    return False

#_________________________________________________________________________________
def PL_Resolve(C1, C2):
    new_clause = []
    temp_clause = []
    
    # Convert string to list
    list_C1 = C1.split('|')
    list_C2 = C2.split('|')
    
    for i in list_C1:
        for j in list_C2:
            if (i == NegateClause(j)):
                # Find p & ~p then delete 
                temp_C1 = copy.deepcopy(list_C1)
                temp_C2 = copy.deepcopy(list_C2)
                temp_C1.remove(i)
                temp_C2.remove(j)
                
                # Check if i is negative
                if (i[0] == '~'):
                    # Extend -> Add multiple element
                    temp_clause.extend(temp_C2)
                    temp_clause.extend(temp_C1)
                else:
                    temp_clause.extend(temp_C1)
                    temp_clause.extend(temp_C2)     
                
                # Add new clause
                clause = '|'.join(temp_clause)
                new_clause.append(clause)  # Append -> Add one element
    
    return new_clause

#_________________________________________________________________________________
# PL Resolution Algorithm - Another type of Robinson Algorithm
def PL_Resolution(KB, alpha): 
    list_resolution = [] # For output
    clauses = set()
    new = set()
    
    clauses.update(KB)  # Update -> Add multiple element
    clauses.add(alpha)  # Add -> Add one element
    
    while True:
        temp_clauses = list(clauses)
    
        for i in range(0, len(temp_clauses) - 1):
            for j in range(i + 1, len(temp_clauses)):
               
                resolvents = PL_Resolve(temp_clauses[i], temp_clauses[j])
                if len(resolvents) == 0:
                    continue
                
                if resolvents[0] == '':
                    return list_resolution, True, f'{temp_clauses[i]}|{temp_clauses[j]}'
                
                for clause in resolvents:
                    if clause not in new and not IsHasTautology(clause):
                        new.add(clause)
                        clause_resolved = f'{temp_clauses[i]},{temp_clauses[j]}->{clause}'
                        list_resolution.append(clause_resolved)
        
        if new <= clauses:
            return list_resolution, False, ""
        
        clauses.update(new)      
    return
            
#_________________________________________________________________________________
def Main():
    # GET INPUT
    KB, alpha = ReadFileInput('input.txt')
    
    # NEGATE ALPHA
    negated_alpha = NegateClause(alpha)
    
    # RESOLUTION
    list_resolution, result, result_clause = PL_Resolution(KB, negated_alpha)
    
    # OUTPUT
    full_clause = []
    full_clause.extend(KB)
    full_clause.append(negated_alpha)
    WriteFileOutput('output.txt', list_resolution, result, result_clause, alpha, full_clause)
    
    return

if __name__ == "__main__":
    Main()
