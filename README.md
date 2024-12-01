# Design & Programming Exercise: Connect Four 
This repository contains my (Linus Groner's) solutions to the Connect Four assignment as part of the hiring process at S[&]T Corporation, Delft.

## How to Install and Run

The code was developed and tested using python 3.12. I recommend to always use a virtual environment.
This python project can be installed using pip with

```
cd $CONNECT_4_DIR
pip install .
connect4 # pip should install this entrypoint in your venv
```

To run the tests or for a development install, run 

```
cd $CONNECT_4_DIR
pip install -U setuptools wheel pip# always a good idea
pip install -r ./requirements-dev.txt
pip install -e .
pytest ./tests
```

## Brief Documentation and Further Work 
The connect 4 game is functionally complete as per the requirements. 

However, testing is not thorough.

There are three main (sub)classes, taking care of, respectively:
* `Connect4` in `game.py`: Captures the game state and its transitions
* `Player` in `game.py`: Subclasses implement strategies, including the human player and the random computer player
*  `Connect4TextTerminal` in `terminal.py`: Handles printing and reading input to/from stdin/stdout. This is separate from `Player`, since some print outs are not per player but rather 

Further refactorings could e.g. 
* extract the `play` method from `Connect4` class. Currently it is hard to test specific steps of the game, while still keeping test coverage of the driver. A solution could be to create a facade that provides as the entry point, while also maintaining an easier construction of the objects in a feasible way.
* the 'x' and 'o' player labels are fairly hard-coded and might hinder certain extensions

The tests are only a sketch of what the intention would be. The idea is to allow unit testing of the above discussed classes, as well as having tests of the listed requirements, as end-to-end tests. Currently only minimal tests for `Connect4` and the terminal are implemented. 

To summarize, further work:
* Extend testing
* Factoring out `play` of `Connect4`, possibly introduce a Facade class
* The design should be able to handle reasonably well extensions like:
  * New player strategies, such as new computer players, 
  * Generalization of the game (e.g. different winning conditions, grid sizes, grid dimensions, "physics" as opposed to currently gravity, number of players)
  * New frontends, e.g. gui or ncurses


## Time Spent:
All in all roughly 12 hours. 