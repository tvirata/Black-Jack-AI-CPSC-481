import pygame
import numpy as np
from collections import defaultdict
import pygame.freetype
from BlackJack import card
   


'''
========================================================================================
                        Hit method
Hit method, will create new card for either the dealer or player
Will create a new card next to any existing cards 
also create a new card next to any existing cards
========================================================================================
'''
def hit(cardCount, isPlayer): 
    if isPlayer:   
        #this part Will create a new card next to any existing cards 
        return card(1050 - 130 * cardCount - 5 * cardCount, 578, True)
    else: #This part Will create a new card next to any existing cards
        return card(20 + 130*cardCount + 5*cardCount, 20, False) 
     

'''
=============================================================================
check for ace function will determine if the ace
can be counted as 1 or 11. 
This Will determine if the ace can be counted as 11, 
without it exceeding the 21st limit
=============================================================================
'''       
def check_for_Ace(playersCard, hidden=False):
    isAce=False
    sumOfList = 0
    
    for i in playersCard:
        sumOfList += i.number
        if i.number == 1:
            isAce = True
    
    if isAce and sumOfList-1+11 <= 21:
        return True
    
    return False


''''
===================================================================================
this Will return the player or dealer's hand sum. 
This will return the highest sum possible, in the case of aces.
=================================================================================
'''
def check_for_Sum(cards, hidden=False):
    cardSum = 0
    for i in cards:
       if not hidden:   
          cardSum += i.number
       else:
           if i.show == True:
               cardSum += i.number
           
    if check_for_Ace(cards, hidden):
        cardSum = cardSum - 1 + 11
    
    return cardSum



'''
===================================================================================
This method Will determine who win loss and if the game is a draw
if  player > 21  player and dealer both lost and height score wins.
if player == dealer  its a draw
if player < dealer  player lose. 
====================================================================================
'''
def Check_for_Wining(dealer,playersCard, dealersCards):
    playersSum = check_for_Sum(playersCard)
    dealersSum = check_for_Sum(dealersCards)
    if playersSum > 21:
        return True, False 
    if playersSum == 21:
        return True, True
    if dealersSum == 21:
        return True, False
    if not dealer:
        return False, False
    if dealer and playersSum <= 21 and dealersSum>21:
        return True, True 
    if dealer and playersSum > dealersSum:
        return True, True
    if dealer and dealersSum > playersSum:
        return True, False
    if dealer and dealersSum == playersSum:
        return True, None
    else:
        return False, False


'''
=========================================================================================
Given an action (0 or 1), will execute the action 
this is where Ai will automatically play infinite loop 
of game with out stop the game.  until user stop the game 
===========================================================================================
'''     
def Step_for_ai(action, playersCard, dealersCards):
    if action == 1: #Hit
        playersCard.append(hit(len(playersCard), True))
    else:
        dealersCards[-1].reveal_card()
        while check_for_Sum(dealersCards) <= 18:
            dealersCards.append(hit(len(dealersCards), False))
    return playersCard, dealersCards


'''
=============================================================================
this Will follow an epsilon greedy policy, given Q to determine the next action 
and its Meaning it will determine the best action to take in the current moment
for the AI tanning 
=================================================================================
'''
def generate_Action(state, e, Q):
    probHit = Q[state][1]
    probStick = Q[state][0]
    
    if probHit > probStick:
        probs = [e, 1-e]
    elif probStick>probHit:
        probs = [1-e, e]
    else:
        probs = [0.5, 0.5]
        
    action = np.random.choice(np.arange(2), p = probs)   
    return action
  
 
 
'''
===================================================================================    
this Will create the current state value. 
The state value is a tuple containing the player's 
this current sum, dealer's current sum, and if the ace can be counted as 11
====================================================================================
'''
def create_State_of_Values(playersCard, dealersCards):
    return check_for_Sum(playersCard), check_for_Sum(dealersCards, True), check_for_Ace(playersCard)



'''
=================================================================================
This setQ method Will change Q after each completed game/episode
and This is where the "learning" is taking place fo the AI 
Player 
=================================================================================
'''
def setQ(Q, currentEpisode, gamma, alpha):
    for t in range(len(currentEpisode)):
        
        #in here the episode[t+1:,2] gives all the rewards in the episode from t+1 onwards
        rewards = currentEpisode[t:,2]
        
        #we Created a list with the gamma rate increasing
        discountRate = [gamma**i for i in range(1,len(rewards)+1)]
        
        #we are Discounting the rewards from t+1 onwards with value 
        updatedReward = rewards * discountRate
        
        #now we are Summing up the discounted rewards to equal the return at time step t
        Gt = np.sum(updatedReward)
        
        #we are calculating  the actual Q table value of the state, actinon pair in the next line of code 
        Q[currentEpisode[t][0]][currentEpisode[t][1]] += alpha *(Gt - Q[currentEpisode[t][0]][currentEpisode[t][1]])
    return Q



