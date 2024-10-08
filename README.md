**SAT Solver**

**Author :** *Sébastien RICHARD*

**Date :** *2024-04-15*

**Description :** *This project is a SAT solver that takes a text file as input and returns a solution if it exists.*

**Utilisation :** *To use this solver, simply run the script `main.py` passing the path of the text file containing the SAT formula as an argument.*

**Example :** `python3 main.py clauses.txt`

**Note :** *The text file must be in the following format : each line is a clause, and each number is a literal and negative literal for non literal.*

**Example :**

    -1 2 3 -5 -4
    -2
    1 2 4
    -2 3
    2 5
    3 -4
    

**Output :** *The output is an answer if it satisfiable or not and if it is satisfiable an instantiation comes with.*

**Example :**
    ```
    [-2, 5, 3, 1]
    ```

**Credits :** *This project is developed by Sébastien RICHARD, a student at the University of Toulon.*

**License :** *This project is under the MIT license.*

**Contact :** *For any questions or suggestions, please contact me at sebastien-richard3@etud.univ-tln.fr*

