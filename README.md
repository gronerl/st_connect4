# Design & Programming Exercise: Connect Four 
## Solution by Linus Groner
This repository contains my (Linus Groner's) solutions to the Connect Four assignment as part of the hiring process at S[&]T Corporation, Delft.

This readme file will serve as a place to collect design information and information on the thought process, as well as track the requirements of the assignment. 

## Requirements and how they are met

### Hard implementation requirements 

#### The program starts with an empty board and displays this on screen. This can be done in any way you like as long as it is clear. For instance, you can just print a few lines to stdout on the command line.
#### The program asks the human in which column they want to drop the disc. It should then update the board with this move, and display or print the board again.
#### After this the computer plays a (random) move and the board is updated and printed again.
#### After every move it must be checked if the move did connect four discs, either horizontally, vertically or diagonally. If it did, the player who played this move is declared the winner and the program exits.
#### Repeat this until a player has won or until the board is full. In the last case the game is declared a draw.
#### The program can be a simple command line program but it doesn't have to be. If you prefer a GUI, web-application, etc., feel free to implement that. But you must be able to show a running version of your program at the interview

### Language and Framework requirements

#### Write in a language supporting OO-programming, to model the game in classes.
I chose to use Python since it is the language that I am most used to and will have to spend the least time figuring out how to do a given thing. 

#### Add a set of relevant tests that either use a testing framework or that can be executed using a specific option of the main program.
I chose to use pytest again for the reason that it is a framework I used and liked in the past.

### Documentation and Submission
Please mail back the assignment containing:

#### The time you spent on the assignment:
1.5h writing this and designing with pencil and paper

#### Treat the comments and documentation as if you are delivering to a customer:
* Rationale of implementation can go inside the code
* Write a small accompanying text listing the things you would do if you were
  to spend more time on this project, including:
  * Work still to be done
  * Bugs / non-working use cases
  * Improvements and new features you might want to add later

## Analysis of the task
The requirements file describes a process as follows:

0. initialize empty board
1. print/display board
2. collect user input
3. print/display updated board
4. check winning condition (exit if met)
5. compute computer input
6. collect user input
7. print/display updated board
8. check winning condition (exit if met)
9. repeat from 1.

Different components that appear in this workflow are:
* Input: User input
* Output: Display board and declare winner
* Computer Strategy
* Check winning conditions
* Representation of game state
* Actions / update of game state

Further, we will want the following components:
* input validation
* 

I categroize as follows:
* input: input validation (selecting move)
* output
* strategy (user, computer)
* game state, move validation (game-state dependent)
To the game, there is no difference who the 

Possible extensions (brain storming):
* game:
  * \# of players/colors
  * grid shape
  * dimensionality of grid
  * winning condition (e.g. periodic boundaries)
  * game "physics" (now, fall down, ...)
* strategy:
  * network players
  * simulating strategies: facilitate efficiently playing an abundance of scenarios to feed an algorithm picking moves
  * non-local strategies: 
    access to game history or history of moves of a given player across games
  * code isolation: make it "impossible" to access certain API from e.g. strategies

The requirements file already hints at some possible extensions, those should be easiest to implement and be directly compatible with the chosen design:
* Different visuals
* Alternative computer strategies 

Further considerations:
* If two human players are present (locally), certain updates, such as the winning declaration, need only to be presented once. However, for a computer player would not have to be informed at all, while e.g. in the case of a network player, each player needs to be informed separately, while in this case information such as "waiting for player A to make his turn" could be transmitted. This could be handled by adding a "terminal" concept. 