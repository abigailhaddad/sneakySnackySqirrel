# -*- coding: utf-8 -*-
"""
This runs sneaky snacky squirrel with n computer players

"""

import random
from statistics import mean

def makeColorList():
    # this is the list of colors you have to fill in to win
    colorList=["RED", "GREEN", "BLUE", "PURPLE", "YELLOW"]
    return(colorList)

def spin():
    # this returns a random spin result
    colorList=makeColorList()
    nonColorOptions=["one", "two", "steal", "lose", "skip"]
    allOptions=nonColorOptions+colorList
    toReturn=random.sample(allOptions, 1)[0]
    return(toReturn)

def printSpin(player, spinResult):
    print(f'Player {player} spun a {spinResult.upper()}')
    
def produceLose(playerBoard):
    # makes all your board values=0
    playerBoard = {x: 0 for x in playerBoard }
    return(playerBoard)
    
def takeTurn(stateOfBoard, player):
    playerBoard=stateOfBoard[player]
    colorList=makeColorList()
    spinResult=spin()
    playerTake=""
    printSpin(player, spinResult)
    get=[]
    missings=[key for (key,value) in playerBoard.items() if value ==0]
    if spinResult in colorList:
        get.append(spinResult)
    elif spinResult=="lose":
        playerBoard = produceLose(playerBoard)
    elif (spinResult=="one") or (spinResult=="two" and len(missings)==1):
        get=get+(random.sample(missings, 1))
    elif spinResult=="two":
        get=get+random.sample(missings, 2)
    elif spinResult=="steal":
        replace, playerTake=steal(player, stateOfBoard, missings)
        if playerTake!="none":
            get.append(replace)
            stateOfBoard[playerTake][get[0]]=0
    for color in get:
        playerBoard[color]=1
    stateOfBoard[player]=playerBoard
    stateChanges(missings, player, get, spinResult, playerTake)
    return(stateOfBoard)
    
def stateChanges(missings, player, get, spinResult, playerTake):
    #this kind of didn't work
    gotten=[i for i in get if i in missings]
    if spinResult=="steal" and len(gotten)>0:
        print(f'Player {player} stole a {gotten[0]} from Player {playerTake}')
    elif spinResult=="lose":
        colorList=makeColorList()
        losts=[i for i in colorList if i not in missings]
        for lost in losts:
            print(f'Player {player} lost a {lost}')
    else:
        for got in gotten:
            print(f'Player {player} drew a {got}')


def startState(n):
    # creates start state - dictionary of dictionaries
    listOfColors= makeColorList()
    initialState={}
    for number in range(0,n):
        #because mutability/dictionaries
        listOfValues = [0] * len(listOfColors)
        initialState[number]=dict(zip(listOfColors, listOfValues))
    return(initialState)

def evaluateWin(state):
    # evaluates whether any of the players have their boards filled in
    colorList=makeColorList()
    for number in range(0, len(state)):
        if sum(state[number].values())==len(colorList):
            return("win")
        else:
            pass

def steal(player, stateOfBoard, missings):
    #we are going to sort the other players by how well they're doing
    #and then steal from the one with the most items who also has an item we want
    biggestSum=0
    replace=[]
    playerTake="none"
    for checkPlayer in range(0, len(stateOfBoard)):
        if player!=checkPlayer:
            theirBoard= stateOfBoard[checkPlayer]
            theirSum=sum(theirBoard.values())
            for missing in missings:
                if theirBoard[missing]==1 and theirSum>biggestSum:
                    biggestSum=theirSum
                    replace=missing
                    playerTake=checkPlayer
    return(replace, playerTake)
                    
def main(n):
    # this runs one game until someone wins
    state=startState(n)
    turnNumber=0
    while evaluateWin(state)!="win":
        player=turnNumber % n
        state=takeTurn(state, player)
        turnNumber=turnNumber+1
    print(f'Player {player} won on turn {turnNumber}')
    return(turnNumber, player)
        
def testIt(count):
    #how big of an advantage is starting first?
    #how much does time to end vary with number of players
    results={}
    for n in range(1, 5):
        results[n]=[ main(n) for i in range(0,count)]
    for n in range(1,5):
        averageLengthGame=mean([i[0] for i in results[n]])
        print("average game length", n, averageLengthGame)
        numberFirstPlayer=len([i[1] for i in results[n] if i[1]==0])
        maxTurns=max([i[0] for i in results[n]])
        print("maximum turns", maxTurns)
        percentOverExpected=round(numberFirstPlayer/count-(1/n),2)
        print(numberFirstPlayer/count)
        print("first player advantage",percentOverExpected )
    return(results)
        
#results=testIt(10000)
main(1)
#testIt(100)

"""



"""
