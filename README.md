# Crossword solver
## Objectiu
Donat un *crossword* o mots encreuats, hem de, usant un diccionari trobar una solució vàlida aplicant les regles del joc
## Algorismes
S'usarà l'algorisme de cerca local *backtracking* i millores usant el *forward checking*
###### Notes
En *sr.Ramón Baldrich* triga menys d'un minut (30-40s) en resoldre el *crossword* amb el diccionari gegant
# Història
## Temps
Les proves s'han executat en dos PCs de sobre taula amb processador `Intel i7 4790k 4.0 Ghz` sota el sistema operatiu `Microsoft Windows 10 [10.0.14393]` i `Python 3.5.2`

1. **Backtracking bàsic**
	- Sense `numpy`
	- Agafem primera variable de la llista
	- Sense *forward-checking*
	- Domini separat per longituds de paraula
	- Restriccions indexades per variable
	- Usem classes / objectes
	```
 	SMALL SET:
	Loading time: 	0.001501 +- 0.0005 seconds
	Compute time:   0.095592 +- 0.0100 seconds
	------------------------------------------
	Total time:     0.097093 +- 0.0105 seconds

	BIG SET:
	Loading time:   45.061957 +- 2 seconds
	Compute time:   18 hours & counting...
	------------------------------------------
	Total time:		∞
	```
2. **Backtracking bàsic + millora heurística**
	- Sense `numpy`
	- Agafem la variable de la llista amb més restriccions
	- Sense *forward-checking*
	- Domini separat per longituds de paraula
	- Restriccions indexades per variable
	- Usem classes / objectes
	```
 	SMALL SET:
	Loading time: 	0.001501 +- 0.0005 seconds
	Compute time:   0.000000 +- 0.0005 seconds
	------------------------------------------
	Total time:     0.001501 +- 0.0010 seconds

	BIG SET:
	Loading time:   45.061957 +- 2 seconds
	Compute time:   hours & counting...
	------------------------------------------
	Total time:		∞
	```
2. **Backtracking + _forward-checking_**
	- Sense `numpy`
	- Agafem primera variable de la llista
	- Sense *forward-checking*
	- Domini separat per longituds de paraula
	- Restriccions indexades per variable
	- Usem classes / objectes
	```
 	SMALL SET:
	Loading time: 	 +-  seconds
	Compute time:    +-  seconds
	------------------------------------------
	Total time:      +-  seconds

	BIG SET:
	Loading time:   45.061957 +- 2 seconds
	Compute time:   ? hours & counting...
	------------------------------------------
	Total time:		∞
	```
