# DPLL SAT SOLVER 

from collections import defaultdict
import os
import time
import argparse

#Parse Input in CNF DIMACS Format 

def parse_input(filename):
  clauses = []
  with open(filename, 'r') as input_file:
    for line in input_file:
      if line[0] in ['c', 'p']:
        continue
      literals = list(map(int, line.split()))
      assert literals[-1] == 0
      literals = literals[:-1]
      clauses.append(literals)
  return clauses

# MAXO (Most Often) 
def maxo_dpll(cnf):
  literal_weight = defaultdict(int)
  for clause in cnf:
    for literal in clause:
        if literal in literal_weight:
            literal_weight[literal] += 1
        else:
            literal_weight[literal] = 1
  return max(literal_weight, key=literal_weight.get)
  
# Jersolow-Wang 
def jw_dpll(cnf):
  literal_weight = defaultdict(int)
  for clause in cnf:
    for literal in clause:
      literal_weight[literal] += 2 ** -len(clause)
  return max(literal_weight, key=literal_weight.get)

# Jersolow-Wang 2 
def jw2_dpll(cnf):
  literal_weight = defaultdict(int)
  for clause in cnf:
    for literal in clause:
      literal_weight[abs(literal)] += 2 ** -len(clause)
  return max(literal_weight, key=literal_weight.get)

# Freeman_DPLL
def freeman_dpll(cnf):
    literal_weight = defaultdict(int)
    for clause in cnf:
        for literal in clause:
            if literal in literal_weight:
                if literal > 0:
                    literal_weight[literal] += 1
                else:
                    literal_weight[-literal] += - 1
            else:
                if literal > 0:
                    literal_weight[literal] = 1
                else:
                    literal_weight[-literal] = - 1
    max_p_literal = max(literal_weight, key=literal_weight.get)
    max_n_literal = min(literal_weight, key=literal_weight.get)
    if literal_weight[max_p_literal] >= abs(literal_weight[max_n_literal]):
        return max_p_literal
    return max_n_literal

# Backtracking Function
# Parsed clause is input from user cnf file  
def backtrack(cnf, var_assign):
  # Clause passed to the assignment function 
  cnf, unit_var_assign = assignment(cnf)
  var_assign = var_assign + unit_var_assign
  if cnf == -1:
    return []
  if not cnf:
  	return var_assign
  
  # Pick Heuristic for Branching
 
  #selected_literal = maxo_dpll(cnf)
  #selected_literal = jw_dpll(cnf)
  selected_literal = jw2_dpll(cnf)
  #selected_literal = freeman_dpll(cnf)

  result = backtrack(unit_propagation(cnf, selected_literal), var_assign + [selected_literal])
  # If no solution when assigning to True, try to assign to False
  if not result:
    result = backtrack(unit_propagation(cnf, -selected_literal), var_assign + [-selected_literal])
  return result

# Assignment function


def assignment(cnf):
  # Assignment of values to the variables 
  var_assign = [] 

  # unit_clause - clause with one variable
  unit_clauses = [clause for clause in cnf if len(clause) == 1]

  # for each unit clause 'X' in the formula
  # remove all non-unit clauses containing '-X'
	#	remove all instances of '-X' in every clause

  while unit_clauses:
    unit = unit_clauses[0][0]
    # Propagate the assignment throughout the clause
    cnf = unit_propagation(cnf, unit) 
    var_assign += [unit]
    if cnf == -1:
      return -1, []
    if not cnf:
      return cnf, var_assign
    unit_clauses = [clause for clause in cnf if len(clause) == 1] 
  return cnf, var_assign

# Unit Propagation Function 

# Pure Literal Elimination
# for each variable x
# if literal is pure, remove all clauses containing the literal
# add a unit clause literal

def unit_propagation(cnf, unit):
  cnf_new = []
  for clause in cnf:
    if unit in clause:
      continue
    if -unit in clause:
      new_clause = [literal for literal in clause if literal != -unit]
      if not new_clause:
        return -1
      cnf_new.append(new_clause)
    else:
      cnf_new.append(clause)
  return cnf_new

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  #input the .cnf file after --input_file 
  parser.add_argument('--input_file', default=None,)
  args = parser.parse_args()
  if args.input_file is not None:
    f = args.input_file
    #clauses parsed from input CNF File
    clauses = parse_input(f)
    start_time_dpll = time.time() 
    #clauses passed to the backtrack() function
    assignment = backtrack(clauses, [])
    if assignment:
      print('SATISFIABLE')
      print(assignment)
      end_time_dpll = time.time()
      print('Execution time: %3f seconds' % (end_time_dpll - start_time_dpll))
    else:
      print('UNSATISFIABLE')
  else:
    print('No input cnf file provided')