import pygame
import random

pygame.init()
window = pygame.display.set_mode((1400,703))
pygame.display.set_caption("FIFA Packs")

class Card():
    def __init__(self, player_img = None, player_img_path = None, Rect = None, rectX = 0, rectY = 0):
        self.rectX = rectX
        self.rectY = rectY
        self.rect = pygame.rect.Rect(self.rectX, self.rectY, 156, 221)
        self.player_img = player_img
        self.player_img_path = player_img_path

    #####__eq__ and __hash__ are used to for removing duplicate Card objects from a list later on
    #####__lt__ is used for sorting the user's club (or inventory)
    def __eq__(self, other):
        return card_rep_int(self) == card_rep_int(other)
    def __hash__(self):
        return card_rep_int(self)
    def __lt__(self, other):
        return card_rep_int(self) < card_rep_int(other)
    ####

    ####Change player_image_path to a random image path taken from the global PlayerImgPaths list, then load and scale into player_img
    def New_Image(self):
        self.player_img_path = random.choice(PlayerImgPaths)
        self.player_img = pygame.image.load(self.player_img_path).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (156,221))
    ####

    ####Set player_image_path to a random image path taken from the global PlayerImgPaths list, then load and scale into player_img
    def SET_IMAGE(self, path):
        self.player_img_path = path
        self.player_img = pygame.image.load(self.player_img_path).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (156,221))
    ####

    def GET_IMAGE_PATH(self):
        for i in range(len(AllPlayerImages)):
            if self.player_img_path == PlayerImgPaths[i]:
                return PlayerImgPaths[i]
            else:
                return self.player_img_path
                
    def Display_Img(self, x, y):
        window.blit(self.player_img, (x , y))

    def MOVE_RECT(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def DISPLAY_RECT(self):
        pygame.draw.rect(window, (0, 0, 0), self.rect)

    def getRect(self):
        return self.rect

    def getImage(self):
        return self.player_img
class Pack():
    def __init__(self, name, price, size, playerImgObjs = [], zero = [], cardRecs = []):
        self.name = name
        self.price = price
        self.size = size
        self.playerImgObjs = playerImgObjs
        self.zero = zero
        self.cardRecs = cardRecs
       
    def check_if_same(self, imgObjs): #Checks if there are Cards within a Pack that are the same. Returns false if they are all different, Returns true if at least one is the same. 
        temp = [int(card_rep(imgObjs[i])) for i in range(self.size)]
        
        seen = set()
        for x in temp:
            if x in seen:
                 return True
            seen.add(x)
        return False
    
    def Display_Players(self, imgObjs): # Display all Card objects, then wait for key press to continue
        x = 0
        y = 100
        if len(imgObjs) < 1 or len(imgObjs) == None or imgObjs == None:
            return
        else:
            for i in range(len(imgObjs)):
                if i == 0:
                    x = 20
                else:
                    x += 200
                    
                imgObjs[i].MOVE_RECT(x,y)
                #imgObjs[i].DISPLAY_RECT()    <--- Used for debugging
                imgObjs[i].Display_Img(x, y)

        pygame.display.flip()
        GAME_STATE["canClick"] = False
        #self.wait_for_key_press()
               
    def wait_for_key_press(self): #Continue and reset the list of Cards only if designated key is pressed
        r = True
        while r:
            try:  
                if keyboard.is_pressed('q'):
                    self.RESET_PLAYERS()
                    r = False
                    break  
                else:
                    pass
            except:
                break
    
    def RESET_PLAYERS(self): #Set to empty list
        self.playerImgObjs = self.zero
     
    def Open(self): #Updates GAME STATE, if player has enough coins to open a pack, returns a List of Card objects. Else, returns an empty list
        
        ##Update the Game State dictionary
        GAME_STATE["Latest Pack"] = self.name
        GAME_STATE["Number of Players in Latest Pack"] = self.size
        ##
       
        if GAME_STATE["Number of Coins"] >= self.price:
            GAME_STATE["Number of Coins"] -= self.price
           
            ##Instantiate i amount of Card images into a temporary array, where i is the size of pack
            ##Instantiate j amount of Card image recs into a temporary array, where j is the size of the original array
            temp = [Card() for i in range(self.size)]
            for i in range(len(temp)):
                temp[i].New_Image()
            ##
            
            #######If there any duplicates within the list of Cards, replace with a new list until there are none
            def o():
                nonlocal temp
                if not self.check_if_same(temp): #if ALL Card objects are different
                    return temp
                else:
                    temp = [Card() for i in range(self.size)] #if at least ONE repeat Card object, create new Cards
                    for i in range(len(temp)):
                        temp[i].New_Image()
                    o()       
            o()
            ########

            ##set the instance variable list of Card objects to the newly instantiated list of Card objects then return
            self.playerImgObjs = temp
            
            return self.playerImgObjs
            ##
        else:
            print("Not Enough Coins")#PLACEHOLDER - WILL IMPLEMENT DISPLAY IN GAME 
            GAME_STATE["notEnoughCoins"] = True
            return self.zero
class MyClubPlayers():
    clubPlayerPaths = []
    clubPlayers = []
    x = 0
    y = 0

    def __init__(self, Rect = None, rectY = 100):
        self.rectY = rectY
        self.rect = pygame.rect.Rect(self.x, self.rectY, 156, 221)

    def Sort(self, type = "DESC"):
        if type == "DESC":
            self.clubPlayers.sort()
        elif type == "ASC":
            self.clubPlayers.sort(reverse = True)

    def Display(self):
         for i in range(len(self.clubPlayers)):
            if i == 0 or i % 10 == 0:
                self.x = 15
                if i == 0 and i % 10 == 0:
                    self.y = 75
                else:
                    self.y += 200
            else:
                self.x += 135
            self.clubPlayers[i].MOVE_RECT(self.x, self.y)
            self.clubPlayers[i].Display_Img(self.x, self.y) 

####Initial Variables
TOTAL_NUM_PLAYERS = 305
TOTAL_NUM_ICONS = 59
NUM_COINS = 12000
PACK_PRICES = {"Two Player Pack": 700, "Four Player Pack": 1100, "Seven Player Pack": 1800}
GAME_STATE = {"Latest Pack": "N/A", "Number of Players in Latest Pack": 0, "Number of Coins": NUM_COINS, "canClick": True, "displayClub": False, "clubSize": 0, "displayNotEnoughCoins": False}
####

#####Fill array with every player card image using the array PlayerImgPaths (which is the sum of arrays of specific player images)
AllPlayerImages = []
IconPlayerImgPaths = ['Images/Players/' + str(i-264) + '.png' for i in range(TOTAL_NUM_ICONS+1)]
GoldPlayerImgPaths = ['Images/Players/' + str(i + 1) + '.png' for i in range(TOTAL_NUM_PLAYERS)]
PlayerImgPaths = IconPlayerImgPaths + GoldPlayerImgPaths
for i in range(TOTAL_NUM_PLAYERS):
    AllPlayerImages += [pygame.image.load(PlayerImgPaths[i]).convert_alpha()]
    AllPlayerImages[i] = pygame.transform.scale(AllPlayerImages[i], (156,221))
#####

######All the types of packs
TwoPlayerPack = Pack("Two Player Pack", PACK_PRICES["Two Player Pack"], 2)
FourPlayerPack = Pack("Four Player Pack", PACK_PRICES["Four Player Pack"], 4)
SevenPlayerPack = Pack("Seven Player Pack", PACK_PRICES["Seven Player Pack"], 7)
######

##Used to store all the players that the user clicked (basically like an inventory)
club = MyClubPlayers()
##

def card_rep_int(c):
    return int(card_rep(c))

def card_rep(c):
    #'Images/Players/XX.png'
    #Where XX is a 1 or 2 digit number and 'XX' is a string of said number
    d = c.GET_IMAGE_PATH().split('/')
    #['Images', 'Players', 'XX.png'] 
    p = d[2].split('.')
    #['XX', 'png']
    p.remove(p[1])
    #['XX']
    i = p[0]
    #'XX'
    return i

Card.__repr__ = card_rep #Used for debugging and storing Cards in club (inventory)

def UpdateCoinText():
    text_NumCoins = font2.render(" " + str(GAME_STATE["Number of Coins"]) + " ", True, yellow, black)
    textRect_NumCoins = text_Coins.get_rect()  
    textRect_NumCoins.center = (230 // 2, 100 // 2)
    window.blit(text_NumCoins, textRect_NumCoins)

########################All text elements and corresponding rects
black = (0,0,0) 
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
font = pygame.font.Font('EASPORTS.ttf', 22)
font2 = pygame.font.Font('eafont.ttf', 22)
text_TwoPP = font.render(' Two Player Pack ', True, white, black)
textRect_TwoPP = text_TwoPP.get_rect()
textRect_TwoPP.center = (740 // 2, 300 // 2)
text_FourPP = font.render(' Four Player Pack ', True, white, black)
textRect_FourPP = text_FourPP.get_rect()
textRect_FourPP.center = (1340 // 2, 300 // 2)
text_SevenPP = font.render(' Seven Player Pack ', True, white, black)
textRect_SevenPP = text_SevenPP.get_rect()
textRect_SevenPP.center = (1940 // 2, 300 // 2)
text_Coins = font2.render(" Coins: ", True, white, black)
textRect_Coins = text_Coins.get_rect()
textRect_Coins.center = (100 // 2, 100 // 2)
text_MyClub = font2.render(" View My Club ", True, white, black)
textRect_MyClub = text_Coins.get_rect()
textRect_MyClub.center = (1600 // 2, 1000 // 2)
text_Back = font2.render(" Back ", True, white, black)
textRect_Back = text_Back.get_rect()
textRect_Back.center = (465, 500)
text_NotEnoughCoins = font2.render(" Not Enough Coins ", True, red, black)
textRect_NotEnoughCoins = text_NotEnoughCoins.get_rect()
textRect_NotEnoughCoins.center = (700, 200)
########################

###########All Inital/Main/Deafult images and corresponding rects
TwoPP_Image = pygame.image.load('images/twopppack.png').convert_alpha()
TwoPP_Rect= TwoPP_Image.get_rect()
TwoPP_Rect.center = (365,300)
FourPP_Image = pygame.image.load('images/fourppack.png').convert_alpha()
FourPP_Rect= FourPP_Image.get_rect()
FourPP_Rect.center = (665,300)
SevenPP_Image = pygame.image.load('D:\Python Programming\CS2021_Scott_Hunt_Final_Project\Images\sevenppack.png').convert_alpha()
SevenPP_Rect= SevenPP_Image.get_rect()
SevenPP_Rect.center = (965,300)
transparent = pygame.image.load('D:\Python Programming\CS2021_Scott_Hunt_Final_Project\Images\def.png').convert_alpha()
###########

###Used for storing/manipulating data in the main loop
Opened_Pack = []
Pack_Card_Recs = []
Club_Card_Recs = []
###

####Make all Card object lists = []
def RESET_ALL_PLAYERS():
    TwoPlayerPack.RESET_PLAYERS()
    FourPlayerPack.RESET_PLAYERS()
    SevenPlayerPack.RESET_PLAYERS()

#Function name is self explanatory <-- CREDIT TO GeeksForGeeks.com for this function
def Remove_Duplicates(list):
    temp = [] 
    for elem in list: 
        if elem not in temp: 
            temp += [elem] 
    return temp

#This is used in the main game loop to check for clicks on a card object, and stores clicked Cards to MyClubPlayers
def AddToClub():
    for i in range(len(Pack_Card_Recs)):             
        r = Pack_Card_Recs[i]
        if r.collidepoint(x,y):
            club.clubPlayers += [Opened_Pack[i]] #clubPlayers is a list of Card objects
            club.clubPlayerPaths += ['images/Players/' + card_rep(Opened_Pack[i]) + '.png'] 

#This is used in the main game loop to check for clicks on a card object, and if that Card is already in MyClubPlayers, then quick sell them
def QuickSell():
    #Store the rects of each Card in the user's club into an array
    Club_Card_Recs = [club.clubPlayers[i].getRect() for i in range(len(club.clubPlayers))]
    for i in range(len(club.clubPlayers)):
        if Club_Card_Recs[i].collidepoint(x,y) and GAME_STATE['displayClub'] == True:
            if card_rep_int(club.clubPlayers[i]) < 0:
                GAME_STATE["Number of Coins"] += 500
            else:
                GAME_STATE["Number of Coins"] += 75
            club.clubPlayers.remove(club.clubPlayers[i])
            club.clubPlayerPaths.remove(club.clubPlayerPaths[i])

run = True
while run:
    ######################################################################
    '''
     Check for events (clicks,key binds, etc) then update display AFTER
                                                                      '''
    ######################################################################
    for event in pygame.event.get():     
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if textRect_Back.collidepoint(x,y):
                print("Clicked Back")
                Opened_Pack, Pack_Card_Recs = [], []
                TwoPP_Image = pygame.image.load('images/twopppack.png').convert_alpha()
                FourPP_Image = pygame.image.load('images/fourppack.png').convert_alpha()
                SevenPP_Image = pygame.image.load('D:\Python Programming\CS2021_Scott_Hunt_Final_Project\Images\sevenppack.png').convert_alpha()
                textRect_Back.center = (465, 500)
                textRect_MyClub.center = (1600 // 2, 1000 // 2)
                textRect_TwoPP.center = (740 // 2, 300 // 2)
                textRect_FourPP.center = (1340 // 2, 300 // 2)
                textRect_SevenPP.center = (1940 // 2, 300 // 2)
                RESET_ALL_PLAYERS()
                GAME_STATE["canClick"] = True
                GAME_STATE['displayClub'] = False
                GAME_STATE['displayNotEnoughCoins'] = False
                if len(club.clubPlayers) is not 0:
                    print("My Club: " + str(club.clubPlayers))

            if textRect_MyClub.collidepoint(x,y) and GAME_STATE["canClick"] == True:
                print("Viewing my club...")
                TwoPP_Image, FourPP_Image, SevenPP_Image = transparent, transparent, transparent
                textRect_Back.center = (500, 50)
                textRect_MyClub.center, textRect_TwoPP.center, textRect_FourPP.center, textRect_SevenPP.center = (-5000,0), (-5000,0),(-5000,0),(-5000,0)
                GAME_STATE["canClick"] = False
                GAME_STATE['displayClub'] = True
                
            if TwoPP_Rect.collidepoint(x,y) and GAME_STATE["canClick"] == True:
                print("Opening Two Player Pack...")
                TwoPP_Image, FourPP_Image, SevenPP_Image = transparent, transparent, transparent
                textRect_TwoPP.center, textRect_FourPP.center, textRect_SevenPP.center = (-5000,0), (-5000,0), (-5000,0)
                if GAME_STATE["Number of Coins"] < PACK_PRICES["Two Player Pack"]:
                    GAME_STATE["displayNotEnoughCoins"] = True
                else:
                    Opened_Pack = TwoPlayerPack.Open()
                    Pack_Card_Recs = [Opened_Pack[i].getRect() for i in range(len(Opened_Pack))]
             
            if FourPP_Rect.collidepoint(x,y) and GAME_STATE["canClick"] == True:
                print("Opening Four Player Pack...")
                TwoPP_Image, FourPP_Image, SevenPP_Image = transparent, transparent, transparent
                textRect_TwoPP.center, textRect_FourPP.center, textRect_SevenPP.center = (-5000,0), (-5000,0), (-5000,0)
                if GAME_STATE["Number of Coins"] < PACK_PRICES["Four Player Pack"]:
                    GAME_STATE["displayNotEnoughCoins"] = True
                else:
                    Opened_Pack = FourPlayerPack.Open()
                    Pack_Card_Recs = [Opened_Pack[i].getRect() for i in range(len(Opened_Pack))]
           
            if SevenPP_Rect.collidepoint(x,y) and GAME_STATE["canClick"] == True:
                print("Opening Seven Player Pack...")
                TwoPP_Image, FourPP_Image, SevenPP_Image = transparent, transparent, transparent
                textRect_TwoPP.center, textRect_FourPP.center, textRect_SevenPP.center = (-5000,0), (-5000,0), (-5000,0)
                if GAME_STATE["Number of Coins"] < PACK_PRICES["Seven Player Pack"]:
                    GAME_STATE["displayNotEnoughCoins"] = True
                else:
                    Opened_Pack = SevenPlayerPack.Open()
                    Pack_Card_Recs = [Opened_Pack[i].getRect() for i in range(len(Opened_Pack))]

            AddToClub()
            QuickSell()
                                     
        if event.type == pygame.QUIT:
            run = False  
            
    club.clubPlayers = Remove_Duplicates(club.clubPlayers)
    club.clubPlayerPaths = Remove_Duplicates(club.clubPlayerPaths)

    GAME_STATE["clubSize"] = len(club.clubPlayers)

    back = pygame.image.load('images/back.jpg').convert()
    back = pygame.transform.scale(back, (1400,703))
    window.blit(back, (0,0))
    window.blit(text_TwoPP, textRect_TwoPP)
    window.blit(text_FourPP, textRect_FourPP)
    window.blit(text_SevenPP, textRect_SevenPP)
    window.blit(text_Coins, textRect_Coins)
    window.blit(text_MyClub, textRect_MyClub)
    window.blit(text_Back, textRect_Back)
    window.blit(TwoPP_Image, TwoPP_Rect)
    window.blit(FourPP_Image, FourPP_Rect)
    window.blit(SevenPP_Image, SevenPP_Rect)

    if GAME_STATE['displayNotEnoughCoins'] == True:
        window.blit(text_NotEnoughCoins, textRect_NotEnoughCoins)

    if GAME_STATE['displayClub'] == True:
        club.Sort(type = "DESC")
        club.Display()

    UpdateCoinText()

    TwoPlayerPack.Display_Players(Opened_Pack)
    FourPlayerPack.Display_Players(Opened_Pack)
    SevenPlayerPack.Display_Players(Opened_Pack)

    if GAME_STATE["clubSize"] == TOTAL_NUM_PLAYERS:
        run = False

    pygame.display.flip()
pygame.display.quit()
pygame.quit()


