'''
=============================================================================
                          Black Jack 
 Black jack game is written by Mohammed Ali and Tonirose Varata
 This is the Final Project for CPSC481 AI 
 California state university of fullerton 
 Date Written: 05/10/2024  
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

height = 800
width = 1200
screen = pygame.display.set_mode((width, height))

'''
=============================================================================
This Background  class to use a background Image in the GUI . 
'''
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
'''
============================================================================= 
'''




BackGround = Background('Cards/background.jpg', [0,0])
#backgroundImage = pygame.image.load('Cards/background.jpg')
#backgroundImage = pygame.transform.scale(backgroundImage, (height, width)) #scales an image




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

# AI = False
# time_Delay_Between_Game = 5 
# Frame_Per_Second = 30 
#Ctrl + K + C : Comment out the selected code. Ctrl + K + U : Uncomment the selected 

        
  

pygame.init()
# This will make the play the sound of the card when playing the game
effect = pygame.mixer.Sound('Cards/cardSound.wav')
effect2 = pygame.mixer.Sound('Cards/money.wav')

#This will load the card.png file for the GUI mode 
programIcon = pygame.image.load('Cards/playing_cards.png')

#this like will display the little png card picture top lect corner of the display
pygame.display.set_icon(programIcon)



#These are the actions the AI can take, 0 for stand, 1 for hit
actionSpace = [0,1] 



dealer_deal_limit = 18 
volume = False
e = 0.1 
gamma = 1 
alpha=0.02

'''
#=============================================================================
                            Card Class
# 1: Ace, 2-10: Number Card, 11: Jack, 12: Queen, 13: King
# 2 chose form 4 different card type harts club or diamond spade
# X location of the card 
# Y location of the card
# X location of the card
# Y location of the card
# If false, the card will be face down. If true, card will be revealed. 
#Identify if the card is for the player's or dealer's
# =============================================================================
'''
class card():
    def __init__(self, x, y, player, show=True):
        self.number = np.random.choice(range(1, 14)) 
        self.number2 = np.random.choice(range(1,5))
        self.x = x 
        self.y = y 
        self.show = show 
        self.player = player 
        
        #Different card image if player vs dealer
        if self.player: 
            location = 'Cards/Player/card_'
            
        else:
            location = 'Cards/Dealer/card_'
                       
        self.image = pygame.image.load(location + str(self.number) + '_' + str(self.number2) + '.png')
        
        #Width/height of card image
        self.w, self.h = self.image.get_rect().size 
        
        #this will change all the face card value to 10
        if self.number > 10: self.number = 10 
        
        # this will Play sound if and only if audio is turned on
        if volume: 
            effect.play()
            
    
    
    # this method will reveal the dealer card 
    # The dealers second card is initially hidden, 
    # this will reveal that card
    def reveal_card(self): 
        self.show = True 
        
        #this will Play sound only if audio is turned on
        if volume: 
            effect.play()
    
    
    #this will Will draw the card to screen
    def draw_card(self): 
        if self.show:
            screen.blit(self.image, (self.x, self.y))
        else:
            screen.blit(pygame.image.load('Cards/faceDown.png'), (self.x, self.y))
            


def main():
    
    bank = 1000  
    bet = 0 
    
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
            AI = False
            time_Delay_Between_Game = 3
            Frame_Per_Second = 30 
            End_of_loop = False
        else:
            print("wrong Entry")
        
        
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
    
    dealers_cards = [ card(20,20, False), card(155,20, False, False) ]
    players_or_AI_cards = [ card(1050, 578, True) ]
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

        
        global volume
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
        
        
            

        if volume:
            screen.blit(pygame.image.load('Cards/audio.png'), (width-200,210))
        else:
            screen.blit(pygame.image.load('Cards/mute.png'), (width-200,210))
            
        '''
        this is going to Draws the Hit and st button  buttons,
        when the  AI mode is off 
        '''
        if not AI:
            screen.blit(pygame.image.load('Cards/HIT.png'), (width-200,20))
            screen.blit(pygame.image.load('Cards/STICK.png'), (width-200,110))
            
            text_surface, rect = GAME_FONT.render(("Bank $"), pygame.Color('white'))
            screen.blit(text_surface, (915, 490))
            
            text_surface, rect = GAME_FONT.render(("BET Amount $"), pygame.Color('white'))
            screen.blit(text_surface, (325, 503))
           
            text_surface, rect = GAME_FONT.render(str(bank), pygame.Color('blue'))
            screen.blit(text_surface, (980, 490))
            
            text_surface, rect = GAME_FONT.render(str(bet), pygame.Color('blue'))
            screen.blit(text_surface, (448, 503))
            
            
            
            if bank > 0:
                screen.blit(pygame.image.load('Cards/one.png'), (80,260))
            else: 
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (80,260))
            
            if bank >= 10:
                screen.blit(pygame.image.load('Cards/ten.png'), (80,340))
            else:
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (80,340))
                
            if bank >= 50:   
                screen.blit(pygame.image.load('Cards/fifty.png'), (80,420))
            else:
                 screen.blit(pygame.image.load('Cards/buttonpress.png'), (80,420))   
                
            if bank >= 500:       
                screen.blit(pygame.image.load('Cards/5Hundred.png'), (80,500))
            else:
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (80,500))
                
            if bank >= 5:
                screen.blit(pygame.image.load('Cards/five.png'), (165,260))
            else:
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (165,260))
                
            if bank >= 20:    
                screen.blit(pygame.image.load('Cards/twenty.png'), (165,340))
            else:
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (165,340))
                
            if bank >= 100:
                       screen.blit(pygame.image.load('Cards/hundred.png'), (165,420))
            else:
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (165,420))
            
            if bank >= 1000:    
                screen.blit(pygame.image.load('Cards/thousand.png'), (165,500))
            else:
                screen.blit(pygame.image.load('Cards/buttonpress.png'), (165,500))
            
            if bank >= 10000:
                screen.blit(pygame.image.load('Cards/10thousands.png'), (80,580))
                
            if bank >=100000:
                screen.blit(pygame.image.load('Cards/100thousand.png'), (165,580))
                
            if bank >= 1000000 :
                screen.blit(pygame.image.load('Cards/1milions.png'), (1090,220))


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
                    
                    if len(players_or_AI_cards) == 2 and check_for_Sum(players_or_AI_cards) == 21:
                        print("blackjack")
                        bank = bank + bet+bet+bet
                    bank = bank + bet + bet
                    bet = 0
                    gamesWon += 1
                  
                else:
                    if len(dealers_cards) == 2 and check_for_Sum(dealers_cards) == 21:
                        print("dealer have blackjack")
                    
                    if check_for_Sum(dealers_cards) == check_for_Sum(players_or_AI_cards):
                        print (" its a Tie")
                        bank = bank + bet
                        
                    bet = 0
                    gamesLost+=1
       
                
                '''
                every number in the list the game will stop 
                then game will display the 3D graphing status
                showing how is IA doing in learning the status
                in Monte Carlo Method of reinforcement learning 
                '''
                if gamesPlayed in [1000000] :
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
                
                
                
                '''when user press v it will turn off the volume of the game'''
                if event.key == pygame.K_v:
                    volume = not volume
                    
                    
                '''
                When user Click on the 1 dollar chip game will add 1 dollar to the bet 
                amount and minus 1 dollar form the bank
                When user Click on the 5 dollar chip game will add 1 dollar to the bet 
                amount and minus 5 dollar form the bank
                When user Click on the 10 dollar chip game will add 1 dollar to the bet 
                amount and minus 10 dollar form the bank
                When user Click on the 20 dollar chip game will add 1 dollar to the bet 
                amount and minus 20 dollar form the bank
                When user Click on the 50 dollar chip game will add 1 dollar to the bet 
                amount and minus 50 dollar form the bank
                When user Click on the 100 dollar chip game will add 1 dollar to the bet 
                amount and minus 100 dollar form the bank
                When user Click on the 500 dollar chip game will add 1 dollar to the bet 
                amount and minus 500 dollar form the bank
                When user Click on the 1000 dollar chip game will add 1 dollar to the bet 
                amount and minus 1000 dollar form the bank
                When user Click on the 10000 dollar chip game will add 1 dollar to the bet 
                amount and minus 10000 dollar form the bank
                When user Click on the 100000 dollar chip game will add 1 dollar to the bet 
                amount and minus 100000 dollar form the bank
                When user Click on the 1000000 dollar chip game will add 1 dollar to the bet 
                amount and minus 1000000 dollar form the bank

                when bank is 0 or if player trying to bet more then the amount they have in the bank they 
                game will pop insufficient fund
                ''' 
                
                
                '''====================$1======================''' 
                if event.key == pygame.K_1 and not game_over_man and not AI:  
                    
                    if volume and bank > 0:
                        effect2.play()                    
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,260))
                   
                    if bank > 0:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,260))
                        bet = bet + 1
                        bank = bank -1
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                    
                
                '''====================$5======================'''                        
                if event.key == pygame.K_2 and not game_over_man and not AI:  
                    
                    
                    if volume and bank >= 5:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,260))
                    
                    if bank >= 5 :
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,260))
                        bet = bet + 5
                        bank = bank -5
                    else: 
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                        
                
                '''====================$10======================'''                                                   
                if event.key == pygame.K_3 and not game_over_man and not AI:
                    
                    if volume and bank >= 10:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,340))
                                            
                    if bank >= 10 :
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,340))
                        bet = bet + 10
                        bank = bank -10
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$20======================'''         
                if event.key == pygame.K_4 and not game_over_man and not AI:
                    
                    if volume and bank >= 20:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,340))
                    
                    if bank >= 20:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,340))
                        bet = bet + 20
                        bank = bank -20
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$50======================'''         
                if event.key == pygame.K_5 and not game_over_man and not AI:
                    
                    if volume and bank >= 50:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,420))
                    
                    if bank >= 50:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,420))
                        bet = bet + 50
                        bank = bank -50
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$100======================'''         
                if event.key == pygame.K_6 and not game_over_man and not AI:
                    
                    if volume and bank >= 100:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,420))
                   
                    if bank >= 100:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,420))
                        bet = bet + 100
                        bank = bank -100
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$500======================'''         
                if event.key == pygame.K_7 and not game_over_man and not AI:
                    
                    if volume and bank >= 500:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,500))
                    
                    if bank >= 500:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,500))
                        bet = bet + 500
                        bank = bank -500
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$1000======================'''         
                if event.key == pygame.K_8 and not game_over_man and not AI:
                    
                    if volume and bank >= 1000:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,500))
                    
                    if bank >= 1000:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,500))
                        bet = bet + 1000
                        bank = bank -1000
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                    
                
                '''====================$10000======================'''  
                if bank >= 10000 :       
                    if event.key == pygame.K_9 and not game_over_man and not AI:
                        
                        if volume and bank >= 10000:
                            effect2.play()
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,580))                 
                        
                        if bank >= 10000:
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,580))
                            bet = bet + 10000
                            bank = bank -10000
                        else:
                            text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                            screen.blit(text_surface, (325, 550)) 
                
                
                '''====================$100000======================'''   
                if bank >= 100000 :      
                    if event.key == pygame.K_0 and not game_over_man and not AI:
                        
                        if volume and bank >= 100000:
                            effect2.play()
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,580))                  
                        
                        if bank >= 100000:
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,580)) 
                            bet = bet + 100000
                            bank = bank -100000
                        else:
                            text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                            screen.blit(text_surface, (325, 550))
                
                
                '''====================$1000000======================'''
                if bank >= 1000000 :         
                    if event.key == pygame.K_m and not game_over_man and not AI:
                        
                        if volume and bank >= 1000000:
                            effect2.play()
                            screen.blit(pygame.image.load('Cards/buttonpres2.png'), (1090,220))
                       
                        if bank >= 1000000:
                            screen.blit(pygame.image.load('Cards/buttonpres2.png'), (1090,220))
                            bet = bet + 1000000
                            bank = bank -1000000
                        else:
                            text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                            screen.blit(text_surface, (325, 550))
                    
                     
            
            
            ''' 
            =================================================MOUSE CLICKS============================================= 
            this where Mouse Clicks event gets implemented 
            user can Click on Hit button to Hit
            user can Click on Stick button to Stick
            user can Click on Volume button to mute/unmet
            '''
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouseX, mouseY = pygame.mouse.get_pos()
                #print(mouseX, mouseY)
                
                ''' if user click on the volume icon the volume will stop'''
                if mouseX >= 1000 and mouseX <= 1050 and mouseY >= 210 and mouseY <= 260:
                    volume = not volume

                if mouseX >= 1000 and mouseX <= 1190 and mouseY >= 20 and mouseY <= 108 and not AI:
                    players_or_AI_cards.append(hit(len(players_or_AI_cards), True))
                    
                    if volume:
                        effect.play()
                    
                if mouseX >= 1000 and mouseX <= 1190 and mouseY >= 120 and mouseY <= 210 and not AI: 
                    dealer = True
                    
                    for i in dealers_cards:
                        i.draw_card() 
                        i.reveal_card()
                    while check_for_Sum(dealers_cards) <= dealer_deal_limit:
                        dealers_cards.append(hit(len(dealers_cards), False))

            

                '''
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 1 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 5 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 10 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 20 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 50 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 100 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 500 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 1000 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 10000 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 100000 dollar form the bank
                When user Click on the 1 dollar chip game will add 1 dollar to the bet amount and minus 1000000 dollar form the bank

                when bank is 0 or if player trying to bet more then the amount they have in the bank they 
                game will pop insufficient fund               
                '''
                
                '''====================$1======================''' 
                if mouseX >= 80 and mouseX <= 150 and mouseY >= 260 and mouseY <= 330 and not AI:
                    
                    if volume and bank > 0:
                        effect2.play()                    
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,260))
                   
                    if bank > 0:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,260))
                        bet = bet + 1
                        bank = bank -1
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))                    


                '''====================$5======================''' 
                if mouseX >= 165 and mouseX <= 235 and mouseY >= 260 and mouseY <= 330 and not AI: 
                    
                    if volume and bank >= 5:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,260))
                    
                    if bank >= 5 :
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,260))
                        bet = bet + 5
                        bank = bank -5
                    else: 
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$10======================'''         
                if mouseX >= 80 and mouseX <= 150 and mouseY >= 340 and mouseY <= 410 and not AI: 

                    if volume and bank >= 10:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,340))
                                            
                    if bank >= 10 :
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,340))
                        bet = bet + 10
                        bank = bank -10
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))   
                
                
                '''====================$20======================'''         
                if mouseX >= 165 and mouseX <= 235 and mouseY >= 340 and mouseY <= 410 and not AI: 

                    if volume and bank >= 20:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,340))
                    
                    if bank >= 20:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,340))
                        bet = bet + 20
                        bank = bank -20
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$50======================'''         
                if mouseX >= 80 and mouseX <= 150 and mouseY >= 420 and mouseY <= 490 and not AI: 
 
                    if volume and bank >= 50:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,420))
                    
                    if bank >= 50:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,420))
                        bet = bet + 50
                        bank = bank -50
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$100======================'''         
                if mouseX >= 165 and mouseX <= 235 and mouseY >= 420 and mouseY <= 490 and not AI: 
 
                    if volume and bank >= 100:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,420))
                   
                    if bank >= 100:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,420))
                        bet = bet + 100
                        bank = bank -100
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                
                
                '''====================$500======================'''         
                if mouseX >= 80 and mouseX <= 150 and mouseY >= 500 and mouseY <= 570 and not AI: 
                    
                    if volume and bank >= 500:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,500))
                    
                    if bank >= 500:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,500))
                        bet = bet + 500
                        bank = bank -500
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
               
               
                '''====================$1000======================'''         
                if mouseX >= 165 and mouseX <= 235 and mouseY >= 500 and mouseY <= 570 and not AI: 
 
                    if volume and bank >= 1000:
                        effect2.play()
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,500))
                    
                    if bank >= 1000:
                        screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,500))
                        bet = bet + 1000
                        bank = bank -1000
                    else:
                        text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                        screen.blit(text_surface, (325, 550))
                        
                
                '''====================$10000======================''' 
                if bank >= 10000:        
                    if mouseX >= 80 and mouseX <= 150 and mouseY >= 580 and mouseY <= 650 and not AI: 
 
                        if volume and bank >= 10000:
                            effect2.play()
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,580))                 
                        
                        if bank >= 10000:
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (80,580))
                            bet = bet + 10000
                            bank = bank -10000
                        else:
                            text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                            screen.blit(text_surface, (325, 550))  
                        
                        
                '''====================$100000======================'''  
                if bank >= 100000:       
                    if mouseX >= 165 and mouseX <= 235 and mouseY >= 580 and mouseY <= 650 and not AI: 

                        if volume and bank >= 100000:
                            effect2.play()
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,580))                  
                        
                        if bank >= 100000:
                            screen.blit(pygame.image.load('Cards/buttonpres.png'), (165,580)) 
                            bet = bet + 100000
                            bank = bank -100000
                        else:
                            text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                            screen.blit(text_surface, (325, 550))      
                
                
                '''====================$1000000======================'''  
                if bank >= 1000000:       
                    if mouseX >= 1090 and mouseX <= 1190 and mouseY >= 220 and mouseY <= 370 and not AI: 
                        
                        if volume and bank >= 1000000:
                            effect2.play()
                            screen.blit(pygame.image.load('Cards/buttonpres2.png'), (1090,220))
                       
                        if bank >= 1000000:
                            screen.blit(pygame.image.load('Cards/buttonpres2.png'), (1090,220))
                            bet = bet + 1000000
                            bank = bank -1000000
                        else:
                            text_surface, rect = GAME_FONT.render(("Insufficient Fund"), pygame.Color('red'))
                            screen.blit(text_surface, (325, 550))
                        
        '''=======================================END OF MOUSE CLICK================================================='''                
                        
                                                                                                                                                                                                                         
                      
        pygame.display.update()
        
    pygame.display.quit()


 
#this will call the main method
if __name__ == "__main__":
    main()