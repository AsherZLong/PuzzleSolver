#Signpost Solver

https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/signpost.html

#Input list of rows, each cell is tuple of compass point string and number (initially 0)
#convert compass point to index notation of each cell with SE being [1,1].
#[-1,-1],[-1,0],[-1,1]
#[0,-1] ,[0,0], [0,1]
#[1,-1] ,[1,0], [1,1]

#Assuming square, solvable inputs
#step by step:
#create markup for each cell of which cells point to it
#fill in cells with only one pointer
    #remove pointers that have been filled somewhere from markup
    #remove markup elements that already have a number
#keep iterating till filled in
#Guess if not

test=[[['SE',0],['SW',0],['SE',0],['SW',0],['S',0]],
      [['N',0],['SW',0],['S',0],['N',0],['S',0]],
      [['S',0],['S',0],['W',0],['S',1],['NW',0]],
      [['E',0],['N',0],['SE',0],['E',0],['N',0]],
      [['NE',0],['NE',0],['NW',0],['W',0],['F',25]]]

test6=[[['E',1],['SW',0],['S',0],['SE',0],['SW',0],['SW',0]],
       [['S',6],['E',0],['S',0],['NW',15],['E',0],['N',0]],
       [['S',0],['NE',0],['E',31],['S',0],['S',0],['W',0]],
       [['E',0],['N',0],['NW',0],['NE',0],['SW',0],['SW',0]],
       [['NE',0],['N',0],['E',0],['S',0],['N',0],['NW',0]],
       [['E',25],['E',0],['N',0],['N',0],['E',0],['F',36]]]

from copy import deepcopy
import numpy as np

def converter(inp):
    grid_size=len(inp) #define grid_size in every function as the length of outer array as inputs should all be square
    out=[]                  #error check (written later) will flag issues if input is not square
    for row in range(grid_size):
        rowtemp=[]
        for col in range(grid_size):
            celltemp=[]
            if inp[row][col][0]=='N':
                celltemp.append([-1,0])
            elif inp[row][col][0]=='NE':
                celltemp.append([-1,1])
            elif inp[row][col][0]=='E':
                celltemp.append([0,1])
            elif inp[row][col][0]=='SE':
                celltemp.append([1,1])
            elif inp[row][col][0]=='S':  #convert each string compass input to a list of [row,col] direction
                celltemp.append([1,0])   #setting [1,0] to a shift 1 row down and [0,1] 1 column across as this works well with grid indexing 
            elif inp[row][col][0]=='SW':
                celltemp.append([1,-1])
            elif inp[row][col][0]=='W':
                celltemp.append([0,-1])
            elif inp[row][col][0]=='NW':
                celltemp.append([-1,-1])
            elif inp[row][col][0]=='F': #endpoint has no direction
                celltemp.append([0,0])
            else:
                raise TypeError(f'Input contains invalid direction input at row {row} column {col}') 
                #if there is an input that is not an inter-cardinal compass direction or the end then want to raise an error
            celltemp.append(inp[row][col][1]) #put the direction with the cells number into a list
            rowtemp.append(celltemp) #add each cell list to a row list
        out.append(rowtemp) #add all rows to total array
    return out #output is similar to input but each string is converted to corresponding direction pair.

def markup_maker(array):
    carray=converter(array) #convert the input
    grid_size=len(array)
    out=[] #create a total array to put each row in
    for row in range(grid_size):
        temp=[] #create a row array to put each cell in
        for col in range(grid_size):
            a=[] #create a cell array
            temp.append(a) #add cells to row
        out.append(temp) #add rows to total
    for row in range(grid_size):
        for col in range(grid_size):
            direc=carray[row][col][0] #define the direction of cell
            if direc!=[0,0]: #don't want the end point to append to point to itself infinitely.
                for i in range(1,grid_size):
                    direc_row,direc_col=np.multiply(i,direc) #find multiple of cell direction for each i
                    temp_direc_row,temp_direc_col=row+direc_row,col+direc_col #add current cell direction to cell coord
                    if 0<=temp_direc_row<grid_size and 0<=temp_direc_col<grid_size: #if the pointed cell coord is inside the grid
                        out[temp_direc_row][temp_direc_col].append([row,col]) #add coordinates of starting cell to current visited cell
    return out             #for example cell ['SE',0] in position [1,0] becomes [[1,1],0] so adds its coords to cells: [2,1],[3,2] but not [4,3] in a 4x4 grid as only goes from [0,0] to [3,3]

def initial_markup_maker(array): #once the initial markup is made a couple of modifications need to be made
    markup=markup_maker(array) #want to set the markup of the cell containing 1 to empty as it should never be changed
    grid_size=len(array) #also want to clear markups for cell that are already pointed to
    filled_nums=[] #for example if the input contains x and x+1 then the markup of x+1 should start as 0 as to not cause errors.
    filled_pos=[]
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],int) and array[row][col][1]>0:
                filled_nums.append(array[row][col][1]) #append all the cells which have sequence number filled in (non zero)
                filled_pos.append([row,col]) #append the coords of these cells.
            if array[row][col][1]==1:
                t=[row,col] #store the coordinate of the cell containing 1 (not always [0,0]; free ends mean 1 and end point can be anywhere in the grid)
    for i in range(len(filled_nums)):
        if filled_nums.count(filled_nums[i]-1)!=0: #if for each filled cell, the previous number is also filled
            temp=filled_nums.index(filled_nums[i]-1) #find index of previous number (same in filled_nums as filled_pos)
            markup[filled_pos[i][0]][filled_pos[i][1]]=[filled_pos[temp]] #set markup to be just the pointing cell
    markup[t[0]][t[1]]=[] #set cell containing 1 to have markup of 0
    return markup

def solo_filler(array,markup): #just fill in any cells that have one possible pointer.
    grid_size=len(array)
    for row in range(grid_size):
        for col in range(grid_size):
            if len(markup[row][col])==1 and array[row][col][1]==0:
                array[row][col][1]=markup[row][col][0]
    return array

#if a pointer only appears once then it must be the markup of that cell

def unique_pointer(array,markup):
    grid_size=len(markup)
    filled_markups=[]
    all_markups=[] #all markups is all cell markups
    all_pos=[]
    for row in range(grid_size):
        for col in range(grid_size):
            if len(markup[row][col])==1:
                filled_markups.append(markup[row][col]) #list of cells with a single entry in the markup
            for i in range(len(markup[row][col])):
                all_markups.append(markup[row][col][i])
                all_pos.append([row,col])
    unique_markup=[]
    unique_pos=[]
    for i in range(len(all_markups)):
        if all_markups.count(all_markups[i])==1: #if markup only appears once
            unique_markup.append(all_markups[i])
            unique_pos.append(all_pos[i])
    for i in range(len(unique_markup)):
        markup[unique_pos[i][0]][unique_pos[i][1]]=[unique_markup[i]] #fill in cells with a unique markup
    return markup #if they were not pointed to by the unique pointer then the unqiue pointer does not point to any cells which is a problem.
                  #therefore markup of cell must be unique pointer

#if a cell is pointed to then its pointer cannot point to any other cell

def filled_remover(array,markup): #if a cell points to another then i want to remove its coords from all other markups as it can only point to one.
    grid_size=len(markup)
    partial_filled=[] #parital filled will be list of pointer coords for cells with one markup for previous but not a definite number
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],list):
                partial_filled.append(array[row][col][1])
    for row in range(grid_size):
        for col in range(grid_size):
            for k in range(len(partial_filled)):
                if markup[row][col].count(partial_filled[k])!=0: #if the markup of a cell is one of the single pointers found earlier
                    markup[row][col].remove(partial_filled[k]) #remove pointing markups from all cells containing markups
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],list):
                markup[row][col].append(array[row][col][1]) #replace pointing markups in cells they point to
    return markup

#if a cell is pointed to by a known number then its markup must be just that number
#similar to filled_remover but covers case where sequence is int not list

def filled_nums(array,markup): #similar to previous function but works with if x and x+1 have non zero sequence numbers
    grid_size=len(markup)
    filled_nums=[]
    filled_nums_pos=[]
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],int) and array[row][col][1]>0:
                filled_nums.append(array[row][col][1])
                filled_nums_pos.append([row,col])
    remove_markup=[]
    for i in range(len(filled_nums)):
        if filled_nums.count(filled_nums[i]-1)!=0:
            q=filled_nums.index(filled_nums[i]-1)
            remove_markup.append(filled_nums_pos[q])
    for row in range(grid_size):
        for col in range(grid_size):
            if len(markup[row][col])>1:
                for i in range(len(remove_markup)):
                    if markup[row][col].count(remove_markup[i])!=0:
                        markup[row][col].remove(remove_markup[i])
                '''for i in range(len(filled_nums)):
                    if markup[row][col].count(filled_nums_pos[i])!=0 and isinstance(array[row][col][1],int) and array[row][col][1]>0:
                        point1,point2=filled_nums_pos[i][0],filled_nums_pos[i][1]
                        if isinstance(array[point1][point2][1],int) and array[point1][point2][1]>0 and array[row][col][1]>array[point1][point2][1]+1:
                            markup[row][col].remove([point1,point2])'''
    return markup #tried to write an extra piece of function that if x+a (a>1) lies in the direction of x then x cannot point to x+a
                  #however for some reason this took either an extrememly long time or infinite time so decided to not use it

#if a cell points the direction of its pointer then remove from pointer markup

def pointed(array,markup): #if x points east and x+1 points west then x+1 coords will be in x but cannot actually point to it as this is a loop within the grid
    grid_size=len(array)
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],list):
                m=array[row][col][1]
                if markup[m[0]][m[1]].count([row,col])!=0:
                    markup[m[0]][m[1]].remove([row,col])
    return markup

#what if have x and x+2, when x+1 is found x+2 will have its markup changed but x+1 needs to be changed too

def middle_sequence(array,markup): #very specific case but was casuing issues
    grid_size=len(array)           #if x and x+2 are already found and a unique cell points to x+2 and is in the line of x
    convert=converter(array)       #then x+1 will point to x+2 and later the markup will be cleaned but it will not realise that x points to it so that must be cleaned too
    filled_nums,filled_nums_pos=[],[]
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],int) and array[row][col][1]!=0:
                filled_nums.append(array[row][col][1])
                filled_nums_pos.append([row,col])
    for i in range(len(filled_nums)):
        for j in range(1,grid_size):
            direc1,direc2=np.multiply(j,convert[filled_nums_pos[i][0]][filled_nums_pos[i][1]][0])[0],np.multiply(j,convert[filled_nums_pos[i][0]][filled_nums_pos[i][1]][0])[1]
            if [direc1,direc2]!=[0,0]:
                rowdirec,coldirec=filled_nums_pos[i][0]+direc1,filled_nums_pos[i][1]+direc2
                if 0<=rowdirec<grid_size and 0<=coldirec<grid_size: #check along all pointing lines
                    if isinstance(array[rowdirec][coldirec][1],int) and array[rowdirec][coldirec][1]==filled_nums[i]+1: #if a cell points to a cell with sequence number one greater than it
                        markup[rowdirec][coldirec]=[filled_nums_pos[i]]                                                 #then clear markup of the cell one greater to be just the cell pointing to it.
    return markup

def markup_cleaner(array,markup): #collection of previous functions to clean up the markup and aid solving
    unique_pointer(array,markup)  #none of these functions change the array, only the markup
    filled_remover(array,markup)
    filled_nums(array,markup)
    pointed(array,markup)
    middle_sequence(array,markup)
    return markup

def pre_filler(array,markup): #the only function that changes sequence numbers by checking if they point to a cell one greater
    grid_size=len(array)      #or are pointed to by a number
    a1=[]
    while array!=a1: #want to keep filling till no changes as there will probably be chains of pointers
        a1=deepcopy(array)
        for row in range(grid_size):
            for col in range(grid_size):
                if isinstance(array[row][col][1],list): #if cell has pointer
                    point1,point2=array[row][col][1][0],array[row][col][1][1]
                    if isinstance(array[point1][point2][1],int) and array[point1][point2][1]>0: #if pointer has non zero sequence number 
                        array[row][col][1]=array[point1][point2][1]+1 #set pointed to cell to be one greater than pointer
                        markup[row][col]=[[point1,point2]] #set markup to be just pointer cell coord
                if len(markup[row][col])==1 and isinstance(array[row][col][1],int) and array[row][col][1]!=0: #if cell has unique markup and has non zero sequence number
                    pointed1,pointed2=markup[row][col][0][0],markup[row][col][0][1] #store coordinates of the pointer
                    if not (isinstance(array[pointed1][pointed2][1],int) and array[pointed1][pointed2][1]!=0): #if the pointer does not already have a sequence number
                        array[pointed1][pointed2][1]=array[row][col][1]-1 #set pointer to one less than the cell
                        markup[row][col]=[[pointed1,pointed2]] #set markup to be pointer
    return array

def looper(array,markup=[]): #combination of all mathematical analysis functions
    if markup==[]:
        markup=initial_markup_maker(array)
    solo=solo_filler(array,markup)
    pre_filler(solo,markup)
    a1=[]
    while a1!=array: #while the array is changing
        a1=deepcopy(array)
        markup=markup_cleaner(solo,markup) #clean markup then fill in solos and fill in sequence numbers
        solo=solo_filler(solo,markup)
        solo=pre_filler(solo,markup)
    return solo,markup

#This part is the random guessing 

def is_solution(array):
    grid_size=len(array)
    all_nos=[]
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],list): #if there are pointers
                return False #then not a solution
            if array[row][col][1]==0: #if there are zeros in the sequence numbers
                return False #then not a solution
            if all_nos.count(array[row][col][1])>0: #if any sequence numbers already appear
                return False #then not a solution (error)
            all_nos.append(array[row][col][1])
    return True

def is_error(array): 
    grid_size=len(array)
    all_nos=[]
    for row in range(grid_size):
        for col in range(grid_size):
            if isinstance(array[row][col][1],int) and not array[row][col][1]==0: #if there duplicate non zero sequence numbers
                all_nos.append(array[row][col][1])
                if all_nos.count(array[row][col][1])>1:
                    return True #return True, there is an error
    return False

def takeThird(elem):
    return elem[2] #just returns third element of list

def random_guesser(array,markup=[]):  
    if markup==[]:
        markup=initial_markup_maker(array)
    grid_size=len(array)
    poss_markups=[]
    for row in range(grid_size):
        for col in range(grid_size):
            if len(markup[row][col])>1 and array[row][col][1]==0:
                poss_markups.append([row,col,len(markup[row][col])]) #make a list of all multiple element markups
    poss_markups.sort(key=takeThird) #sort by their length
    if len(poss_markups)==0: #if there are no possible markups then either array is already solved or there is an incorrect input, either way random guesser can do nothing
        return array,False
    row,col=poss_markups[0][0],poss_markups[0][1] #define row and col as coordinate of smallest markup
    length=len(markup[row][col]) #length of smallest markup
    for pos in range(length): # Position in markup < amount of pointers in markup
        guess_array=deepcopy(array) #create a seperate deep copy going through each element of arrays within arrays to guess from
        guess_array[row][col][1]=markup[row][col][pos]# Add chosen number to array
        guess_markup=deepcopy(markup) #make a markup for guess
        guess_markup[row][col]=[markup[row][col][pos]]
        looper(guess_array,guess_markup) # Go through trying to solve it with this guess in place
        if is_solution(guess_array):
            return guess_array,True #if array is the solution then return True and top of recursion will return the array
        elif not is_error(guess_array): #if there is not an error with the guess
            guess_array,flag=random_guesser(guess_array,guess_markup) #maker another guess
            if flag: #if flag is true then pass to previous layer of recursion to be passed all the way to the first layer of recursion
                return guess_array,flag
    return guess_array,False #if there is an error then flag false and go back to previous layer till a different guess can be made

def humanReadable(array):#Outputs the array input in a nice looking format.
    for row in array:
        print(row)
    print('')
    
def error_check(array):
    grid_size=len(array)
    vals=[]
    for row in range(grid_size):
        if len(array[row])!=grid_size:
            raise Exception(f'Input grid is not square; row {row} is not same length as height of grid.')
        for col in range(grid_size):
            if not isinstance(array[row][col][1],int):
                raise Exception(f'invalid input for position in sequence at position [{row},{col}]')
            if array[row][col][1]>0:
                vals.append(array[row][col][1])
            if vals.count(array[row][col][1])>1:
                raise Exception(f'Duplicate values appears; second one in cell [{row},{col}].')
    if vals.count(1)!=1:
        raise Exception('Missing start 1 cell')
    if vals.count(grid_size**2)!=1:
        raise Exception(f'Missing end {grid_size**2} cell')
    converter(array)
    return array
    
def solve(array):
    error_check(array)
    array,markup=looper(array)
    if is_solution(array):
        return array
    sol,flag=random_guesser(array,markup)
    if flag:
        return sol
    else:
        raise Exception('Input is not solvable')

#Time testing:
#mean time for 4x4=0.01757
#mean time for 4x4 with free ends=0.006457
#mean time for 5x5=0.1293
#mean time for 5x5 with free ends:0.06838
#mean time for 6x6=11.48
#mean time for 7x7:233.4 (4mins)
#time taken for longest 7x7 is 727 (12mins) seconds
