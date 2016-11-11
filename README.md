# Crossword Solver
## What is _Crossword Solver_?
The aim of the project is to implement an example of a backtracking algorithm (using improvements like _Forward-Checking_ and some heuristics). To do this, we've dealt with the crossword problem. Given a crossword board and using a dictionary of valid words in a language, then we have to find a valid solution for that crossword applying the rules of the popular crossword game.

### The algorithm
We'll use a *backtracking algorithm* variation: *forward-checking*, with some heuristics (_LWF_: Largest Word First, _MCV_: Most Constraining Values and _MRV_: Minimum Remaining Values) to improve the solving speed

## What can the _Crossword Solver_ do?
1. **Solve a crossword board** (read from a file)
2. **Display the solving process** the software applies while is solving the crossword. This helps us to check how the algorithm is working and introduce improvements based on its behaviour.
3. **Generate crossword puzzles** given an empty crossword. We'll look for the solutions and afterwards look for the meanings of the words in an online dictionary (currently only in [_Wiktionary_](https://www.wiktionary.org/) in Catalan language)

## About the code
The code is written in _Python 3_, and requires some libraries (available in [_PyPi_](https://pypi.python.org/pypi)):

### Libraries
#### Required
The following libraries are required for the software to run:
 - `numpy`

#### Optional
The following libraries must be present if you want to generate crossword puzzles based on an online dictionary
 - `mwapi`
 - `beautifulsoup4`

### Running the application
The application is command-line based so, open a terminal and change into the repo's root. Then, you can run the application calling to Python interpreter into main script:
```bash
python src/main.py -h
```
The `-h` argument will help you to discover how the software works and what it can do for you

### License
The code is licensed under Apache Software Foundation (_ASF_) License v2.0

***Made with love in [ETSE](https://uab.cat/enginyeria), UAB by @ccebrecos & @davidlj***
<center><img src="http://www.uab.cat/doc/logo-UAB.png" width="100" alt="UAB Logotype"></center>
