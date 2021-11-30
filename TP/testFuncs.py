'''
    testFuncs.py 
        This file harbors most of the more complex helper functions for the conditions checks, 
        score calculations, and establishment of a new round. It also harbors helper functions which call 
        AI functions stored in the AI.py file. 
'''
import copy, random, AI
from AI import *

def aiMoveHelper(app):
    #Calls the AI, function tells AI to make a move 
    aiMove(app)

def checkAIGinOrKnock(app):
    #Calls the AI, function which checks if AI can call gin or knock 
    return (aiGin(app), aiKnock(app))

def unableToUse(cards): 
    #Makes sure that cards aren't out of bounds 
    for card in cards: 
        if card // 10 > 13: 
            return True
    return False 

def aiSetup(app): 
    #This function called the AI file and the respective AI function. It is located in testFuncs.py
    #in order to avoid circulation errors in file importing 
    #Function establishes what the AI needs and what AI will discard as name values 
    hand = convertToNames(app.playerHands[2])
    semiMelds = definePlan(hand, [])
    needs, discards = defineNeeds(semiMelds, app)
    if unableToUse(needs) or unableToUse(discards):
        reset(app)
    app.aiPlan = semiMelds
    for meld in semiMelds:
        if meld in discards:
            app.aiPlan -= meld
    needs, discards = decodeHand(needs), decodeHand(discards)
    #Converting back into card objects 
    objectDiscards = []
    objectNeeds = []
    for card in app.playerHands[2]:
        if card.name in discards: 
            objectDiscards.append(card)
    for card in app.deck: 
        if card.name in needs: 
            objectNeeds.append(card)
    for card in app.pile: 
        if card.name in needs: 
            objectNeeds.append(card)
    for card in app.playerHands[1]: 
        if card.name in needs: 
            objectNeeds.append(card)
    return objectNeeds, objectDiscards

def convertToNames(cards):
    #Converts a set of card objects to their name values 
    nameHand = []
    for card in cards: 
        nameHand.append(card.name)
    nameHand = encodeHand(nameHand)
    return nameHand

def checkGin(hand):
    #This function checks the players hand and returns True if the player has gin 
    nameHand = convertToNames(hand)
    unmatched, melds = checkUnmatchedAndMelds(nameHand, [[]])
    if len(hand) == 11 and (len(unmatched) == 1 or len(unmatched) == 0): return True 
    elif len(hand) == 10 and len(unmatched) == 0: return True 
    return False

def checkKnock(hand):
    #This function checks the players hand and returns True if the player can knock 
    nameHand = convertToNames(hand)
    if checkGin(hand) == False:
        unmatched, melds = checkUnmatchedAndMelds(nameHand, [[]])
        score = unmatchedScore(unmatched)
        if score <= 10: return True
    return False

def unmatchedScore(cards):
    #Calculates the point values of a set of unmatched cards 
    score = 0
    for card in cards:
        val = card//10
        if val >= 10 or val == 1: 
            score += 10
        else: 
            score += val
    return score

def encodeHand(hand):
    #This funciton turns a hand into a list of integers rather than strings which is an 
    # encoded version of the cards names
    vals = {'K':130, 'Q':120, 'J':110, '10':100, 
            '9':90, '8':80, '7':70, '6':60, '5':50, '4':40, '3':30, '2':20, 'A':10}
    suits = {'S':1, 'H':2, 'D':3, 'C':4}
    intHand = []
    for name in hand:
        suit = name[-1]
        value = name[:-1]
        cardVal = vals[value] + suits[suit]
        intHand.append(cardVal)
    return intHand

def decodeHand(hand):
    #This function takes a hand of encoded integers and returns the cards as their string values
    newHand = []
    vals = {130:'K', 120:'Q', 110:'J', 100:'10', 
            90:'9', 80:'8', 70:'7', 60:'6', 50:'5', 40:'4', 30:'3', 20:'2', 10:'A'}
    suits = {1:'S', 2:'H', 3:'D', 4:'C'}
    for card in hand:
        suit = card%10
        val = card - suit
        newHand.append((vals[val] + suits[suit]))
    return newHand
    

#NOTE: MUST GIVE MELDS AN INITIAL CARD list i.e. call checkUnmatchedAndMelds(hand, [])
def checkUnmatchedAndMelds(hand, melds):
    #Base case 
    if hand == []: 
        #Get all melds smaller than three as these are unmatched cards
        unmatched, melds = getUnmatched(melds)
        #Checks one last time if any of the unmatched fit into melds 
        #RETURNS THE UNMATCHED CARDS AND THE MELDS 
            #unmatched, melds (Note: encoded)
        return (matchUnmatched(unmatched, melds, 0))
    #Recursive case 
    else: 
        #Take a card 
        currCard = hand[0]
        restHand = hand[1:]
        
        #Check if fits in the prev meld 
        for i in range(len(melds)):
            fits, dir = fitsInMeld(currCard, melds[i])
            if fits and len(melds[i]) < 3:
                #Add card to meld 
                if dir == False:
                    melds[i].append(currCard)
                if dir == True: 
                    melds[i].insert(0, currCard)
                return checkUnmatchedAndMelds(restHand, melds)
        melds.append([currCard])
        return checkUnmatchedAndMelds(restHand, melds)
  
    
def worksWith(card1, card2):
    #Checks that two cards "work" with each other 
    if card1 % 10 == card2 % 10: 
        if abs(card1//10 - card2//10) == 1:
            return True
    if card1//10 == card2//10:
        return True 
    return False

def samePattern(card1, card2, card3):
    #Checks that the parameters for card fitting in meld extend to melds of lengths longer than one 
    #Checks the same suit condition 
    if card3 % 10 == card2 % 10: 
        if card1 % 10 == card2 % 10 and abs(card1//10 - card2//10) == 1:
            return True
    #Checks the same number condition
    if card3//10 == card2//10:
        if card1//10 == card2//10:
            return True 
    return False 

def fitsInMeld(card, meld):
    #Takes a card and a meld and returns whether or not that card can fit into the meld 
    if meld == [] or (len(meld) == 1 and worksWith(card, meld[0])): return True, False 
    if len(meld) > 1:
        if samePattern(card, meld[-1], meld[-2]):
            return True, False
        elif samePattern(card, meld[0], meld[1]):
            return True, True 
    return False, None 

def matchUnmatched(unmatched, melds, index):
    #Function tries to fit all unmatched cards into the given melds
    newUnmatched = []
    while index != len(unmatched):
        currCard = unmatched[index]
        placedCard = False
        for i in range(len(melds)):
            fits, dir = fitsInMeld(currCard, melds[i])
            if fits and placedCard == False:
                placedCard = True
                if dir == False: 
                    melds[i].append(currCard)
                elif dir == True: 
                    melds[i].insert(0, currCard)
        if not placedCard: 
            newUnmatched.append(currCard)
        index += 1
    return newUnmatched, melds
    

def getUnmatched(melds):
    #Function takes all derrived melds 
    #Takes a list of melds and puts all melds < 3 cards into unmatched list
    #returns the unmatched cards and the official melds 
    unmatched = []
    officialMelds = []
    for i in range(len(melds)): 
        if len(melds[i]) < 3: 
            unmatched += melds[i]
        else: 
            officialMelds.append(melds[i])
    return unmatched, officialMelds


################################ ROUND ENDED ###################################
'''
    This section of the testFuncs file is responsible for all of the necessary actions to be carried 
    out when a round ends. NOTE: Called in both two player and AI mode. 
'''
def getInitHand(app):
      #When the game is started, deals a list of 10 cards from deck to each player  
      hand = []
      for i in range(10):
            hand.append(app.deck[0])
            app.deck = app.deck[1:]
      return hand

def shuffle(deck):
      #This function will shuffle a given deck of cards 
      random.shuffle(deck)
      return deck 

'''
    roundEndedActions:  
    - Calculate score based on state of players' hands 
    - Reset the deck/pile  
    - Reset the player hands 
    - Reset the player status 
    - Start a new round 
'''
def roundEndedActions(app):
    #Function carries out all necessary actions when a player ends a round whether 
    # by knocking or calling gin (Full explanation above)
    if app.player == True: 
        player = 1
        other = 2
    else: 
        player = 2
        other = 1
    
    if app.aiModeOn == False:
        opponentsHand = convertToNames(app.playerHands[other])
        playersHand = convertToNames(app.playerHands[player])
        opponentsUnmatched, opponentsMelds = checkUnmatchedAndMelds(opponentsHand, [[]])
        playersUnmatched, playersMelds = checkUnmatchedAndMelds(playersHand, [[]])
    elif app.aiModeOn == True and player == 2:
        opponentsHand = convertToNames(app.playerHands[other])
        opponentsUnmatched, opponentsMelds = checkUnmatchedAndMelds(opponentsHand, [[]])
        playersHand = convertToNames(app.playerHands[player])
        playersUnmatched, playersMelds = checkUnmatchedAndMeldsAI(app.aiPlan, app, encodeAINeedsHand(app.aiNeeds))
    elif app.aiModeOn == True and other == 2: 
        opponentsHand = convertToNames(app.playerHands[other])
        playersHand = convertToNames(app.playerHands[player])
        opponentsUnmatched, opponentsMelds = checkUnmatchedAndMeldsAI(app.aiPlan, app, encodeAINeedsHand(app.aiNeeds))
        playersUnmatched, playersMelds = checkUnmatchedAndMelds(playersHand, [[]])

    #Opponent gets opportunity to discard any unmatched cards 
    opponentsNewUnmatched, sharedMelds = checkUnmatchedAndMelds(opponentsUnmatched, playersMelds)

    #If the player called Gin: 
    if app.playerStatus[player][0] == True: 
        #Retrieve the melds of the player who called gin, retrieve the unmatched cards of opponent
        #check if any of the opponents unmatched cards fit in the melds of the player 
        app.playerScores[player] += (20 + unmatchedScore(opponentsNewUnmatched))   
        app.roundWinner = player

    #If the player knocked: 
    elif app.playerStatus[player][1] == True: 
        # Try to fit Non-knocking players unmatched cards into knocking players melds 
        opponentUnmatchedScore = unmatchedScore(opponentsNewUnmatched)
        playersUnmatchedScore = unmatchedScore(playersUnmatched)
        unmatchedDifference = abs(opponentUnmatchedScore - playersUnmatchedScore)
        #If the opponent won the knock 
        if opponentUnmatchedScore <= playersUnmatchedScore: 
            #Other player gets difference of unmatched scores plus an additional 10 points 
            app.playerScores[other] += (10 + unmatchedDifference)
            app.roundWinner = other
        #If the player won the knock 
        elif playersUnmatchedScore < opponentUnmatchedScore: 
            app.playerScores[player] += unmatchedDifference
            app.roundWinner = player


    #Check if the game is over or if it is just a new round 
    app.newRound = True
    if app.playerScores[1] >= 100 or app.playerScores[2] >= 100: 
        app.newRound = False
        app.gameScreen = False 
        app.gameOver = True
        app.winner = app.roundWinner 
    
    #If it still is a new round, then reset the conditions of the model 
    #Add player's cards back to the deck 
    else: 
        for player in app.playerHands:
            app.deck += app.playerHands[player]
        #Add the pile cards back to the deck
        for i in range(len(app.pile) - 1): 
            app.deck.append(app.pile[i])
        app.pile = [app.pile[-1]]
        app.pile[0].selected, app.pile[0].hovered = False, False
        # Reshuffle and deal 
        app.deck = shuffle(app.deck)
        for i in range(len(app.deck)):
            app.deck[i].selected, app.deck[i].hovered = False, False
        app.playerHands = {}
        app.playerHands = {
                        1:getInitHand(app), 
                        2:getInitHand(app)
                        }
        app.playerStatus = {
                            1:(False, False),
                            2:(False, False)
                            }
        app.roundNumber += 1
        if app.aiModeOn == True: 
            app.aiNeeds, app.aiDiscards = aiSetup(app)

def reset(app):
    #Carries out aspects of roundEndedActions() without calling all of the actions 
    #in that function 
    for player in app.playerHands:
            app.deck += app.playerHands[player]
    for i in range(len(app.pile) - 1): 
        app.deck.append(app.pile[i])
    app.pile = [app.pile[-1]]
    app.pile[0].selected, app.pile[0].hovered = False, False
    app.deck = shuffle(app.deck)
    for i in range(len(app.deck)):
        app.deck[i].selected, app.deck[i].hovered = False, False
    app.playerHands = {}
    app.playerHands = {
                    1:getInitHand(app), 
                    2:getInitHand(app)
                    }
    app.playerStatus = {
                        1:(False, False),
                        2:(False, False)
                        }
    app.roundNumber += 1
    if app.aiModeOn == True: 
        app.aiNeeds, app.aiDiscards = aiSetup(app)