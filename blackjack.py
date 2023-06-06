from queue import Empty
from random import random

from bjgui import *
import time
import sys
import random

class Game:
    Players = []
    def __init__(self):
        app = QApplication(sys.argv)
        self.GameActive = True
        self.GameControl()
        sys.exit(app.exec_())

    def GameControl(self):
        OurDeck = Deck()
        OurPlayer = Player()
        #Add Player and Dealer to GAme
        self.Players.append(OurPlayer)
        dealer = Player()
        dealer.name = "Dealer"
        self.Players.append(dealer)
        ourwindow = MainWindow(OurPlayer)

        #Menu Loop
        while self.GameActive:
            self.printMenuOptions()
            wannaplay = input("---------------------\nInput: ")
            if wannaplay == "Play":
                if OurPlayer.bankroll == 0:
                    print("Please Deposit First")
                else:
                    OurDeck.shuffle()
                    newRound = Round(self.Players, OurDeck)
            elif wannaplay == "Add":
                depositing = True
                while depositing:
                    deposit = input("\nHow much do you want to add: ")
                    try:
                        OurPlayer.bankroll += int(deposit)
                        print("\nDeposit successful, new balance is ${}".format(int(OurPlayer.bankroll)))
                        time.sleep(1.5)
                        depositing = False
                    except:
                        print("\nNot a valid deposit amount try again")
            elif wannaplay == "Balance":
                print("\nYou have ${}".format(OurPlayer.bankroll))
            elif wannaplay == "Help":
                self.printMenuOptions()
            elif wannaplay == "Exit":
                self.GameActive = False      
                exit()      
            else:
                print("\nPlease enter a valid command, Type 'Help' to see all commands")
        return OurPlayer

    def printMenuOptions(self):
        print("---------------------\n'Play' to Start the game\n'Balance' to see bankroll\n'Add' to add funds\n'Exit' to quit \n'Help' to show these options again")       

class Round:
    def __init__(self,playerlist,playingdeck):
        for player in playerlist:
            if player.name != "Dealer":
                player.currentwager = self.GetWager(player)
        time.sleep(1.5)
        print("---------------------\nWagering Complete, Dealing cards")
        self.DealRound(playerlist, playingdeck)
        self.PrintHands(playerlist, "HiddenPhase")
        busterbrown = self.PlayerAction(playerlist,playingdeck)
        if busterbrown == False: self.DealerAction(playerlist,playingdeck)
        self.CheckSuccess(playerlist)

        for a in playerlist:
            a.resethand()
    
    def GetWager(self,playerwagering):
        wagering = True
        while wagering:
            wager = input("\nYou have ${} How much do you want to wager: ".format(playerwagering.bankroll))
            try:
                wager = int(wager)
                if wager > 0 and wager <= playerwagering.bankroll:
                    playerwagering.bankroll -= wager
                    print("\nWagering ${}, new balance is ${}".format(wager, int(playerwagering.bankroll)))
                    wagering = False
                    return wager
                else:
                    print("\nPlease enter a valid wager amount, within your balance")
            except:
                print("\nNot a valid wager amount try again")        

    def DealRound(self, playerlist, playingdeck):
        dealing = True
        while dealing:
            for a in playerlist:
                firstdrawncard = playingdeck.draw()
                a.hand.append(firstdrawncard)
            for b in playerlist:
                seconddrawncard = playingdeck.draw()
                b.hand.append(seconddrawncard)
            dealing = False

    def PrintHands(self, playerlist, state):
        if state == "HiddenPhase":
            for player in playerlist:
                if player.name != "Dealer":
                    time.sleep(1.5)
                    print("\n" + player.name + "'s Cards")
                    player.showhand()
                    player.calchandvalue()
                else:
                    time.sleep(1.5)
                    print("\n" + player.name + "'s Cards")
                    time.sleep(1.5)
                    print("?? Unknown ??")
                    player.hand[1].show()
                    time.sleep(1.5)
        elif state == "DealerPhase":
            for player in playerlist:
                print("\n" + player.name + "'s Cards")
                player.showhand()
                player.calchandvalue()
        
    def PlayerAction(self, playerlist,playingdeck):
        actioning = True
        while actioning:
            for player in playerlist:
                if player.name != "Dealer":
                    if player.handscore < 21:
                        playerinput = input("---------------------\nType 'H' to hit 'S' to stay: ")
                        if playerinput == "H":
                            time.sleep(1.5)
                            print("\nHit me!\n")
                            newcard = playingdeck.draw()
                            newcard.show()
                            player.hand.append(newcard)
                            self.PrintHands(playerlist, "HiddenPhase")
                        if playerinput == "S":
                            time.sleep(1.5)
                            actioning = False
                            print("\nI'll Stay")
                            time.sleep(1.5)
                            print("\n---------------------\nDealer shows his cards")
                            self.PrintHands(playerlist,"DealerPhase")
                            return False
                    if player.handscore == 21:
                        print("---------------------\n\nBlackjack!\n")
                        self.PrintHands(playerlist,"DealerPhase")
                        actioning = False;
                        return False
                    if player.handscore > 21:
                        time.sleep(1.5)
                        print("---------------------\n\nYou busted!\n")
                        actioning = False
                        return True

    def DealerAction(self, playerlist,playingdeck):
            actioning = True
            while actioning:
                for player in playerlist:
                    if player.name == "Dealer":
                        if player.handscore <= 21:
                            if player.handscore < 17:
                                time.sleep(1.5)
                                print("---------------------\nDealer hits\n")
                                newcard = playingdeck.draw()
                                newcard.show()
                                player.hand.append(newcard)
                                self.PrintHands(playerlist, "DealerPhase")
                            if player.handscore >= 17:
                                time.sleep(1.5)
                                actioning = False
                                if player.handscore < 21:
                                    print("---------------------\nDealer Stays.\n")
                                if player.handscore > 21:
                                    print("\nDealer Busts!!\n")
                        else:
                            time.sleep(1.5)
                            print("---------------------\nDealer busted!\n")
                            time.sleep(1.5)
                            actioning = False
                            self.PrintHands(playerlist,"DealerPhase")

    def CheckSuccess(self, playerlist):
        dealerscore = 0
        for ourplayer in playerlist:
            if(ourplayer.name == "Dealer"):
                dealerscore = ourplayer.handscore
        for ourplayer in playerlist:
            if(ourplayer.name != "Dealer"):
                playerscore = ourplayer.handscore
                time.sleep(1.5)
                if((ourplayer.handscore <=21 and int(playerscore) > int(dealerscore)) or (ourplayer.handscore <= 21 and dealerscore > 21)):
                    print("Player {} scores {} Dealer scores {}".format(ourplayer.name, playerscore, dealerscore))
                    print("Player {} wins ${}!!".format(ourplayer.name, ourplayer.currentwager))
                    ourplayer.bankroll += ourplayer.currentwager * 2
                elif(ourplayer.handscore <= 21 and playerscore == dealerscore):
                    print("Player {} scores {} Dealer scores {}".format(ourplayer.name, playerscore, dealerscore))
                    print("Player {} Pushes".format(ourplayer.name))
                    ourplayer.bankroll += ourplayer.currentwager
                else:
                    if ourplayer.handscore > 21:
                        print("Player {} scores {} Dealer scores ??".format(ourplayer.name, playerscore, dealerscore))
                    else:
                        print("Player {} scores {} Dealer scores {}".format(ourplayer.name, playerscore, dealerscore))
                    print("Player {} Loses".format(ourplayer.name))
        time.sleep(1.5)

    #Deal is One up to each player, One down to dealer, second up to player, second dealer up

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.pointval = 0
        self.imagename = ""
        self.secondpointval = 0
        
        self.assignval()
        self.imgname()
        
    def imgname(self):
        self.imagename = "./PlayingCards./"+str(self.val) + str(self.suit) + ".png"

    def show(self):
        time.sleep(1.5)
        if self.val == "A":
            print("[{}] of [{}] value is [{}] or [{}]".format(self.val, self.suit, self.pointval, self.secondpointval))
        else:
            print("[{}] of [{}] value is [{}]".format(self.val, self.suit, self.pointval))
    
    def assignval(self):
        if self.val in ["2", "3", "4", "5","6","7","8","9","10"]:
            self.pointval = int(self.val)
        elif self.val == "J" or self.val == "Q" or self.val == "K":
            self.pointval = 10
        elif self.val == "A":
            self.pointval = 11
            self.secondpointval = 1

    def Draw():
        pixmapxx = QPixmap('./PlayingCards./2Hearts.png')
        pixmapxx = pixmapxx.scaled(128, 128, Qt.KeepAspectRatio)
        


class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.originalcount = 52
    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]:
                self.cards.append(Card(s,v))
    def showdeck(self):
        for a in self.cards:
            a.show()
    def shuffle(self):
        random.shuffle(self.cards)
    def draw(self):
        try:
            ourcard = self.cards.pop(0)
        except:
            print("New deck.. Shuffling")
            self.build()
            self.shuffle()
            ourcard = self.cards.pop(0)
            ourcard.Draw()
        return ourcard
    def countdeck(self):
        return 52 - len(self.cards)
            


class Player:
    def __init__(self):
        self.hand = []
        self.name = "Placeholder"
        self.bankroll = 0
        self.handscore = 0
        self.currentwager = 0
        self.acecount = 0

    def showhand(self):
        for a in self.hand:
            a.show()

    def resethand(self):
        self.hand = []

    def calchandvalue(self):
        self.handscore = 0 
        for a in self.hand:
            self.handscore += int(a.pointval)
            if a.val == "A":
                self.acecount += 1
            while self.handscore > 21 and self.acecount > 0:
                self.acecount -= 1
                self.handscore -= 10
        self.acecount = 0
        time.sleep(1.5)
        print("Hand value is " + str(self.handscore))

if __name__ == '__main__':
       ourGame = Game()
