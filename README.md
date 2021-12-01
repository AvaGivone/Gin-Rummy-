# Gin-Rummy-
Gin Rummy (College Freshman- Fall 2021)  with 2 Player and AI (rendition of hand-built strategy) modes. Carnegie Mellon University CS 15112 Term Project in Python. 
Description: 
For my term project, I created Gin Rummy. This is a two player game where the object of the game is to be the first player to reach 100 
points through numerous rounds of play. Play consists of players, one at a time, picking up a card from either the deck or the top card 
from the pile. The player tries to create melds, or sets, of minimum 3 cards which must be of the same suit in an ascending sequence or 
the same number from each suit. If the player has gin, meaning all of their 10 cards are in melds or they have no unmatched cards 
(unmatched cards are cards that don't fit into one of the player's melds), then they can simply win that round. Before points are totaled, 
their opponent gets the opportunity to match their unmatched cards to the other player's melds. Whoever called gin would then get the point 
value of however many of their opponents cards are unmatched plus 20 points. The player can also knock, meaning that their unmatched cards 
have point values of less than 10. In this case, either player can win the round as the winner will be whoever has the lower point value of 
unmatched cards (if they are equal amounts, the person who did not knock wins the round). If the winner is the player who knocked, they 
receive the point value of the difference in unmatched cards. If the winner is the player who did not knock then they receive an additional 
10 points to the unmatched difference. In this rendition of Gin Rummy, players can either play against each other, or against an AI opponent.
For a more thorough explanation, check out the rules button in my project! :) 

How to Run Gin Rummy: 
User should run the file "agtermproject.py" as the main file. However, users should note that this file uses the following source files: 
cmu_112_graphichs.py, testFuncs.py, and AI.py. The game also derives images and sound effects from the source files entitled, PNG and sounds.
All of these elements should be housed in a single folder for the game to work properly. Controls for game itself can be found in main file 
or when running the program through the question mark button. 

Shortcut Demands: 
There are no shortcut demands, but there is one series of print statements commented out of the main file which allow the user to view the 
AI's hand, needs, and discards in real time. 
