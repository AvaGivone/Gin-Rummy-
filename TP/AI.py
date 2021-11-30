#AI Functions 
'''
    This AI was built entirely from scatch. My verison of the Gin Rummy AI was derived after research showing 
    how many different routes this game AI can take. The following sources were essential for research: 
    
    Works Referenced: 
    https://www.aaai.org/AAAI21Papers/EAAI-66.EicholtzM.pdf
    https://towardsdatascience.com/learning-gin-rummy-part-i-75aef02c94ba
    https://digitallibrary.oswego.edu/content/AA/00/00/02/79/00001/Rummy%20500%20With%20Symbolic%20AI%20Opponent%20-%20Matthew%20Grzenda.pdf

    My rendition of the Gin Rummy AI, takes inspiration from the Hand Built strategy. The AI gets dealt a 
    hand of cards and determines what it needs to have a hand of 10 cards which qualify for knocking or gin. 
    For the sake of clarity, efficiency, and probability, the AI does not strive to achieve a meld which consists 
    of a set of same numbers, rather it only strives to achieve melds which are sequences of numbers of the same 
    suit. 
'''

def aiGin(app):
    #Returns a boolean saying if current AI state is gin 
    if app.aiNeeds == []:
        return True
    return False

def aiKnock(app):
    #Return a boolean saying if current AI state is knock 
    #An AI hand can only knock if the needed cards are greater than an ace and less than a 3
    #this will make the knocking a random decision and more human 
    possibles = ['2D', '2S', '2C', '2H']
    if not aiGin(app): 
        if len(app.aiNeeds) == 1 and app.aiNeeds[0].name in possibles:
            return True 
    return False

def aiMove(app):
    #This function carries out the AI move depending on the first card in the pile, or the card the AI picks 
    #up from the deck 
    #If the card in the pile is in AI needs, pick it up 
    if app.pile[-1] in app.aiNeeds: 
        app.aiNeeds.remove(app.pile[-1])
        pickedUp = app.pile.pop()
        app.playerHands[2].append(pickedUp)

        discarding = app.aiDiscards.pop()
        app.playerHands[2].remove(discarding)
        app.pile.append(discarding)
    #If did not take from pile, take from deck 
    else: 
        pickedUp = app.deck.pop()
        if pickedUp in app.aiNeeds: 
            app.aiNeeds.remove(pickedUp)
            app.playerHands[2].append(pickedUp)

            discarding = app.aiDiscards.pop()
            app.playerHands[2].remove(discarding)
            app.pile.append(discarding)
        else: 
            app.pile.append(pickedUp)

def tooSpreadOut(meld):
    #Checks if a meld is spread out by too many cards, AKA the meld is 3 cards and more than one pair in the set is two apart 
    if len(meld) < 3: return False
    prevVal = None
    twoAparts = 0
    for val in meld: 
        if prevVal != None:
            if abs((prevVal // 10) - (val // 10)) >= 2: 
                twoAparts += 1
                if twoAparts > 1:
                    return True 
        elif prevVal == None: 
            val = prevVal   
    return False

def needsUsed(meld, used, length):
    #Checks if the meld needs a card that is already being used somewhere else 
    meldNeeds = getNeeded(meld, length)
    for val in meldNeeds: 
        if val in meld: 
            return True
    return False 

def defineNeeds(semiMelds, app):
    #Function returns all of the needed cards for the AI to have gin 
    #Sort the melds by length, becuase once you have reached 10 cards obtained and needed for some melds, 
    # anything left over will be swapped for needed cards
    semiMelds = sorted(semiMelds, key=len)
    semiMelds = semiMelds[::-1]
    needed = []
    discards = []
    lengths = [4, 3, 3]
    lenInd = 0
    used = 0
    meldIndex = 0
    #If you are dealt a sequence larger than 4, then aim to complete the sequence
    #or if the semi meld is 3 cards but all the cards are two apart 
    if len(semiMelds[0]) > 4 or tooSpreadOut(semiMelds[0]):
        needed = getNeeded(semiMelds[0], 10)
        for i in range(1, len(semiMelds)):
            discards += semiMelds[i]
        return needed, discards
    #Otherwise, devise a strategy based on your 3 largest melds
    for meld in semiMelds: 
        #The AI going for a set of the same number overcomplicates the entire algorithm 
        #so this AI only goes for straight runs, which are higher probability of completing anyway 
        if not tooSpreadOut(meld) and notSet(meld) and not needsUsed(meld, needed, 4):
            #Here is where you handle the case that your meld is larger than the desired length, then you
            #would just aim to complete the hand with that meld 
            if lenInd != len(lengths):
                length = lengths[lenInd]
                if len(meld) > length: 
                    length = 10 - used
                    newNeeded = getNeeded(meld, length)
                    needed += newNeeded
                #This is the ordinary case of a normal size starting meld 
                elif len(meld) <= length: 
                    newNeeded = getNeeded(meld, length)
                    needed += newNeeded
                    used += len(newNeeded)
                    lenInd += 1
            else: 
                discards += meld
    return needed, discards

def notSet(meld):
    #Returns a boolean determining if this meld is aiming for a set of the same number
    if len(meld) == 1: return True 
    if meld[0] // 10 == meld[1] // 10: 
        return False 
    return True

def getNeeded(meld, length):
    #Finding the card values you need given a semiMeld of a sequence
    meld.sort()
    needed = [] 
    suit = meld[0] % 10
    notNeededValues = []
    for i in range(len(meld)):
        notNeededValues.append(meld[i] // 10)
    #If the card is higher than or equal to a jack, you will need to calculate needed cards in reverse order 
    #as to not go out of bounds
    if meld[0] // 10 >= 11: 
        meld.reverse()
        for i in range(length):
            card = (meld[0] // 10 - i) * 10 + suit
            if card // 10 not in notNeededValues:
                needed.append(card) 
    else:
        for i in range(length):
            card = (meld[0] // 10 + i) * 10 + meld[0] % 10
            if card // 10 not in notNeededValues:
                needed.append(card)
    return needed
        

def definePlan(hand, semiMelds):
    #Recursively defines the AI's plan for the game. Note: for the sake of clarity, and probability
    #the AI avoids aiming to achieve sets of the same number, and, rather, aims to create sequential melds
    #Base case 
    if hand == []:
        return semiMelds
            
    #Recusive case 
    else:
        card = hand[0]
        cardVal = card // 10
        rest = hand[1:]
        newRest = hand[1:]
        possibleSeq = [card]
        possibleSame = [card]
        #Indicates that AI should avoid attempting a set of K's, Q's, 2's, or A's 
        # CITATION: 
        #The decision of prioritizing strategies is based on statistics derived from: 
        #http://rummytalk.com/the-mathematics-and-odds-of-gin-rummy/ 
        avoidSame = [13, 12, 2, 1]
        for test in rest:
            if isOneOrTwoApart(possibleSeq[0], test) or isOneOrTwoApart(possibleSeq[-1], test):
                possibleSeq.append(test)
        if len(possibleSeq) > 0:
            semiMelds.append(possibleSeq)
            newRest = [i for i in newRest if i not in possibleSeq]
        return definePlan(newRest, semiMelds)

def isSameNum(card1, card2):
    #Returns a boolean whether or not two cards have the same number value 
    if card1 // 10 == card2 // 10: 
        return True 
    return False

def isOneOrTwoApart(card1, card2):
    #Function checks if the cards are one or two places apart 
    if card1 % 10 != card2 % 10:
        return False
    card1Val = card1 // 10
    card2Val = card2 // 10 
    if abs(card1Val - card2Val) <= 2: 
        return True 
    return False

def checkUnmatchedAndMeldsAI(semiMelds, app, needs):
    #This is the AI rendition of checkingUnmatchedAndMelds. This function essentually builds
    # the AI's unmatched cards and melds by replicating the operations the AI took to define it's 
    #plan and needed cards, but checks if those cards are still needed. If they are not, then this would
    #indicate that the AI has that card in it's hand, so the meld would be a completed meld in the AI's hand
    #If the cards are still needed, then the possessed card which require unpossessed needed cards are unmatched. 
    semiMelds = sorted(semiMelds, key=len)
    semiMelds = semiMelds[::-1]
    needed = []
    currAINeeds = needs
    unmatched = []
    melds = []
    lengths = [4, 3, 3]
    lenInd = 0
    incomplete = False
    used = 0
    if len(semiMelds[0]) > 4 or tooSpreadOut(semiMelds[0]):
        needed = getNeeded(semiMelds[0], 10)
        for val in needed: 
            if val in currAINeeds:
                incomplete = True
            else:
                semiMelds[0].append(val)
        if incomplete == True:
            unmatched += semiMelds[0]
        else:
            melds.append(semiMelds[0])
        return unmatched + encodeAINeedsHand(app.aiDiscards), melds
    #Otherwise, devise a strategy based on your 3 largest melds
    for meld in semiMelds: 
        incomplete = False
        if not tooSpreadOut(meld) and notSet(meld) and not needsUsed(meld, needed, 4):
            if lenInd != len(lengths):
                length = lengths[lenInd]
                if len(meld) > length: 
                    length = 10 - used
                    newNeeded = getNeeded(meld, length)
                    for val in newNeeded: 
                        if val in currAINeeds:
                            incomplete = True
                        else:
                            meld.append(val)
                    if incomplete == True:
                        unmatched += meld
                    else:
                        melds.append(meld)
                #This is the ordinary case of a normal size starting meld 
                elif len(meld) <= length: 
                    newNeeded = getNeeded(meld, length)
                    needed += newNeeded
                    for val in newNeeded: 
                        if val in currAINeeds:
                            incomplete = True
                        else:
                            meld.append(val)
                    if incomplete == True:
                        unmatched += meld
                    else:
                        melds.append(meld)
                    lenInd += 1
    return unmatched + encodeAINeedsHand(app.aiDiscards), melds


def encodeAINeedsHand(hand):
    #This funciton turns a hand into a list of integers rather than strings which is an 
    # encoded version of the cards names
    vals = {'K':130, 'Q':120, 'J':110, '10':100, 
            '9':90, '8':80, '7':70, '6':60, '5':50, '4':40, '3':30, '2':20, 'A':10}
    suits = {'S':1, 'H':2, 'D':3, 'C':4}
    intHand = []
    for card in hand:
        name = card.name
        suit = name[-1]
        value = name[:-1]
        cardVal = vals[value] + suits[suit]
        intHand.append(cardVal)
    return intHand