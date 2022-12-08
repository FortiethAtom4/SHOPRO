import random
from abc import ABC, abstractmethod

class Zone(ABC):
    @abstractmethod
    def __init__(self):
        self.card_list = []

    def print_card_list(self):
        if len(self.card_list) == 0:
            print("[Empty]")
        for i in range(len(self.card_list)):
            print(str(i + 1) + ": ", end='')
            self.card_list[i].print_card()

    def get_num_of_cards(self):
        return len(self.card_list)

    def get_card_list(self):
        return self.card_list

    def shuffle(self):
        pass

    def display(self):
        pass

    def get_card_at_index(self,index):
        return self.card_list[index]

    def remove_card(self,index):
        return self.card_list.pop(index)

    def find_card_index(self,cardname):
        for i in range(len(self.card_list)):
            if self.card_list[i].get_name() == cardname:
                return i
        return "error"

    def append_card(self,newcard):
        self.card_list.append(newcard)

    def find_card(self,name):
        for card in self.card_list:
            if card.get_name() == name:
                return card
        return "error"


class FaceUpZone(Zone):
    def __init__(self):
        super().__init__()

    def get_card_list(self):
        
        super().get_card_list()

    def shuffle(self):
        pass #face up zones do not shuffle

    def display(self):
        pass #deal with this later

    def get_card_at_index(self,index):
        return self.card_list[index]

    def get_num_of_cards(self):
        return len(self.card_list)
    
    def append_card(self,newcard):
        self.card_list.append(newcard)

    def get_card_list(self):
        return super().get_card_list()

    def find_card(self, name):
        return super().find_card(name)

    def remove_card(self, index):
        return super().remove_card(index)
    


class FaceDownZone(Zone):
    def __init__(self):
        super().__init__()

    def shuffle(self):
        #shuffle the cards in a deck
        temp = self.card_list
        temp2 = []
        while len(temp) > 0:
            x = random.randint(0,len(temp) - 1)
            temp2.append(temp.pop(x))

        self.card_list.clear()
        self.card_list = temp2 #hopefully that's it, right?

    def get_card_at_index(self,index):
        return self.card_list[index]

    def get_num_of_cards(self):
        return len(self.card_list)

    def display(self):
        print("[" + str(len(self.card_list)) + "]",end='')

    def print_card_list(self): #for searching only. Generally stick to the 'display' function for a visual representation.
        super().print_card_list()

    def append_card(self,newcard):
        self.card_list.append(newcard)

    def remove_card(self, index):
        return super().remove_card(index)

    def shuffle_in(self,newcard):
        self.card_list.insert(random.randrange(0,len(self.card_list) - 1), newcard)

    def draw_card(self):
        return self.card_list.pop(len(self.card_list) - 1)

    def get_card_list(self):
        return super().get_card_list()

    def find_card(self, name):
        return super().find_card(name)