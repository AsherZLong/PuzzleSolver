test=[[9,0,1,4,0,2,0,3,0],
      [0,0,8,0,6,0,0,0,0],
      [0,2,0,0,0,0,0,0,0],
      [1,4,0,2,0,0,0,0,8],
      [0,0,0,0,7,0,0,0,0],
      [6,0,0,0,0,4,0,7,3],
      [0,0,0,0,0,0,0,9,0],
      [2,0,0,0,5,0,7,0,0],
      [0,8,0,7,0,6,4,0,5]]
import time as t

def column_maker(array):
    import pandas
    Data_Frame= pandas.DataFrame(array) # Make array into data frame
    columns= []
    for col in range(len(Data_Frame.axes[1])): # Go through each column
        individual_columns=Data_Frame.iloc[:,col].tolist() # Add each column to list
        columns.append(individual_columns) # Add each column to final list
    return columns
    
def Box_maker(x):
    grid_size= len(x)
    size_box = int(grid_size**0.5)
    boxes = []
    for box_i in range(0, size_box):
        for box_j in range(0, size_box):
            box = []
            for i in range(0, size_box):
                for j in range(0, size_box):
                    box.append(x[size_box*box_i + i][size_box*box_j + j]) # Covers every cell in the array and appends it to the current box which then is appended to the bigger array, boxes
            boxes.append(box)
    return boxes
            
def markupmaker(array):
    grid_size= len(array)
    columns=column_maker(array)
    boxes=Box_maker(array)
    size_box = int(grid_size**0.5)
    markup=[]
    for q in range(grid_size):## Adds an empty list for each row to the markup
        markup_row=[]
        markup.append(markup_row)
        for w in range(grid_size):## adds an empty list for each cell in the markup
            markup_column=[]
            markup[q].append(markup_column)
## Adding values to the markup for each cell
    for i in range(1,grid_size+1):##loop through numbers 1 to 9
        for j in range(grid_size):##loop through rows
            for k in range(grid_size):##loop through cells
                if array[j][k] == 0:
                    if i not in array[j]:## check not in row
                        if i not in columns[k]:## check not in column
                           if i not in boxes[((j//size_box)*size_box)+(k//size_box)]:
                               markup[j][k].append(i)
    return markup

def markup_single(markup,array):
    grid_size=len(array)
    for i in range(grid_size): #going through row of markup
        for j in range(grid_size): #going through cell in markup
            if len(markup[i][j])==1: #checks if markup for cell is single
                array[i][j]=markup[i][j][0] #if it is then fill in the array with that single
                return array
    return array #if no elements of the markup are single then return the array

def markup_minimise(array1):
    count = 0
    while count == 0:
        #markup1 = MarkupSoloFiller2(array1)
        markup1=markupmaker(array1) #create an initial markup for an array
        array2 = markup_single(markup1, array1)#creates a new array with singles filled in from markup
        markup2 = markupmaker(array2)#creates new markup from new array with singles added
        if markup1 == markup2:#checks if new markup is same as initial markup
            count +=1 #if there is no change in markup then no cell has been filled in so the function ends and returns filled in array
        else:
            array1 = array2
    return array2

def preemptive_set_maker(markup): 
    grid_size = len(markup)
    for i in range(grid_size): # Go through each row
        for j in range(grid_size): # Go through each cell
            size_poss_preemptive = len(markup[i][j]) #size of preemptive set
            preemptive_pos = [] #create list of preemptive set co-ordinates
            if len(markup[i][j]) != 0: # If markup for cell is not empty
                markup_set=set(markup[i][j]) #create set of preemptive set
                for k in range(grid_size): # Go through cells again
                    if len(markup[i][k]) != 0: #if the markup is non-empty
                        temp_set=set(markup[i][k]) 
                        if temp_set.issubset(markup_set): # If cell (i,k) markup is subset of cell (i.l)
                            preemptive_pos.append(k) #add cell coordinate to preemptive set
                if len(preemptive_pos) == size_poss_preemptive: #if the number of subset cells is the same as the number of elements in the markup 
                    for l in range(grid_size):
                        if l not in preemptive_pos:
                            for m in markup[i][j]:
                                if m in markup[i][l]:
                                    markup[i][l].remove(m) #remove other elemnts from those cells leaving just the preemptive set
    return markup

def preemptive_minimiser(array1):
    #only runs once and runs on rows columns and boxes
    markup1 = markupmaker(array1)
    markup1 = preemptive_set_maker(markup1)
    markup1 = preemptive_set_maker(column_maker(markup1))
    markup1 = preemptive_set_maker(Box_maker(markup1))
    return markup1

def Is_Error(markup,array):
    grid_size= len(array)
    for i in range(grid_size):
        for j in range(grid_size):
            if array[i][j]==0 and len(markup[i][j])==0: #checks if any cells ahs an empty cell and an empty markup, if there is then there is an error
                return True
    return False
            
def Is_Solution(array):
    grid_size= len(array)
    for i in range(grid_size):
        for j in range(grid_size):
            if array[i][j] == 0: #if there any cells in the array still not filled in then not a solution so return False
                return False
    return True

def takeThird(elem):
    return elem[2] #just returns third element of list

def Random_Guesser(inputarray):
    import copy
    #for row in inputarray:
     #   print(row)
    #print('')    
    markup=markupmaker(inputarray)
    grid_size= len(inputarray) # Loop through cells in row
    possMarkups=[]
    for i in range(grid_size):
        for j in range(grid_size):
            if len(markup[i][j])!=0:
                possMarkups.append((i,j,len(markup[i][j]))) #make a list of all non empty markups
    possMarkups.sort(key=takeThird) #sort by their length
    if len(possMarkups)==0: #if there are no possible markups then either array is already solved or there is an incorrect input, either way random guesser can do nothing
        return inputarray,False
    i,j=possMarkups[0][0],possMarkups[0][1] #define i and j as coordinate of smallest markup
    k=len(markup[i][j]) #length of smallest markup
    for position in range(k): # Position in markup < amount of numbers in markup
        gArray=copy.deepcopy(inputarray) #create a seperate deep copy going through each element of arrays within arrays to guess from
        gArray[i][j]=markup[i][j][position]# Add chosen number to array
        gArray = markup_minimise(gArray) # Go through trying to solve it with this guess in place
        gMarkup=markupmaker(gArray) #make a markup for guess
        preemptive_minimiser(gArray)
        if Is_Solution(gArray):
            return gArray,True #if array is the solution then return True and top of recursion will reutrn the array
        elif not Is_Error(gMarkup,gArray): #if there is not an error with the guess
            #Random_Guesser(array)
            gArray,flag=Random_Guesser(gArray) #maker another guess
            if flag: #if flag is true then pass to previous layer of recursion to be passed all the way to the first layer of recursion
                return gArray,flag
    return gArray,False #if there is an error then flag false and go back to previous layer till a different guess can be made

def errorCheck(array):
    cols=column_maker(array)
    boxes=Box_maker(array)
    grid_size=len(array)
    for i in range(grid_size):#Takes each row
        for j in range(1,grid_size+1):# For each possible entry
            if array[i].count(j)>1 or cols[i].count(j)>1 or boxes[i].count(j)>1:#If any number appears more than once in row i, column i, or box i.
                raise Exception('Input has duplicate values in sub-structure')#Returns an Error message and stops code running.
    if grid_size**(1/2)!=int(grid_size**(1/2)):#Checks the length of the array is a square number.
        raise Exception('length of grid must be a square number')
    for i in range(grid_size):
        if len(array[i])!=grid_size:#Checks each row is of the same length as the columns.
            raise Exception('input not a square')
        for j in range(grid_size):#Cycles through every cell.
            if type(array[i][j])!=int:#Checks inupts are integers.
                raise TypeError(f'Input contains non integer at row {i+1} column {j+1}')#Returns position of error in input and stops code running.
            elif array[i][j]>grid_size or array[i][j]<0:#Checks all inputs are in the correct numerical range for the sudoku.
                raise TypeError(f'Input not in range of expected possible input values at row {i+1} column {j+1}')#Returns location of error and stops code from running.

def solve(array):
    errorCheck(array)
    array1=markup_minimise(array)
    if Is_Solution(array1):
        return array1
    Sol,Error=Random_Guesser(array1)
    if Error:#If no error is found.
        return Sol
    else:
        raise Exception('Input is not solvable')

def humanReadable(array):#Outputs the array input in a nice looking format.
    for row in array:
        print(row)
    print('')   
    

[[0,0,0,0,0,1,9,8,0],
 [0,0,6,4,8,9,0,0,3],
 [0,7,0,0,0,0,6,0,0],
 [0,6,0,3,0,0,4,0,0],
 [4,0,0,0,0,0,0,0,7],
 [0,0,2,0,0,7,0,9,0],
 [0,0,7,0,0,0,0,5,0],
 [9,0,0,1,2,5,7,0,0],
 [0,3,1,8,0,0,0,0,0]]

t1=t.perf_counter()
solve(test)
t2=t.perf_counter()
print(t2-t1)



