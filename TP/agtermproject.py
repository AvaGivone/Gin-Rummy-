'''
    Gin Rummy 
    By: Ava Givone 
    Andrew ID: agivone 
    15112 Term Project F21

    Project description: 
    Checkpoints: 
        1. Preliminary setup 
        2. Game screen which draws player hand and the deck and allows player to pick up and maneuver their cards
            - Call functions that check if players hand (in that order) permits Gin or Knocking  
        3. Player can rearange their cards 
        4. Player needs ability to discard
        5. Player can knock or gin (must test these conditions)
        6. Tally player score
            - Knock: difference of unmatched cards (non-knocker gets extra 10 points if win)
            - Gin: player gets 20 points plus unmatched cards
        7. First player to get 100 points wins 
'''

'''
Game operation notes: 
      - To select a card from the deck or pile, simply click on it 
      - To swap the positions of two cards in a hand, click on one card, press left or right arrow to move card left or right, 
            press enter to lock card in
      - To choose a card to put on pile, select it then press 

'''
import random, math, string, time, copy
import cmu_112_graphics
import testFuncs
from cmu_112_graphics import *
from PIL import Image, ImageTk
from testFuncs import *
import soundEffects
from soundEffects import *

def appStarted(app):
      '''Citations: 
            Images:
            app.imgHome
                  https://acbl.mybigcommerce.com/table-playing-images/
            app.backArrow 
                  https://www.pngkit.com/bigpic/u2q8a9y3t4u2y3t4/ 
            app.rulesImage
                  https://bicyclecards.com/how-to-play/500-rum/ 
            app.guideImage 
                  https://www.coolgenerator.com/png-text-generator 
            Fonts:
            fancyLetters(): 
                  https://lingojam.com/FancyTextGenerator 
            
      '''
      app.imgHome = app.loadImage('PNG/home.png')
      app.imgBackArrow = app.loadImage('PNG/backArrow.png')
      app.rulesImage = app.loadImage('PNG/rules.png')
      app.cardBack = app.loadImage('PNG/back.png')
      app.cardHalo = app.loadImage('PNG/halo.png')
      app.guideImage = app.loadImage('PNG/guide.png')
      app.homeScreen = True
      app.welcomeScreen = True
      app.rulesScreen = False
      app.startScreen = False
      app.helpScreen = False
      app.gameScreen = False
      app.newRound = False 
      app.gameOver = False
      app.rulesSelected = (1, 30)
      app.startSelected = (1, 30)
      app.player1Name = 'Enter name'
      app.player2Name = 'Computer'
      app.hoverStart = 'black'
      app.aiModeOn = True
      app.player = True #True means player 1, False means player 2
      app.playerHands = {}
      app.playerNames = {}
      #This dictionary keeps track of whether the player is eligible or not for gin or knocking 
            #[False, False] --> [has gin, can knock]
      app.playerStatus = {
                        1:(False, False),
                        2:(False, False)
                        }
      app.playerScores = {
                        1:0,
                        2:0
                        }
      app.pile, app.deck = makeInitDeck(app)
      app.deckHalo, app.pileHalo = False, False
      app.imageDict = imageDictionary()
      app.swapOn = False 
      app.passPlayer = False
      app.firstPassPlayer = False
      app.roundWinner = ''
      app.winner = ''
      app.hoverButton = 'black'
      app.roundNumber = 1
      app.aiNeeds = []
      app.aiPlan = []
      app.aiDiscards = []
      app.roundLength = 0
      

      #This is the audio 
      app.shuffleSound = getSound("sounds/deckShuffle.mp3")
      app.cardSound = getSound("sounds/cardMoving.mp3")
      

class Card():
      #Class which makes all 52 cards in the deck objects 
      def __init__(self, name, hovered, selected):
            self.name = name
            self.imagePath = 'PNG/' + name + '.png'
            self.hovered = hovered
            self.selected = selected
      def pointVal(self):
            vals = ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A']
            points = [10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 10]
            val = self.name[:-1]
            ind = vals.index(val)
            return points[ind]
      def __eq__(self, other):
            return self.name == other.name
      def __repr__(self):
            return f'{self.name}'

def loadCardImage(app, imageName, size):
      #This function allows the image of a card to be loaded at any point in the MVC
      image = Image.open(imageName)
      formattedImage = image.resize(size)
      return formattedImage

def invalidName(s):
      #Returns whether or not the string given by the user is valid for use 
      for chr in s: 
            if chr not in string.ascii_letters:
                  return True
      return False 

def tempResizeImage(imagePath):
      #Temporarily resizes image when the image is hovered over by mouse 
      size = (196 + 20, 300 + 20)
      copyImage = Image.open(imagePath)
      tempImage = copyImage.resize(size)
      return tempImage

def imageDictionary():
      #Generates a dictionary of the card images 
      cardNames = []
      size = (196, 300)
      imageDict = dict()
      suits = ['C', 'D', 'S', 'H']
      vals = ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A']
      for suit in suits:
            for value in vals:
                  cardNames.append(value+suit)
      for name in cardNames: 
            path = 'PNG/' + name + '.png'
            image = Image.open(path)
            imageDict[name] = image.resize(size)
      return imageDict

def fancyLetters(s):
      #Helper function that converts ordinary text into the formatted themed text
      fancyLetters = '𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ'
      newS = ''
      for letter in s:
            if letter.isalpha():
                  newS += fancyLetters[string.ascii_letters.find(letter)]
            else: 
                  newS += letter
      return newS

def makeInitDeck(app):
      #Function creates a deck of 52 cards 
      cardNames = []
      cardObjects = []
      suits = ['C', 'D', 'S', 'H']
      vals = ['K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2', 'A']
      for suit in suits:
            for value in vals:
                  cardNames.append(value+suit)
      random.shuffle(cardNames)
      for i in range(len(cardNames)):
            cardObjects.append(Card(cardNames[i], False, False))
      return [cardObjects[0]], cardObjects[1:]

def keyPressed(app, event):
      if app.gameScreen == True:
            if app.player == True: player = 1
            else: player = 2
            if app.newRound == True:
                  if event.key == 'c':
                        playSound(app.shuffleSound)
                        app.roundWinner = ''
                        app.newRound = False
            if app.player == True or (app.player == False and app.aiModeOn == False): 
                  handSize = len(app.playerHands[player])
                  movingIndex = None
                  for i in range(len(app.playerHands[player])):
                        if app.playerHands[player][i].selected == True:
                              movingIndex = i
                  if movingIndex != None:
                        movingCard = app.playerHands[player][movingIndex]
                  if event.key == 'Right':
                        if movingIndex != None and movingIndex < handSize - 1:
                              app.playerHands[player].pop(movingIndex)
                              app.playerHands[player].insert(movingIndex + 1, movingCard)
                              playSound(app.cardSound)
                              
                  if event.key == 'Left':
                        if movingIndex != None and movingIndex > 0:
                              app.playerHands[player].pop(movingIndex)
                              app.playerHands[player].insert(movingIndex - 1, movingCard)
                              playSound(app.cardSound)
                            

                  if event.key == 'Return':
                        if movingIndex != None:
                              #if movingCard != None:
                              movingCard.selected = False
                              #YOU CAN CHECK HAND CONDITIONS WHEN THEY REARRANGE DECK
                              app.playerStatus[player] = (checkGin(app.playerHands[player]), checkKnock(app.playerHands[player])) 
                              if app.playerStatus[player][0] == True: app.playerStatus[player][1] == False

                  #If they push the up key, then they want to discard a card to pile 
                  if event.key == 'Up':
                        #Player can only discard if they have already picked up 
                        if handSize == 11 and movingIndex != None:
                              app.playerHands[player].pop(movingIndex)
                              app.pile.append(movingCard)
                              #Switch the player turn 
                              app.passPlayer, app.player = True, not app.player
                              


def mouseMoved(app, event):
      if app.homeScreen == True:
            #Changes the model view of the home screen 
            if app.welcomeScreen == True:
                  if (event.x >= app.width/2 - 100 and 
                  event.x <= app.width/2 + 100 and event.y >= app.height/2 and 
                  event.y <= app.height/2 + 50): 
                        app.rulesSelected = (5, 40)
                        app.startSelected = (1, 30)
                  elif (event.x >= app.width/2 - 100 and 
                  event.x <= app.width/2 + 100 and event.y >= app.height/2 + 100
                  and event.y <= app.height/2 + 150): 
                        app.startSelected = (5, 40)
                        app.rulesSelected = (1, 30)
                  else: 
                        app.rulesSelected = (1, 30)
                        app.startSelected = (1, 30)
            if app.startScreen == True: 
                  if (event.x >= app.width/2 - 100 and event.x <= app.width/2 + 100 
                        and event.y >= app.height - app.height/3 + 100 and 
                        event.y <= app.height - app.height/3 + 150):
                        app.hoverStart = 'white'
                  else: 
                        app.hoverStart = 'black'

      #Operations on the game screen 
      if app.gameScreen == True: 
            if app.player == True: player = 1
            else: player = 2
            if app.player == True or (app.player == False and app.aiModeOn == False):
                  #Can only access the deck or pile if you have 10 cards
                  if app.helpScreen == False:
                        if len(app.playerHands[player]) == 10:
                              if event.x >= 284 and event.x <= 298 + 196 and event.y >= 25 and event.y<= 325:
                                    app.deckHalo, app.pileHalo = True, False 
                              elif event.x >= 284 + 196 + 40 and event.x <= 284 + 196 + 40 + 196 and event.y >= 25 and event.y<= 325:
                                    app.deckHalo, app.pileHalo = False, True
                              else: 
                                    app.deckHalo, app.pileHalo = False, False 

                        #When scrolling over the player hand, checks which card user is hovering over 
                        width = 850/(len(app.playerHands[player]) + 1) 
                        for i in range(len(app.playerHands[player])):
                              if i != len(app.playerHands[player]) - 1 and event.x >= 50 + i * width and event.x < 50 + (i+1) * width and event.y >= 375 and event.y <= 675:
                                    app.playerHands[player][i].hovered = True
                              elif i == len(app.playerHands[player]) - 1 and event.x >= 50 + i * width and event.x < 50 + (i+1) * width + 98 and event.y >= 375 and event.y <= 675:
                                    app.playerHands[player][i].hovered = True
                              else: 
                                    app.playerHands[player][i].hovered = False
                        
                        if event.x >= app.width/2 - 100 and event.x <= app.width/2 + 100 and event.y >= 710 and event.y <= 760:
                              app.hoverButton = '30'
                        else: app.hoverButton = '20'


def mousePressed(app, event):
      if app.homeScreen == True:
            #Mouse changes parameters for the welcome screen 
            if app.welcomeScreen == True:
                  if (event.x >= app.width/2 - 100 and 
                  event.x <= app.width/2 + 100 and event.y >= app.height/2 and 
                  event.y <= app.height/2 + 50): 
                        app.welcomeScreen = False
                        app.rulesScreen = True
                        app.startScreen = False 
                  elif (event.x >= app.width/2 - 100 and 
                  event.x <= app.width/2 + 100 and event.y >= app.height/2 + 100
                  and event.y <= app.height/2 + 150): 
                        app.welcomeScreen = False
                        app.rulesScreen = False 
                        app.startScreen = True

            #Mouse changes parameters for the rules screen 
            if app.rulesScreen == True:
                  if (event.x >= 5 and event.x <= 55 and event.y >= 5 and 
                  event.y <= 45):
                        app.rulesScreen = False
                        app.welcomeScreen = True
                        app.rulesSelected = (1, 30)

            #Mouse changes parameters for the start screen 
            if app.startScreen == True:
                  if (event.x >= 5 and event.x <= 55 and event.y >= 5 and 
                  event.y <= 45):
                        app.startScreen = False
                        app.startSelected = (1, 30)
                        app.welcomeScreen = True
                  if (event.x >= app.width/2 - 100 and event.x <= app.width - 90 
                        and event.y >= app.height/2 and event.y <= app.height/2 + 10):
                        app.aiModeOn = True
                        app.player2Name = 'Computer'
                  if (event.x >= app.width/2 + 60 and event.x <= app.width/2 + 70 
                        and event.y >= app.height/2 and event.y <= app.height/2 + 10):
                        app.aiModeOn = False
                        app.player2Name = 'Enter name'
                  
                  #Input the player names 
                  if (event.x >= app.width/3 - 90 and event.x <= app.width/3 + 90 
                        and event.y >= app.height/2+120 and event.y <= app.height/2 + 150):
                        app.player1Name = app.getUserInput("Player 1")
                        if app.player1Name == None or app.player1Name == '' or invalidName(app.player1Name):
                              app.player1Name = 'Enter name' 
                        
                  if app.aiModeOn == False: 
                        if (event.x >= app.width-app.width/3-90 and 
                              event.x <= app.width - app.width/3+90 and 
                              event.y >= app.height/2+120 and event.y <= app.height/2+150):
                              app.player2Name = app.getUserInput("Player 2")
                              if app.player2Name == None or app.player2Name == '' or invalidName(app.player2Name):
                                  app.player2Name = 'Enter name' 
                                  
                  #Start button that takes player to new view 
                  if (event.x >= app.width/2 - 100 and event.x <= app.width/2 + 100 
                        and event.y >= app.height - app.height/3 + 100 and 
                        event.y <= app.height - app.height/3 + 150):
                        playSound(app.shuffleSound)
                        app.startScreen = False
                        app.homeScreen = False
                        app.playerHands = {
                                          #GIVE THE PLAYERS A HAND OUT OF THE DECK 
                                          #Deals 10 cards to each player
                                          1:getInitHand(app), 
                                          2:getInitHand(app)
                                          }
                        app.playerNames = {
                                          1:app.player1Name,
                                          2:app.player2Name
                                          }

                        app.firstPassPlayer = True
                        app.gameScreen = True
                        if app.aiModeOn == True:
                              app.aiNeeds, app.aiDiscards = aiSetup(app)
                              while len(app.aiNeeds) != len(app.aiDiscards):
                                    reset(app)
                        #Make sure no cards got selected when you pressed start 
                        for card in app.playerHands[1]:
                              card.hovered, card.selected = False, False

      if app.gameScreen == True:
            if app.player == True: player = 1
            else: player = 2
            if app.player == True or (app.player == False and app.aiModeOn == False):
                  #Player can only choose from deck or pile if they have 10 cards in hand 
                  if app.helpScreen == False: 
                        if len(app.playerHands[player]) == 10:
                              #If the player chooses from the deck 
                              if event.x >= 284 and event.x <= 298 + 196 and event.y >= 25 and event.y<= 325:
                                    chosenCard = app.deck.pop()
                                    app.playerHands[player].append(chosenCard)
                                    app.deckHalo = False
                                    checkDeckRestock(app)
                              #If the player chooses from the pile 
                              if event.x >= 284 + 196 + 40 and event.x <= 284 + 196 + 40 + 196 and event.y >= 25 and event.y<= 325:
                                    chosenCard = app.pile.pop()
                                    app.playerHands[player].append(chosenCard)
                                    app.pileHalo = False
                        
                        #This is code for selecting two cards to swap positions 
                        width = 850/(len(app.playerHands[player]) + 1) 
                        for i in range(len(app.playerHands[player])):
                              if i != len(app.playerHands[player]) - 1 and event.x >= 50 + i * width and event.x < 50 + (i+1) * width and event.y >= 375 and event.y <= 675:
                                    app.playerHands[player][i].selected = True
                              elif i == len(app.playerHands[player]) - 1 and event.x >= 50 + i * width and event.x < 50 + (i+1) * width + 98 and event.y >= 375 and event.y <= 675:
                                    app.playerHands[player][i].selected = True
                              else: 
                                    app.playerHands[player][i].selected = False
                        
                        #Checks if the player elected to knock or call gin 
                        if event.x >= app.width/2 - 100 and event.x <= app.width/2 + 100 and event.y >= 710 and event.y <= 760:
                              #If the player chooses one of these things, then compute the score at the current state 
                              if app.playerStatus[player][0] == True or app.playerStatus[player][1] == True:
                                    roundEndedActions(app)
                        
                  #If player pushed the help button 
                  if event.x >= app.width - 80 and event.x <= app.width-20 and event.y >= app.height-80 and event.y <= app.height - 20:
                        app.helpScreen = True
                  if app.helpScreen == True and event.x >= 305 and event.x <= 355 and event.y >= 206 and event.y <= 244:
                        app.helpScreen = False

      if app.gameOver == True: 
            #This is the restart button 
            if event.x >= app.width/2 - 100 and event.x <= app.width + 100 and event.y >= app.height/3 + 150-25 and event.y <= app.height/3 + 150 + 25:
                  appStarted(app)
            
                  
def checkDeckRestock(app):
      #If the deck runs out of cards, this function takes all the cards from the pile and reshuffles them to put into the deck
      #leaving the top card of the pile only 
      if len(app.deck) == 0:
            for i in range(len(app.pile) - 1):
                  app.deck.append(app.pile[i])
            last = app.pile.pop()
            app.pile = [last]
            shuffle(app.deck)

def timerFired(app):
      if app.aiModeOn == True and app.player == False: 
            #Here is where the AI carries out its moves 
            app.playerStatus[2] = checkAIGinOrKnock(app)
            if app.playerStatus[2][0] == True or app.playerStatus[2][1] == True: 
                  roundEndedActions(app)
            elif app.playerStatus[2][0] != True and app.playerStatus[2][1] != True: 
                  aiMoveHelper(app)
                  '''NOTE: The following print statements show what AI has/needs/will discard
                  print(app.playerHands[2])
                  print(app.aiNeeds)
                  print(app.aiDiscards)'''
                  time.sleep(1)
                  checkDeckRestock(app)
                  app.player = True
      #Passing players and round transition screens 
      if app.firstPassPlayer == True: 
            time.sleep(1)
            app.firstPassPlayer = False 
            app.gameScreen = True
      if app.passPlayer == True and app.newRound == False: 
            app.passPlayer = False
            time.sleep(2)
            app.roundLength += 1

def drawHome(app, canvas):
      #Draws the three pages of the home screen, the welcome page, the rules 
      #page and the start page where players input their name for play 
      if app.welcomeScreen == True:
            #Draws the welcome page which allows player to see rules or start 
            canvas.create_image(app.width/2, app.height/2, 
                  image=ImageTk.PhotoImage(app.imgHome)) 

            canvas.create_rectangle(app.width/2 - 400, app.height/3 - 50, 
                  app.width/2 + 400, app.height/3 + 55, fill='white', width=5, outline='white')
            canvas.create_text(app.width/2, app.height/3, text=fancyLetters('Gin Rummy'), 
                  fill='#a92500', font=('Gothic', '60', 'bold'))

            canvas.create_rectangle(app.width/2 - 100, app.height/2, 
                  app.width/2 + 100, app.height/2 + 50, fill='white', 
                  width=app.rulesSelected[0], outline='white',)
            canvas.create_text(app.width/2, app.height/2 + 25, text=fancyLetters('Rules'), 
                  fill='#a92500', font=('Gothic', f'{app.rulesSelected[1]}', 
                  'bold'))
            canvas.create_rectangle(app.width/2 - 100, app.height/2 + 100, 
                  app.width/2 + 100, app.height/2 + 150, fill='white', 
                  width=app.startSelected[0], outline='white')
            canvas.create_text(app.width/2, app.height/2 + 125, text=fancyLetters('Start'), 
                  fill='#a92500', font=('Gothic', f'{app.startSelected[1]}', 
                  'bold'))

      #Draws the rules screen on the home page 
      if app.rulesScreen == True:
            canvas.create_rectangle(0, 0, app.width, app.height, fill='#130000')
            canvas.create_rectangle(63, 0, app.width-63, app.height, 
                  fill='#510101', outline='#510101')
            canvas.create_rectangle(126, 0, app.width-126, app.height, 
                  fill='#711400', outline='#711400')
            canvas.create_image(30, 25, 
                  image=ImageTk.PhotoImage(app.imgBackArrow)) 
            canvas.create_image(app.width/2, app.height/2, 
                  image=ImageTk.PhotoImage(app.rulesImage))
            
      #Draws the start screen on the home page so player can set up the game 
      if app.startScreen == True:
            canvas.create_rectangle(0, 0, app.width, app.height, fill='#711400')
            canvas.create_rectangle(63, 0, app.width-63, app.height, 
                  fill='#510101', outline='#510101')
            canvas.create_rectangle(126, 0, app.width-126, app.height, 
                  fill='#130000', outline='#711400')
                  
            canvas.create_rectangle(app.width/2 - 300, app.height/3 - 50, 
                  app.width/2 + 300, app.height/3 + 55, fill='', width=5, outline='')
            canvas.create_text(app.width/2, app.height/3, text=fancyLetters("Gin Rummy"), 
                  fill='#a92500', font=('Gothic', '60', 'bold'))
            canvas.create_image(30, 25, 
            image=ImageTk.PhotoImage(app.imgBackArrow)) 

            #AI Mode on/off switch 
            canvas.create_text(app.width/2, app.height/2 - 40, 
                  text=fancyLetters("Computer Oponent"), fill='#a92500', font=('Gothic', 30, 
                  'bold'))
            canvas.create_text(app.width/2 - 65, app.height/2 + 5, 
                  text=fancyLetters('Yes'), fill='#a92500', font=('Gothic', 20, 
                  'bold'))
            canvas.create_text(app.width/2 + 90, app.height/2 + 5, 
                  text=fancyLetters('No'), fill='#a92500', font=('Gothic', 20, 
                  'bold'))

            if app.aiModeOn == True:
                  canvas.create_oval(app.width/2 - 100, app.height/2, 
                        app.width/2 - 90, app.height/2 + 10, fill='#FEDE17', outline='white')
                  canvas.create_oval(app.width/2 + 60, app.height/2, 
                        app.width/2 + 70, app.height/2 + 10, fill='', outline='white')
            elif app.aiModeOn == False:
                  canvas.create_oval(app.width/2 - 100, app.height/2, 
                        app.width/2 - 90, app.height/2 + 10, fill='', outline='white')
                  canvas.create_oval(app.width/2 + 60, app.height/2, 
                        app.width/2 + 70, app.height/2 + 10, fill='#FEDE17', outline='white')

            #Player 1 input 
            canvas.create_text(app.width/3, app.height/2 + 75, text=fancyLetters('Player 1'), 
                  fill='#a92500', font=('Gothic', 30, 
                  'bold'))
            canvas.create_rectangle(app.width/3 - 100, app.height/2 + 110, 
                  app.width/3 + 100, app.height/2 + 160, fill='#510101', outline='#510101')
            canvas.create_rectangle(app.width/3 - 90, app.height/2 + 120, 
                  app.width/3 + 90, app.height/2 + 150, fill='white')
            canvas.create_text(app.width/3, app.height/2 + 135, 
                  text=f'{fancyLetters(app.player1Name)}', 
                  fill='#130000', font=('Cardo, Arial', 20, 'bold'))

            #Player 2 input 
            canvas.create_text(app.width - app.width/3, app.height/2 + 75, 
                  text=fancyLetters('Player 2'), fill='#a92500', font=('Gothic', 30, 
                  'bold'))
            canvas.create_rectangle(app.width - app.width/3 - 100, 
                  app.height/2 + 110, app.width - app.width/3 + 100, 
                  app.height/2 + 160, fill='#510101', outline='#510101')
            canvas.create_rectangle(app.width - app.width/3 - 90, 
                  app.height/2 + 120, app.width - app.width/3 + 90, 
                  app.height/2 + 150, fill='white')
            canvas.create_text(app.width - app.width/3, app.height/2 + 135, 
                  text=f'{fancyLetters(app.player2Name)}', 
                  fill='#130000', font=('Cardo, Arial', 20, 'bold'))
            
            #Draws the start button once setup parameters are filled out
            if app.player1Name != "Enter name" and app.player2Name != "Enter name":
                  canvas.create_rectangle(app.width/2 - 100, app.height - app.height/3 + 100, 
                        app.width/2 + 100, app.height - app.height/3 + 150, fill=app.hoverStart, 
                        width=5, outline='white')
                  canvas.create_text(app.width/2, app.height - app.height/3 + 125, text=fancyLetters('Start'), 
                        fill='#a92500', font=('Gothic', 30, 
                        'bold'))

def drawHand(app, canvas): 
      #Draws a player's hand as it would appear on the table 
      if app.player == True or (app.player == False and app.aiModeOn == False):
            if app.player == True: 
                  player = 1
            else: 
                  player = 2
            handLen = len(app.playerHands[player])
            #Note: plus one becuase you are diplaying handLen + 1 card HALFS
            width = 850/(handLen + 1) 
            height = 350
            for i in range(handLen):
                  if not app.playerHands[player][i].hovered and not app.playerHands[player][i].selected: 
                        canvas.create_image(50 + i * width + 98, 375+150, image=ImageTk.PhotoImage(app.imageDict[app.playerHands[player][i].name]))
                  #If hovering over card adds a halo 
                  elif app.playerHands[player][i].hovered or app.playerHands[player][i].selected:
                        canvas.create_image(50 + i * width + 98, 375+150, image=ImageTk.PhotoImage(tempResizeImage(app.playerHands[player][i].imagePath)))
                        

def drawDeck(app, canvas):
      #Draws the deck and the pile (and the halo if mouse in region)
      if app.player == True or (app.player == False and app.aiModeOn == False):
            if app.deckHalo == True: 
                  canvas.create_image(284 + 98, 25 + 150, 
                        image=ImageTk.PhotoImage(app.cardHalo))
            canvas.create_image(284 + 98, 25 + 150, 
                  image=ImageTk.PhotoImage(app.cardBack)) 
            if len(app.pile) > 1:
                  canvas.create_image(284+196+40+90, 25+150,
                  image=ImageTk.PhotoImage(app.imageDict[app.pile[-2].name]))
            if app.pileHalo == True: 
                  canvas.create_image(284 + 196 + 40 + 98, 25 + 150, 
                        image=ImageTk.PhotoImage(app.cardHalo))
            if len(app.pile) >= 1:
                  canvas.create_image(284+196+40+98, 25+150, 
                        image=ImageTk.PhotoImage(app.imageDict[app.pile[-1].name]))

def drawAITurn(app, canvas): 
      #Draws the screen indicating to user that it is the AI's turn 
      canvas.create_rectangle(0, 0, app.width, app.height, fill='#711400')
      canvas.create_rectangle(63, 0, app.width-63, app.height, 
            fill='#510101', outline='#510101')
      canvas.create_rectangle(126, 0, app.width-126, app.height, 
            fill='#130000', outline='#711400')
      canvas.create_text(app.width/2, app.height/3, text=fancyLetters("Computer's Thinking"), 
                  fill='white', font=('Gothic', '60', 'bold'))

def drawPassPlayer(app, canvas):
      #Two player version. Temporary screen which indicates that user should pass computer to next player 
      if app.player == True: player = 1
      elif app.player == False: player = 2
      canvas.create_rectangle(0, 0, app.width, app.height, fill='#711400')
      canvas.create_rectangle(63, 0, app.width-63, app.height, 
            fill='#510101', outline='#510101')
      canvas.create_rectangle(126, 0, app.width-126, app.height, 
            fill='#130000', outline='#711400')
      canvas.create_text(app.width/2, app.height/3, text=fancyLetters(f"{app.playerNames[player]}'s Turn"), 
                  fill='white', font=('Gothic', '60', 'bold'))

def drawGinOrKnock(app, canvas):
      #Function draws buttons giving player option to knock or call gin if eligible 
      if app.player == True: player = 1
      else: player = 2
      if app.playerStatus[player][0]:
            #If this player has gin draw gin button 
            canvas.create_rectangle(app.width/2 - 100, 700, app.width/2 + 100, 770, fill='#cc3f00')
            canvas.create_rectangle(app.width/2 - 90, 710, app.width/2 + 90, 760, fill='#130000')
            canvas.create_text(app.width/2, 735, text=fancyLetters('Call Gin'), fill='white', font=('Gothic', f'{app.hoverButton}', 'bold')) 
      elif app.playerStatus[player][1]:
            #If this player can knock draw knock button 
            canvas.create_rectangle(app.width/2 - 100, 700, app.width/2 + 100, 770, fill='#a92500')
            canvas.create_rectangle(app.width/2 - 90, 710, app.width/2 + 90, 760, fill='#130000')
            canvas.create_text(app.width/2, 735, text=fancyLetters('Knock'), fill='white', font=('Gothic', f'{app.hoverButton}', 'bold'))

def drawGuide(app, canvas):
      #Draws an operation guide for user
      canvas.create_rectangle(300, 200, app.width - 300, app.height - 200, fill='#130000')
      canvas.create_rectangle(310, 210, app.width-310, app.height - 210, 
            fill='#510101', outline='#510101')
      canvas.create_rectangle(320, 220, app.width-320, app.height - 220, 
            fill='#711400', outline='#711400')
      canvas.create_image(330, 225, 
                  image=ImageTk.PhotoImage(app.imgBackArrow)) 
      canvas.create_image(510, 415, image=ImageTk.PhotoImage(app.guideImage))

def drawTable(app, canvas):
      #Function draws the different elements on the table 
      if app.player == True: 
            player = 1
      elif app.player == False:
            player = 2
      canvas.create_rectangle(-1, -1, app.width+1, app.height+1, fill='#130000')

      #Display the player scores/round number: 
      canvas.create_text(10, 30, text=fancyLetters(f"{app.playerNames[1]}'s Score: ") + f'{app.playerScores[1]}', fill='white', font=('Gothic', 20, 'bold'), anchor='sw')
      canvas.create_text(app.width - 10, 30, text=fancyLetters(f"{app.playerNames[2]}'s Score: ") + f'{app.playerScores[2]}', fill='white', font=('Gothic', 20, 'bold'), anchor='se')
      canvas.create_text(10, app.height - 40, text=fancyLetters(f'Round {app.roundNumber}'), fill='white', font=('Gothic', 30, 'bold'), anchor='sw')
      canvas.create_text(10, app.height - 20, text=fancyLetters(f"{app.playerNames[player]}'s Turn"), fill='white', font=('Gothic', 20, 'bold'), anchor='sw')
     
      #Help button 
      canvas.create_oval(app.width-80, app.height-80, app.width-20, app.height-20, fill='#711400', outline='#a92500')
      canvas.create_text(app.width-50, app.height-50, text='?', fill='white', font=('Gothic', 30, 'bold'), anchor='c')
      if app.player == True or (app.player == False and app.aiModeOn == False):
            if app.passPlayer == True or app.firstPassPlayer == True: drawPassPlayer(app, canvas)
            else:
                  drawHand(app, canvas)
                  drawDeck(app, canvas)
                  drawGinOrKnock(app, canvas)
      if app.player == False and app.aiModeOn == True and app.newRound == False:
            drawAITurn(app, canvas)
      if app.helpScreen == True: 
            drawGuide(app, canvas)

def drawNewRound(app, canvas):
      #Draws a screen indicating that the round ended 
      canvas.create_rectangle(0, 0, app.width, app.height, fill='#711400')
      canvas.create_rectangle(63, 0, app.width-63, app.height, 
                  fill='#510101', outline='#510101')
      canvas.create_rectangle(126, 0, app.width-126, app.height, 
                  fill='#130000', outline='#711400')
      canvas.create_text(app.width/2, app.height/3, text=fancyLetters(f'Round goes to {app.playerNames[app.roundWinner]}'), 
                  fill='white', font=('Gothic', '60', 'bold'), anchor='c')
      canvas.create_text(app.width/2, app.height/3 + 150, text=fancyLetters("Press c to continue"), 
                  fill='white', font=('Gothic', '20', 'bold')) 
      canvas.create_text(app.width/2, app.height/3 + 250, text=fancyLetters(f"{app.playerNames[1]}'s Score: {app.playerScores[1]}"), 
                  fill='white', font=('Gothic', '30', 'bold')) 
      canvas.create_text(app.width/2, app.height/3 + 350, text=fancyLetters(f"{app.playerNames[2]}'s Score: {app.playerScores[2]}"), 
                  fill='white', font=('Gothic', '30', 'bold')) 

def drawGameOver(app, canvas):
      #View drawn when game is over indicating winner and scores. Asks user to play again 
      canvas.create_rectangle(0, 0, app.width, app.height, fill='#711400')
      canvas.create_rectangle(63, 0, app.width-63, app.height, 
                  fill='#510101', outline='#510101')
      canvas.create_rectangle(126, 0, app.width-126, app.height, 
                  fill='#130000', outline='#711400')
      canvas.create_text(app.width/2, app.height/3, text=fancyLetters(f"{app.playerNames[app.winner]} Wins!"), 
                  fill='white', font=('Gothic', '60', 'bold'))
      #Resart Button 
      canvas.create_rectangle(app.width/2 - 100, app.height/3 + 150 - 25, 
                  app.width/2 + 100, app.height/3 + 150 + 25, fill='white', 
                  width=5, outline='#711400')
      canvas.create_text(app.width/2, app.height/3 + 150, text=fancyLetters('Play Again'), 
                  fill='#a92500', font=('Gothic', '30', 
                  'bold'))

      canvas.create_text(app.width/2, app.height/3 + 250, text=fancyLetters(f"{app.playerNames[1]}'s Score: {app.playerScores[1]}"), 
                  fill='white', font=('Gothic', '40', 'bold')) 
      canvas.create_text(app.width/2, app.height/3 + 400, text=fancyLetters(f"{app.playerNames[2]}'s Score: {app.playerScores[2]}"), 
                  fill='white', font=('Gothic', '40', 'bold')) 
            
def redrawAll(app, canvas):
      if app.homeScreen == True:
            drawHome(app, canvas)
      if app.gameScreen == True: 
            if app.newRound: 
                  drawNewRound(app, canvas)
            if not app.newRound: 
                  drawTable(app, canvas)
      if app.gameOver == True: 
            drawGameOver(app, canvas)
   
def rummy500():
      runApp(width=1000, height=800)

rummy500()