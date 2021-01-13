# Justin Lu
# Implements the A* search algorithm on the sliding puzzle game of RushHour
from copy import deepcopy


# State class is one instance of the Rush Hour board
class State():
    def __init__(self, board, parent, cars):
        self.board = board   # Board is a 2d array representing the current board
        self.parent = parent # Parent is a pointer to previous state (used for tracing optimal path)
        self.cars = cars     # List of car objects
        self.g = 0           # Path from start
        self.h = 0           # Any heuristic
        self.f = 0           # Combined values of h and g
        
    def __eq__(self, other):
        return self.board == other.board

# Car class represents a single car in a state
class Car():
    def __init__(self, letter, x, y, length, ori):
        
        self.letter = letter # Alphabetical representation of the car
        self.x = x           # Most left X coord of car
        self.y = y           # Highest Y Coord of car
        self.length = length # Length of car
        self.ori = ori       # "H" - Horizontal or "V" - Vertical
            
    def __eq__(self, other):
        return self.letter == other.letter


# MAIN RUSHHOUR FUNCTION -------------------------    
# Rushhour function takes a starting rush hour state and 1 or 0 arg
# to decide a blocking or custom heuristic, it then uses A*
# Algo on given heuristic and state to calculate
# and print out the optimal path, total moves, and states explored

# sample format :
## rushhour(0,["-ABBO-",
## "-ACDO-",
## "XXCDO-",
## "PJFGG-",
## "PJFH--",
## "PIIH--"] )

def rushhour(heuristicArg, startingState):

    # Get neccessary information from start
    intialBoard = getBoard(startingState)
    cars = getCars(intialBoard)
    
    # Intialize our starting state
    start = State(intialBoard, None, cars)
    start.g = 0
    start.h = 0
    start.f = 0

    # This is our closed list, tracks all visited states
    visitedStates = []
    # This is our open list / frontier, holds all potential states to visit
    frontier = []

#A* ALGORITHM / BEST FIRST SEARCH -------------------------------
    # Counter used to track moves explored
    frontierCounter = 0
    # Put starting state into frontier
    frontier.append(start)
    
    # Pull nodes off frontier if there are states to be taken
    while len(frontier) > 0:
        
        # Loop through frontier, checking each next element
        # to select state with lowest f value
        currState = frontier[0]
        for state in frontier:
            if state.f < currState.f:
                currState = deepcopy(state)

        # Pull move off frontier now that we use it       
        frontier.remove(currState)       
        frontierCounter = frontierCounter + 1

        # Used to track if we are finished
        foundGoal = False

        foundGoal = checkIfGoal(currState, frontierCounter)
        
        # If we print goal solution leave frontier looping, we are finished           
        if foundGoal == True:
            break

        # Generates all possible moves to be taken with current state
        allPossibleStates = getMoves(currState)
        
        for state in allPossibleStates:
                # Make sure we have not already visited this state
                if state.board not in visitedStates:
                                   
                    if foundGoal == False:
                        if heuristicArg == 0:
                            blockingHeuristic(state,frontier,currState)
                            
                        elif heuristicArg == 1:
                            customHeuristic(state,frontier,currState)
                                               
        # Once moves generated add current state to visisted states list                
        visitedStates.append(currState.board)


# BLOCKING HEURISTIC ---------------------------
# Given a state, calculates the g,h,and f values
# For H(n), counts how many spaces in front of
# Red car are not "-" + 1, once all needed values are calculated
# Function appends new state to frontier
def blockingHeuristic(state,frontier,currState):                
    # Calculate G, add one b/c new child
    state.g = currState.g + 1
    
    # Locate X position of red car
    for car in state.cars:
        if car.letter == "X":
            redCarX = car.x
            
    # H is set to 1 + #Blocking cars
    hValue = 1       
  
    # Check for non "-" in front of red car
    for i in range(len(state.board[2])):
        # Make sure in front of red car and spot is not empty
        if (i > redCarX + 1) and (state.board[2][i] != "-"):
            hValue = hValue + 1
            
    # If goal return, h as 0 (Assignment prompt states to do so)    
    if(state.board[2][4] == "X" and state.board[2][5] == "X" ):
        hValue = 0
        
    # Set H to amount of blocking cars
    state.h = hValue                    
    # Set F to G + H
    state.f = state.g + state.h

    # Flag used to check if state exist in frontier already
    flag = False
    
    # Check for same state in frontier
    for i in frontier:
        if (state.board == i.board):
                flag = True
                
    if flag != True:
        frontier.append(state)


# CUSTOM HEURISTIC ---------------------------
# Given a state, calculates the g,h,and f values
# For H(n), counts how many spaces in front of
# Red car are not "-", as well as distance of red car
# from exit , + 1, once all needed values are calculated
# Function appends new state to frontier
# The improved heuristic reduces our amount of states explored
# As it picks tiebreakers better than the blocking heuristic does
def customHeuristic(state,frontier,currState):
    # Calculate G, add one b/c new child
    state.g = currState.g + 1
    
    # Locate X position of red car
    for car in state.cars:
        if car.letter == "X":
            redCarX = car.x          
    hValue = 1

    # Find blocking cars, increment accordingly
    for i in range(len(state.board[2])):
        if (i > redCarX + 1) and (state.board[2][i] != "-"):
            hValue = hValue + 1
            
    # Tracks distance of red Car from exit, increment accordingly
    for i in range(len(state.board[2])):
        if (i > redCarX + 1):
            hValue = hValue + 1
            
    if hValue == 1:
        hValue = 0
        
    # Set H to total incremented value       
    state.h = hValue                    
    state.f = state.g + state.h

    # Since custom, to improve efficency, I set f to 0 , since
    # it is the goal state anyways, instead of setting h to 0
    # like I do for blocking
    if(state.board[2][4] == "X" and state.board[2][5] == "X" ):
        state.f = 0
    
    flag = False
    
    # Check for same state in frontier
    for i in frontier:
        if (state.board == i.board):
                flag = True
    if flag != True: 
        frontier.append(state)


# Given a state, it checks if the red car is in the winning position
# if it is it prints out the path, moves taken, and moves explored
# and returns a flag with true for goal found and false for goal not found
def checkIfGoal(state,frontierCounter):    
    # Check if goal state Ie: the XX car is at (2,4) & (2,5)
    if(state.board[2][4] == "X" and state.board[2][5] == "X" ):
        # Add all states taken to reach goal path
        # Use parent attribute to get previous states board
        goalPath = []
        while state is not None:
            # Uses parent attribute to trace path
            goalPath.append(state.board)
            state = deepcopy(state.parent)
 
        # Print out the goal paths as string output
        for i in reverse(goalPath):
            for j in i:
                for p in range(len(j)):
                    print(j[p], end='')        
                print("\n")
            print("\n")

        print("Total moves: "+str(len(goalPath)-1))
        print("Total states explored: ",frontierCounter)
        return True
    
    else:
        return False


# Takes in starting state as list of strings
# converts it into a 2d Array and returns it
def getBoard(startingState):
    intialBoard = []
    for i in startingState:
        rows = []
        for j in i:
            rows.append(j)
        intialBoard.append(rows)
    return intialBoard


# Takes in the intial board and finds all of the
# cars inside and their attributes, and returns a list
# filled with all the cars in the board
def getCars(intialBoard):
    # Represents all the cars list filled with car objects to be put
    # in starting state
    cars = []
    # List used to make sure once we see a unqiue car
    # we dont put in the same car
    uniqueCarLetter = []
    # This bulk of code finds a unique car letter, and depending on the surrounding area
    # it detects if the car is of length 2 or 3 , and finds its coordinates and orientation
    icounter = -1 # Represents row position
    for i in intialBoard:
        jcounter = -1 # Represents col position
        icounter = icounter + 1
        for j in i:
            jcounter = jcounter + 1
            if (j != "-"):
                if (j not in uniqueCarLetter):
                    uniqueCarLetter.append(j)
                    if jcounter <= 3: # Potential length 3 horizontal car
                        if intialBoard[ icounter][  jcounter+2] == j:
                            newCar = Car(j,jcounter, icounter, 3, "H")
                            cars.append(newCar)
                            continue
                    if jcounter <= 4: # Potential length 2 horizontal car
                        if intialBoard[ icounter][  jcounter+1] == j:
                            newCar = Car(j,jcounter, icounter, 2, "H")
                            cars.append(newCar)
                            continue           
                    if icounter <= 3: # Potential length 3 vertical car
                        if intialBoard[ icounter+2][  jcounter] == j:
                            newCar = Car(j,jcounter, icounter, 3, "V")
                            cars.append(newCar)
                            continue                         
                    if icounter <= 4: # Potential length 2 vertical car
                        if intialBoard[ icounter+1][  jcounter] == j:
                            newCar = Car(j,jcounter,icounter, 2, "V")
                            cars.append(newCar)
                            continue
    return cars


# Taking in current state, generates all possible Vertical and
# Horizontal moves and returns a list with all the moves
# Uses genHmoves and genVmoves
def getMoves(currState):
    # Generate all possible Horizontal moves
    possibleHStates = genHMoves(currState)
    # Generate all possible Vertical moves
    possibleVStates = genVMoves(currState)
    # Put all possible states into list
    allPossibleStates = []
   
    for i in possibleHStates:
        allPossibleStates.append(i)

    for i in possibleVStates:
        allPossibleStates.append(i)
    return allPossibleStates
                        
         
# Generates all Horizontal moves from given state
# in each possible move, we check if the spot we want to goto
# has a - , then we copy a new board and cars and put those
# into a new state which points to previous state as parent
# We then access the same car and modify the new car coordinates
# as well as modify the board of the new state, we then return a list
# with all the possible moves
def genHMoves(currState):
    possibleStates = []
    carCount = -1
    for car in currState.cars:
        carCount = carCount + 1
        if car.ori == 'H':   
            if car.x > 0:
                # Check left length 2
                if car.length ==2:
                    # Make sure the move is possible by checking if no car in spot
                    if currState.board[car.y][car.x-1] == '-':
                        # Copy board , cars , create new state
                        newBoard = deepcopy(currState.board)
                        newCars = deepcopy(currState.cars)
                        # Assign parent to current state in new state
                        newState = State(newBoard, currState, newCars)
                        newCar = newState.cars[carCount]
                        # Make swaps on new board, and change new car coords
                        newState.board[newCar.y][newCar.x+1] = '-'
                        newState.board[newCar.y][newCar.x-1] = newCar.letter
                        newCar.x = newCar.x - 1
                        # Add new state to possible States
                        possibleStates.append(newState)
                # Check left length 3        
                if car.length == 3:
                    if currState.board[car.y][car.x-1] == '-':
                        newBoard = deepcopy(currState.board)
                        newCars = deepcopy(currState.cars)
                        newState = State(newBoard, currState, newCars)
                        newCar = newState.cars[carCount]
                        newState.board[newCar.y][newCar.x+2] = '-'
                        newState.board[newCar.y][newCar.x-1] = newCar.letter
                        newCar.x = newCar.x - 1
                        possibleStates.append(newState)
               # Check right length 3
            if car.length == 3 and car.x < 3:
                if currState.board[car.y][car.x+3] == '-' :
                    newBoard2 = deepcopy(currState.board)
                    newCars2 = deepcopy(currState.cars)
                    newState2 = State(newBoard2, currState, newCars2)
                    newCar2 = newState2.cars[carCount]
                    newState2.board[newCar2.y][newCar2.x] = '-'
                    newState2.board[newCar2.y][newCar2.x+3] = newCar2.letter
                    newCar2.x = newCar2.x + 1
                    possibleStates.append(newState2)      
            # Check right length 2
            if car.length ==2 and car.x < 4:     
                if currState.board[car.y][car.x+2] == '-' :
                    newBoard2 = deepcopy(currState.board)
                    newCars2 = deepcopy(currState.cars)
                    newState2 = State(newBoard2, currState, newCars2)
                    newCar2 = newState2.cars[carCount]
                    newState2.board[newCar2.y][newCar2.x] = '-'  
                    newState2.board[newCar2.y][newCar2.x+2] = newCar2.letter
                    newCar2.x = newCar2.x + 1
                    possibleStates.append(newState2) 
    return possibleStates


# Generates all Vertical moves from given state, follows same format
# as horizontal move generator, returns list with possible vertical moves
def genVMoves(currState):
    possibleStates = []
    carCount = -1   
    for car in currState.cars:
        carCount = carCount + 1
        if car.ori == 'V':
            if car.y > 0:
                # Go up length 2
                if car.length == 2:      
                    if currState.board[car.y-1][car.x] == '-': 
                        newBoard = deepcopy(currState.board)
                        newCars = deepcopy(currState.cars)
                        newState = State(newBoard, currState, newCars)
                        newCar = newState.cars[carCount]  
                        newState.board[ newCar.y+1][ newCar.x] = '-'
                        newState.board[ newCar.y-1][ newCar.x] =  newCar.letter
                        newCar.y = newCar.y - 1
                        possibleStates.append(newState)
                # Go up length 3
                if car.length ==3:
                    if currState.board[car.y-1][car.x] == '-' :
                        newBoard = deepcopy(currState.board)
                        newCars = deepcopy(currState.cars)
                        newState = State(newBoard, currState, newCars)
                        newCar = newState.cars[carCount]
                        newState.board[newCar.y+2][newCar.x] = '-'
                        newState.board[newCar.y-1][newCar.x] =  newCar.letter
                        newCar.y = newCar.y - 1
                        possibleStates.append(newState)                      
            # Go down length 3
            if car.length == 3 and car.y < 3:
                if currState.board[car.y+3][car.x] == '-':
                    newBoard2 = deepcopy(currState.board)
                    newCars2 = deepcopy(currState.cars)
                    newState2 = State(newBoard2, currState, newCars2)
                    newCar2 = newState2.cars[carCount]
                    newState2.board[newCar2.y][newCar2.x] = '-'
                    newState2.board[newCar2.y+3][newCar2.x] =  newCar2.letter
                    newCar2.y = newCar2.y+ 1
                    possibleStates.append(newState2)
            # Go down length 2
            if car.length == 2 and car.y < 4:
                if currState.board[car.y+2][car.x] == '-':
                    newBoard2 = deepcopy(currState.board)
                    newCars2 = deepcopy(currState.cars)
                    newState2 = State(newBoard2, currState, newCars2)
                    newCar2 = newState2.cars[carCount] 
                    newState2.board[newCar2.y][newCar2.x] = '-'
                    newState2.board[newCar2.y+2][newCar2.x] =  newCar2.letter
                    newCar2.y = newCar2.y+ 1                
                    possibleStates.append(newState2)                 
    return possibleStates


# Used to reverse the goal path
def reverse(st):
    return st[::-1]


