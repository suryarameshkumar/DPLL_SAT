# DPLL_SAT

To Run 

python3 dpll_project.py --input_file input.cnf 

To change Heuristics 

Change 'selected_literal' in dpll_project.py

  selected_literal = maxo_dpll(cnf)
  selected_literal = jw_dpll(cnf)
  selected_literal = jw2_dpll(cnf)
  selected_literal = freeman_dpll(cnf) 
