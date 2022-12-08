#import pygame
from abc import ABC, abstractmethod
from player import Player


class Card(ABC):
    @abstractmethod
    def __init__(self,name,image,text):
       
        self.name = name
        self.player = ""
        self.image = image
        self.text = text #the official effects text.
        self.type = "null"
        self.owner = None

        self.tags = {} #To be used for series identification, counter bookkeeping, etc.


    def get_name(self):
        return self.name

    def set_name(self,newname):
        self.name = newname

    def get_cost(self):
        pass

    def print_card(self):
        pass

    def get_type(self):
        return self.type

    def get_effect_logic(self): #for the passive effect list.
        pass

    def set_owner(self,player = Player):
        self.owner = player

    def get_owner(self):
        return self.owner




class Kyara(Card):

    def __init__(self,name,cost,image,text,sex,age,effect):
        self.name = name
        self.cost = cost
        self.player = ""
        self.image = image
        self.sex = sex
        self.age = age

        self.is_attacking = False
        self.is_tapped = False

        self.effects = {}
        for i in range(len(text)):
            self.effects.update({text[i]:effect[i]})

        self.type = "Kyara"
        self.tags = {} #bookkeeping, update later TODO

    def get_name(self):
        return super().get_name()

    def ready_to_attack(self):
        self.is_attacking = True

    def reset_attack(self):
        self.is_attacking = False

    def get_is_attacking(self):
        return self.is_attacking

    def get_is_tapped(self):
        return self.is_tapped

    def tap(self):
        self.is_tapped = True

    def untap(self):
        self.is_tapped = False

    def print_card(self):
        print("[" + self.name + " ("+ str(self.cost) +")", end='')
        if self.is_tapped:
            print(" tapped]", end=' ')
        elif self.is_attacking:
            print(" attacking]", end=' ')
        else:
            print("]",end=' ')

    def print_detailed_card(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(self.name)
        print("Sex: " + self.sex + ", Age: " + str(self.age))
        print("Cost: " + str(self.cost))
        print("Effects:\n")
        for eff in self.effects.keys():
            print(eff)
        print(f"\nEffect logic (printed for testing purposes): \n{self.effects}") 
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def get_type(self):
        return super().get_type()

    def get_effects(self): #returns the entire dictionary.
        return self.effects
        
    
    def get_cost(self):
        return self.cost

    def get_effect_logic(self): #for the effect logic list.
        return self.effects.values()
    
    def get_owner(self):
        super().get_owner()

    def set_owner(self, player):
        super().set_owner(player)

class Event(Card):

    def __init__(self,name,image,text,effect):
        self.name = name
        self.player = ""
        self.image = image
        self.text = text #the official effects text.
        self.effect = effect #the unprocessed effects logic.

        self.type = "Event"
        self.cost = 2


    def print_card(self):
        print("[Event: " + self.name + "] ", end='')

    def print_detailed_card(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Event: "+ self.name)
        print("\n" + self.text)
        print("\nEffect logic: (printed for testing purposes):") 
        print(self.effect)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def get_cost(self):
        return self.cost

    def get_type(self):
        return super().get_type()

    def get_effect_logic(self): #for the effect list.
        return self.effect

    def set_owner(self, player):
        super().set_owner(player)

    def get_owner(self):
        super().get_owner()


    

