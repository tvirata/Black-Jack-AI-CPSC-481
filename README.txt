CPSC 481 Capstone Project - Blackjack AI - by Mohammed Ali and Tonirose Virata

---------------
# Description #
---------------
Our Blackjack AI game is designed to show how to train a computer AI to play Blackjack. This Blackjack game has two game modes: one for the computer AI to play against the dealer (training simulation) and another mode for the user to play against the dealer. We implemented machine learning to show how our computer AI is learning how to play Blackjack on its own.

----------
# Layout #
----------
Within our Blackjack game, there are multiple folders and source files.
- Card Directory: holds all the GUI resource files
	- Dealer: holds images for dealer's cards
	- Player: holds images for player's cards
- Fonts Directory: holds different fonts for the game
- Statistics Directory: holds all the graphical statistics showing the machine learning of the computer AI
- Main Directory
	- BlackJack.py: This file is where the game is ran. The main function is located in this python file.
	- cardClass.py: This file contains the Card class functions that are used as objects within the BlackJack.py file.
	- plot_utils.py: This file contains the functions needed to create graphs for visual analysis for machine learning of the Computer AI.
- Documentation file: Full explanatory report of the Blackjack AI project.

------------------
# How to Install #
------------------
Step 1: Install Python, numpy, pygame, matplotlib. Use an IDE to run the code, ideally use Visual Studio Code.
Step 2: When in your IDE, run the program through BlackJack.py
Step 3: While game is running, go into the terminal to select an option.
Step 4: When you type the ai option, the training simulation will load for the computer AI.
Step 5: When you type the game option, it will prompt to ask for your name. After entering your name, the game will load such that you are playing against the dealer. 

----------------------
# General Operations # 
----------------------
- Betting chips on the side will allow the player to bet how ever much they want depending on how much money they have in their bank. The user is not able to over bet depending on how much money they have in their bank.
- Audio Button allows for users to play or mute the in-game sound while playing the game. 
- The user is able to see how many rounds the dealer or them have won, and see how many games they have played. 
- When in AI mode, a graph will be shown after certain rounds. You can also press "P" to generate a plot at any moment.

---------------------
# Button Operations #
---------------------
- R: reset the current game
- P: plot the current plot
- W: print games won/lost
- T: reset the win/lose numbers
- H: do a hit (not in AI mode)
- S: do a stick (not in AI mode)
- V: turn on/off volume of game

----------------------
# Betting Operations #
----------------------
- 1 Dollar Chip: add 1 dollar to the bet amount and minus 1 dollar from the bank
- 5 Dollar Chip: add 5 dollars to the bet amount and minus 5 dollars from the bank
- 10 Dollar Chip: add 10 dollars to the bet amount and minus 10 dollars from the bank
- 20 Dollar Chip: add 20 dollars to the bet amount and minus 20 dollars from the bank
- 50 Dollar Chip: add 50 dollars to the bet amount and minus 50 dollars from the bank
- 100 Dollar Chip: add 100 dollars to the bet amount and minus 100 dollars from the bank
- 500 Dollar Chip: add 500 dollars to the bet amount and minus 500 dollars from the bank
- 1000 Dollar Chip: add 1000 dollars to the bet amount and minus 1000 dollars from the bank
- 10000 Dollar Chip: add 10000 dollars to the bet amount and minus 10000 dollars from the bank
- 100000 Dollar Chip: add 100000 dollars to the bet amount and minus 100000 dollars from the bank
- 1000000 Dollar Chip: add 10000000 dollars to the bet amount and minus 1000000 dollars from the bank 
- When bank is 0 or if player trying to bet more then the amount they have in the bank they game will pop insufficient fund