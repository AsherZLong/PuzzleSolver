## READ ME ##

Signpost solver

A user should import Signpost.py then call the solve() function on an input to retunr the solution.

Input should be in the form of an array of arrays with each cell being reperesented with:
a list of a string indicating compass point and a number indicating the cell's position in the sequence.
For example:[[['S',1],['S',0],['W',0],['SW',0]],[['E',0],['E',0],['S',0],['NW',0]],[['N',0],['SE',0],['SW',0],['N',0]],[['E',0],['NE',0],['NE',0],['F',16]]]
is a 4x4 example with [['S',1],['S',0],['W',0],['SW',0]] being the first row.

The output of a soluble signpost puzzle will be in the same form as the input.

If the input is unsolvable the solve function will raise an error, giving the reason behind lack of solvability.

Puzzles can be found here: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html