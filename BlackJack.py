'''
=============================================================================
                          Black Jack 
 Black jack game is written by Mohammed Ali and Tonirose Varata
 This is the Final Project for CPSC481 AI 
 California state university of fullerton 
 Date Written: 05/01/2024  
============================================================================
'''


import pygame
import numpy as np
from collections import defaultdict
import pygame.freetype
from plot_utils import plot_blackjack_values
from cardClass import *



'''
===================================================================
The is the main The game starts here calling 
We hand to install pygame to use graphical use interface 
install matplotlib to use the graphs 
installed NumPy for mathematical operations on arrays. 
It adds powerful data structures to Python that guarantee 
efficient calculations with arrays and we used to generate 
number for graphs. 
#If the player won
======================================================================
'''



'''
===================================================================
This variable can be changed for programmer testing purpose 
dealer_deal_limit -  needed for dealer to stop hitting.
time_Delay_Between_Game - Delay (in seconds) between games
Frame_Per_Second - How many frames will be drawn every second.
volume button bale to turn of the card sound when AI is playing
AI - If False, you can play against the dealer without the AI

The tree value is for monte carlo Algorithm testing for the AI player

e - Epsilon Value for Monte Carlo Algorithm
gamma - Gamma Value for Monte Carlo Algorithm
alpha - Alpha Value for Monte Carlo Algorithm
===================================================================
'''

AI = False
time_Delay_Between_Game = 5 
Frame_Per_Second = 30 
#Ctrl + K + C : Comment out the selected code. Ctrl + K + U : Uncomment the selected 
End_of_loop = True

while End_of_loop:
    AI_OR_Name = input("To Play regular game type 'Game' watch AI play type 'AI' : ")
    if AI_OR_Name.lower() == 'ai':
        AI = True
        time_Delay_Between_Game = .0001
        Frame_Per_Second = 120
        End_of_loop = False
    elif AI_OR_Name.lower() == 'game':
        name1 = input("Enter you name: ")
        End_of_loop = False
    else:
        print("wrong Entry")
        
        
dealer_deal_limit = 18 
volume = True
e = 0.1 
gamma = 1 
alpha=0.02




def main():
        
    ''' 
    running is to keep the game table alive
    inside the while loop 
    '''
    pygame.display.set_caption("BlackJack AI Machine Learning")
    running = True
    clock = pygame.time.Clock()
    
    '''
    dealers_Card and players_or_AI_cards Will create two random cards for player and dealer. 
    One of the The dealer's second card is going to be hidden.
    Each of the card is almost  5 to  pixels away from each other.
    game_over_man variable is going to ge False at first. after playing each hand it will going to 
    get change by the function check_for_Winning, if the game is over or not?
    Is it the dealer's turn or not?
    dealer variable will decide if if dealer, player aor AI's  turn
    winner variable will check for the if the player is a winner or not. 
    delay_between_the_game will keep on track the delay of the game time between of the games
    '''
    
    dealers_cards = [card(20,20, False), card(155,20, False, False)]
    players_or_AI_cards = [card(1050, 578, True)]
    players_or_AI_cards.append(hit(len(players_or_AI_cards), True))
    game_over_man = False 
    dealer = False 
    winner = False
    delay_between_the_game = 0 

    '''
    currentEpisode variable is a list containing the moves of the game
    we are Initialling an empty dictionary for Q
    gamesWon, gamesLost, gamesPlayed variable are Initially the games won and lost are 0
    GAME_FONT variable loads a default fonts for the game. you can change 
        the other fonts we have uploaded over 20 plus font in the font folder. 
        just change the name of the .ttf file. 
    '''
    currentEpisode = [] 
    Q = defaultdict(lambda: np.zeros(2))
    gamesWon = gamesLost = gamesPlayed = 0 
    GAME_FONT = pygame.freetype.Font("Fonts/BebasNeue-Regular.ttf", 24)
    
    
    
    ''' This is where game stats playing until running == false'''
    while running:
        clock.tick(Frame_Per_Second)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        #screen.fill(pygame.Color(17, 115, 79))
        #screen.blit(backgroundImage, (0, 0))
        
       
        ''' this will draw a card for dealer '''
        for i in dealers_cards:
            i.draw_card() 

        for i in players_or_AI_cards:
            i.draw_card()
        
        ''' 
        This where Will total card sum test at (23, 230)
        will display total dealer card sum at (23, 230)
        will display player card sum at (912, 539)
        will display AI player card sum at (23, 230)
        will display  game won by AI at (912, 539)
        will display game won by player at (23, 230)
        will display number of round played at (232, 75, 61)
        '''
        if AI:
            name = "AI"
        else:
            name = name1
        text_surface, rect = GAME_FONT.render((name + "'s Total card Sum: " + str(check_for_Sum(players_or_AI_cards))), pygame.Color('white'))
        
        if not AI:
            screen.blit(text_surface, (912, 539))
        else:
            screen.blit(text_surface, (912, 539))
        text_surface, rect = GAME_FONT.render(("Dealer's Total card Sum: " + str(check_for_Sum(dealers_cards, True))), pygame.Color('white'))
        screen.blit(text_surface, (23, 230))
        
        text_surface, rect = GAME_FONT.render(("Games Won by "  + name + ": " + str(gamesWon)), pygame.Color('blue'))
        screen.blit(text_surface, (23, 665))#470
        
        text_surface, rect = GAME_FONT.render(("Games Lost: " + str(gamesLost)), (242, 235, 24), bgcolor = 'black')# this is rgb color 
        screen.blit(text_surface, (23, 705))#510
        
        text_surface, rect = GAME_FONT.render(("Number of Rounds: " + str(gamesPlayed)), (232, 75, 61))
        screen.blit(text_surface, (23, 745))#550
        
        
            


            
        '''
        this is going to Draws the Hit and st button  buttons,
        when the  AI mode is off 
        '''
        if not AI:
            screen.blit(pygame.image.load('Cards/HIT.png'), (width-200,20))
            screen.blit(pygame.image.load('Cards/STICK.png'), (width-200,110))

        game_over_man, winner = Check_for_Wining(dealer, players_or_AI_cards, dealers_cards)
        
        
        '''
        this the game design and game mechanics  ends here 
        this where game start to count how many game have been play 
        until the user stop the game.  
        '''           
        if game_over_man and delay_between_the_game <= time_Delay_Between_Game * Frame_Per_Second:
            if delay_between_the_game == 0:
                gamesPlayed += 1
                if None:
                    gamesWon = gamesWon
                elif winner:
                    # Testing print("You Won")
                    gamesWon += 1
                    #Testing print(gamesWon, gamesLost)
                else:
                    gamesLost+=1
                    #Testing print(gamesWon, gamesLost)
                
                '''
                every number in the list the game will stop 
                then game will display the 3D graphing status
                showing how is IA doing in learning the status
                in Monte Carlo Method of reinforcement learning 
                '''
                if gamesPlayed in [50000, 500000, 10000000, 5000000, 10000000, 5000000, 100000, 150000, 200000, 250000, 500000, 1000000] :
                    plot_blackjack_values(dict((k,np.max(v)) for k, v in Q.items()), gamesPlayed, gamesWon, gamesLost )
                   
            delay_between_the_game += 1
         
        '''
        this is the section decides who wins the game 
        dealer or the player  
        '''       
        if game_over_man and delay_between_the_game >= time_Delay_Between_Game * Frame_Per_Second:
            dealers_cards = [card(20,20, False), card(155,20, False, False)] #5 space
            players_or_AI_cards = [card(1050, 578, True)]
            players_or_AI_cards.append(hit(len(players_or_AI_cards), True))
            game_over_man = dealer = winner = False
            delay_between_the_game = 0

        
        
        '''
        AI aspect, stores each state/reward of an episode. After an episode it updates the Q values
        and adds the number 1 or -1 to the winner or loser
        this part also taker care of the AI current state value 
        this is where Monte Carlo Method of reinforcement learning 
        happens. 
        '''
        if AI and not game_over_man and not dealer:
            # test print("AI MODE")
            currentState = create_State_of_Values(players_or_AI_cards, dealers_cards)
            action = generate_Action(currentState, e, Q)
            if action == 0:
                dealer = True
            players_or_AI_cards, dealers_cards = Step_for_ai(action, players_or_AI_cards, dealers_cards)
            game_over_man, winner = Check_for_Wining(dealer, players_or_AI_cards, dealers_cards)
            if game_over_man and winner:
                reward = 1
            elif game_over_man and not winner:
                reward = -1            
            else:
                reward = 0

            currentEpisode.append((currentState, action, reward))
            
            if game_over_man:
                currentEpisode = np.array(currentEpisode, dtype="object" ) #must use 'dtype="object"' so the game will not crash for older version of numpy game
                Q = setQ(Q, currentEpisode, gamma, alpha)
                currentEpisode= []
        

        '''
        this is the button user interface 
        this is also takes of mouse click interface
            Key Presses
            when user Press r will reset the current game
            when user Press p will plot the current plot
            when user Press w will print games won/lost
            when user Press t will reset the win/lose numbers
            when user Press h will do a hit (when not in AI mode)
            when user Press s will do a stick (when not in AI mode)
        '''
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    dealers_cards = [card(20,20, False), card(155,20, False, False)] #5 space
                    players_or_AI_cards = [card(1050, 578, True)]
                    game_over_man = dealer = winner = False
                    delay_between_the_game = 0
                    currentEpisode = 0
                if event.key == pygame.K_p:
                    
                    plot_blackjack_values(dict((k,np.max(v)) for k, v in Q.items()), gamesPlayed, gamesWon, gamesLost )
                    
                if event.key==pygame.K_w:
                    print("Wins:", gamesWon, "Losses:", gamesLost,  "Games Played:", gamesPlayed)
                if event.key==pygame.K_t:
                    gamesWon=gamesLost=0
                if event.key == pygame.K_h and not game_over_man and not AI:
                    players_or_AI_cards.append(hit(len(players_or_AI_cards), True))
                if event.key == pygame.K_s and not game_over_man and not AI:
                    dealer=True
                    
                    for i in dealers_cards:
                        i.draw_card() 
                        i.reveal_card()
                    while check_for_Sum(dealers_cards) <= dealer_deal_limit:
                        dealers_cards.append(hit(len(dealers_cards), False))
                   
            
            
            '''  
            this where Mouse Clicks event gets implemented 
            user can Click on Hit button to Hit
            user can Click on Stick button to Stick
            user can Click on Volume button to mute/unmet
            '''
            if  event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                print(mouseX, mouseY)
                if mouseX >= 940 and mouseX <= 990 and mouseY >= 210 and mouseY <= 260:
                    volume =  not volume
                if mouseX >= 1000 and mouseX <= 1190 and mouseY >= 20 and mouseY <= 108 and not AI:
                    players_or_AI_cards.append(hit(len(players_or_AI_cards), True))
                if mouseX >= 1000 and mouseX <= 1190 and mouseY >= 120 and mouseY <= 210 and not AI: 
                    dealer = True
                    
                    for i in dealers_cards:
                        i.draw_card() 
                        i.reveal_card()
                    while check_for_Sum(dealers_cards) <= dealer_deal_limit:
                        dealers_cards.append(hit(len(dealers_cards), False))
        
                      
        pygame.display.update()
        
    pygame.display.quit()


 
#this will call the main method
if __name__ == "__main__":
    main()