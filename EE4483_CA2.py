#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Develop a program that uses heuristic search to play the tic-tac-toe game (Fig. 4.1 in our slides).
To interact with the program, a visual interface is preferred but not necessary, e.g., the input of
the user and the response of the computer can be simply as (x,y), where x and y indicate the
spatial location at the chess board. (10 points)
"""

import numpy as np
import sys
from copy import copy

rows=3
cols=3
board=np.zeros((rows,cols))
# 0 = blank
# 1 = 'x'
# 2 = 'o'
inf=9999999
neg_inf=-9999999
searchDepth=1 #control search depth


def printBoard():
    for i in range(0,rows):
        for j in range(0,cols):
            if board[i,j]==0:
                print(" _ ",end=" ")

            elif board[i,j]==1:
                print(" X ",end=" ")
            else:
                print(" O ",end=" ")        
        print ()


#the heuris function 
winningStates=np.array([[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]])

def scoreOfState(boardState):   
    stateCopy=copy(boardState.ravel())
    heuristic=0
    for i in range(0,8):
        maxp=0
        minp=0
        for j in range(0, rows):
            if stateCopy[winningStates[i,j]]==2: # o wins
                maxp+=1
            elif stateCopy[winningStates[i,j]]==1: # x wins
                minp+=1
        
        if minp == 0:
            heuristic += 1
        if maxp == 0:
            heuristic += -1 
        if maxp==2 and minp ==0:
            heuristic += 2
        if minp==2 and maxp ==0:
            heuristic += -2
        if maxp==2 and minp ==1:
            heuristic += -5
        if minp==2 and maxp ==1:
            heuristic += 5              
        if maxp==3:
            heuristic += 10
        if minp==3:
            heuristic += -10
            
    return heuristic

def checkGameOver(boardState):
    stateCopy=copy(boardState.ravel())
    for i in range(0,8):
        maxp=0
        minp=0
        for j in range(0, rows):
            if stateCopy[winningStates[i,j]]==2: # o wins
                maxp+=1
            elif stateCopy[winningStates[i,j]]==1: # x wins
                minp+=1
           # print(maxp, minp)    
            if maxp == 3:
                return -1
            if minp == 3:
                return 1
    return 0

def minimax(boardState,alpha,beta,isMax,depth):    
    if depth==0:
        return scoreOfState(boardState),boardState
    
    left=np.where(boardState==0)
    
    returnState=copy(boardState)
    if len(left[0])==0: #nothing empty
        return scoreOfState(boardState),returnState
        
    if isMax==True:
        score=neg_inf
        for i in range(0,len(left[0])):
            nextState=copy(boardState)
            nextState[left[0][i],left[1][i]]=2
            Nscore,Nstate=minimax(nextState,alpha,beta,False,depth-1)
            if Nscore > score:
                score=Nscore
                returnState=copy(nextState)
            if score > alpha:
                alpha=score
            if alpha >= beta:
                #pruned
                break;


        
        return score,returnState

    else:
        score=inf
        for i in range(0,len(left[0])):
            nextState=copy(boardState)
            nextState[left[0][i],left[1][i]]=1
            Nscore,Nstate=minimax(nextState,alpha,beta,True,depth-1)
            if Nscore < score:
                score = Nscore
                returnState=copy(nextState)
            if score < beta:
                beta=score
            if alpha >= beta :
                #pruned
                break;


        return score,returnState
        

       
def main():
    num=int(input('enter player num (1 or 2), 1 starts first: '))
    gameOver=0
    global board
    for turn in range(0,rows*cols):
       
        if (turn+num)%2==1: #make the player go first, and make the user player as 'X' min
            valid = False 
            while not valid:
                print('Your Turn')    
                r,c=[int(x) for x in input('Enter your move in row(1,2,3) and col(1,2,3): ').split(' ')]
                #cannot rewrite the board
                if board[r-1,c-1]!=0:
                    print('invalid move, try again')
                    continue
                valid = True
                board[r-1,c-1]=1
                printBoard()
                gameOver=checkGameOver(board)
                if gameOver==1:
                    print ('U win.Game Over')
                    sys.exit()
            print ()
        else: #its the computer's turn make the PC always put a 'O' max
            print('AI\'s Turn')
            state=copy(board)
#            print(searchDepth)
            score,nextState=minimax(state,neg_inf,inf,True,searchDepth)
            board=copy(nextState)
            printBoard()
            print ()
            gameOver=checkGameOver(board)
            if gameOver==-1:
                print ('PC wins.Game Over')
                sys.exit()
        
    print ('It\'s a draw')

main()