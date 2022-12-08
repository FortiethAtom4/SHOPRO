from zone import Zone
import time

class Player:
    def __init__(self,hp,acp,deck,field,hand,discard,shadowrealm):
        self.hp = hp #should default to 20 
        self.acp = acp #should default to 0
        self.deck = deck
        self.field = field
        self.hand = hand
        self.discard = discard
        self.shadowrealm = shadowrealm

        self.lost = False
        self.has_shuffled = False

    def draw_card(self,isDrawPhase = bool):
        if self.deck.get_num_of_cards() == 0:
            if isDrawPhase:
                print("Deck empty. Shuffling discard pile into deck...")
                if self.discard.get_num_of_cards() == 0:
                    print("No more cards in discard pile.")
                    return
                self.deck = self.discard
                self.discard.clear()
            else:
                print("no more cards to draw.\n")
                return
        self.hand.append_card(self.deck.remove_card(self.deck.get_num_of_cards()-1))

    def shuffle(self,shuffle = bool):
        self.has_shuffled = shuffle
    
    def shuffled(self):
        return self.has_shuffled

    def lose(self):
        self.lost = True

    def hasLost(self):
        return self.lost

    def get_hp(self):
        return self.hp

    def print_health_bar(self):
        print("[",end='')
        if self.hp <= 20:
            for i in range(0,self.hp*2):
                print("\u2588",end='')
            for i in range(self.hp*2,40):
                print(" ",end='')
        else:
            for i in range(0,self.hp*2):
                print("\u2588",end='')
        print("]")
    
    def set_hp(self,value):
        self.hp = value

    def get_acp(self):
        return self.acp

    def set_acp(self,value):
        self.acp = value
                
