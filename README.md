# Comiler-Utilities
This program  

### Features implemented
1. Check if the grammar contains left recursion for any production.                  
2. Eliminate the left recursions if any.                                             
3. Find the First of each Non Terminal in the given grammar.                         
4. Find the Follow of each Non Terminal in the given grammar.

### How to run
``python3 compilerUtils.py``

### Instructions to Use
The program is evident. However there is a format to enter the productions. Refer to the example here:          
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A -> A B d | A a <br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A -> c <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;B -> b | EPSILON <br/>  

---
**NOTE**
1. There must be a space after each symbol or separator in the productions.
2. Use 'EPSILON' to represent empty string in the production.
3. The program doesnt check for validity of grammar.      
---

### Look at the program



--------------------------------------------------------------------------------------------------------

