from cmath import cos, phase
from difflib import Match
from math import fabs
from operator import index
from posixpath import split
from turtle import pos
from player import Player
from zone import FaceUpZone, FaceDownZone
from card import Kyara, Event #and club member... eventually.... pain
import os
import time
import re

import pygame #comin up

def get_next_string(string = str, index = int, end_char = str): #NOTE: you can make newlines in effect text using the backslash ("\").
    i = index
    newstr = ""
    while string[i] != end_char and i < len(string) - 1:
        if string[i] == "\\":
            newstr = newstr + '\n'
        else:
            newstr = newstr + string[i]
        i += 1
    
    return newstr

def check_in_list(string = str,list = list):
    if string in list:
        return string
    return "invalid"

def split_logic(logic = str): #returns a list of elements in a line of card logic, keeping blocks in curly brackets as one element. May be defunct.
    split_logic = []
    temp_brackets = ""
    logic.split()
    for i in range(0,len(logic)):
        if "{" in logic[i]:
            logic[i].replace("{","")
            while "}" not in logic[i]:
                temp_brackets = temp_brackets + logic[i] #does not currently account for nested sets of curly brackets. Hopefully that isn't necessary, but may be later.
                i += 1
            logic[i].replace("}","")
            temp_brackets = temp_brackets + logic[i]
            split_logic.append(temp_brackets)
            temp_brackets = ""
        else:
            split_logic.append(logic)
    return split_logic

def read_in_kyara(line): #assumes we know that properly formatted Kyara data is on that line

    #init order in class: name, cost, image, text, sex, age

    i = 7
    card_name = get_next_string(line,i,'\"')
    i += len(card_name) + 2
    card_sex = get_next_string(line,i,' ')
    i += len(card_sex) + 1
    temp_age = get_next_string(line,i,' ')
    card_age = int(temp_age)
    i += len(temp_age) + 1
    temp_cost = get_next_string(line,i,' ')
    card_cost = int(temp_cost)
    i += len(temp_cost) + 2
    temp_effect_text = get_next_string(line,i,'\"')
    i += len(temp_effect_text) + 3
    temp_eff_string = get_next_string(line,i,"]")
    effect_logic = []
    temp = ""
    sum = 0
    for i in range(temp_eff_string.count("|") + 1):
        temp = get_next_string(temp_eff_string,sum,"|") #TODO: not working properly.
        effect_logic.append(temp)
        sum += len(temp) + 1
    temp = ""
    sum = 0
    effect_text = []
    for i in range(temp_effect_text.count('\n') + 1): 
        temp = get_next_string(temp_effect_text,sum,'\n')
        effect_text.append(temp)
        sum += len(temp) + 1
    #TODO: image path
    #TODO: check to be sure that number of text and number of logic strings match. Otherwise there will be problems.

    newcard = Kyara(card_name, card_cost, "", effect_text, card_sex, card_age, effect_logic)
    return newcard

def read_in_event(line): #name,image,text, effect
    i = 7
    card_name = get_next_string(line,i,'\"')
    i += len(card_name) + 3
    effect_text = get_next_string(line,i,'\"')
    i += len(effect_text) + 3
    effect_logic = get_next_string(line,i,"]")

    #TODO: image path

    newcard = Event(card_name,"",effect_text,effect_logic)
    return newcard

class Game():
    def __init__(self):
        self.cards = []
        self.turns = [] #append something after each end phase. length of array % 2 + 1 determines the numbered player's turn (1 for p1, 2 for p2). len / 2 + 1 is current turn number.
        #player 1 zones
        self.p1_hand = FaceUpZone() 
        self.p1_deck = FaceDownZone()
        self.p1_field = FaceUpZone()
        self.p1_discard = FaceUpZone()
        self.p1_shadow_realm = FaceUpZone()
        

        self.p1 = Player(20,0,self.p1_deck,self.p1_field,self.p1_hand,self.p1_discard,self.p1_shadow_realm) 

        #player 2 zones
        self.p2_hand = FaceUpZone()
        self.p2_deck = FaceDownZone()
        self.p2_field = FaceUpZone()
        self.p2_discard = FaceUpZone()
        self.p2_shadow_realm = FaceUpZone()

        self.p2 = Player(20,0,self.p2_deck,self.p2_field,self.p2_hand,self.p2_discard,self.p2_shadow_realm)

        #Market
        self.market_kyaras = FaceUpZone()
        self.market_kyaras_pile = FaceDownZone()
        self.market_events = FaceDownZone()

        self.club_members = FaceUpZone() 

        #game iterates on this list to determine whose turn it is.
        self.players = [self.p1,self.p2]

        self.effect_stack = [] #current activated effects
        self.passive_effects = {} #check this after each action if conditions have been met.

        self.current_events = []
        self.phase = 0 #6 phases total


    def read_cards(self): #do card reading stuff. TODO: separate Kyaras into their respective shows, somehow.
        filepath = "cards.txt" #future players must ensure cards.txt is in the game file as the rest of the game. For now.
        with open(filepath, "r", encoding="utf8") as cardfile:
            card_info = cardfile.readlines() #and thats it for the file i guess?

        card_types = ["Kyara","Event","ClubMember"]

        for card_line in card_info:
            card_line.rstrip()

            card_type = check_in_list(get_next_string(card_line,0,' '),card_types)

            match card_type:
                case "Kyara": 
                    self.cards.append(read_in_kyara(card_line))

                case "Event":
                    self.cards.append(read_in_event(card_line))

                case "ClubMember": #TODO
                    pass

                case _:
                    print("Invalid card found.")
                    continue

    def print_cards(self): #for testing purposes.
        for card in self.cards:
            print(card.get_name() + " Cost: " + str(card.get_cost()))

    def display_field(self):
        os.system('cls||clear')
        if len(self.turns) % 2 == 0:
            print("Player 2 HP: " + str(self.p2.get_hp()) + " ",end='')
            self.p2.print_health_bar()
            print("Player 2's hand: ")
            print("Deck: ",end='')
            self.p2.deck.display()
            print("  ",end='')
            self.p2_hand.print_card_list()
            print()
            print("Player 2's field:")
            self.p2.field.print_card_list()
            print("\n\n\nMARKET")
            self.market_kyaras_pile.display()
            print("  ",end='')
            self.market_kyaras.print_card_list()
            print("  Events: ",end='')
            self.market_events.display()
            print("\n\n\n")
            print("Your field:")
            self.p1.field.print_card_list()
            print()
            print("Your hand: ")
            self.p1_hand.print_card_list()
            print("   Deck: ",end='')
            self.p1.deck.display()
            print()
            print("Your HP: " + str(self.p1.get_hp()) + " ",end='')
            self.p1.print_health_bar()
            print()
        else:
            print("Player 1 HP: " + str(self.p1.get_hp()) + " ",end='')
            self.p1.print_health_bar()
            print("Player 1's hand: ")
            print("Deck: ",end='')
            self.p1.deck.display()
            print("  ",end='')
            self.p1_hand.print_card_list()
            print()
            print("Player 1's field:")
            self.p1.field.print_card_list()
            print("\n\n\nMARKET")
            self.market_kyaras_pile.display()
            print("  Events: ",end='')
            self.market_kyaras.print_card_list()
            print("  ",end='')
            self.market_events.display()
            print("\n\n\n")
            print("Your field:")
            self.p2.field.print_card_list()
            print()
            print("Your hand:")
            self.p2_hand.print_card_list()
            print("   Deck: ",end='')
            self.p2.deck.display()
            print()
            print("Your HP: " + str(self.p2.get_hp()) + " ",end='')
            self.p2.print_health_bar()
            print()

    def check_command(self):
        action = input("Type the name of a card to see details about it: ").rstrip()
        card_found = False
        for card in self.cards:
            if card.get_name().casefold() == action.casefold(): #may need to do some text normalization during file processing. see NKFD normalization documentation for more.
                card.print_detailed_card()
                
                card_found = True

        if not card_found:
            print("Error: No card of that name found in the database. ")
            time.sleep(1.5)

    def start_of_game(self):
        i = 0
        self.read_cards()
        
        x = 0
        for card in self.cards:
            self.players[x].deck.append_card(card)
            match card.get_type():
                case "Kyara":    
                    self.market_kyaras_pile.append_card(card)
                case "Event":
                    self.market_events.append_card(card)
            x = (x + 1) % 2
            
        self.p1.deck.shuffle()
        self.p2.deck.shuffle()

        while i < 2:
            self.p1.draw_card(False)
            self.p2.draw_card(False)
            i += 1
        self.p2.draw_card(False)
        
        self.market_kyaras_pile.shuffle()
        while self.market_kyaras.get_num_of_cards() < 4:
            self.market_kyaras.append_card(self.market_kyaras_pile.draw_card())

    def check_victory(self):
        count = len(self.players)
        winning_player = 0
        for i in range(0,len(self.players)):
            if self.players[i].hasLost() or self.players[i].get_hp() <= 0:
                self.players[i].lose()
                count -= 1
            else:
                winning_player = i
        if count == 1:
            return winning_player
        return -1

    def faceup_zone_input(self,zone = FaceUpZone, input_text = str): #TODO: allow for input from multiple faceup zones
        action = input(input_text + "\nInput: ") 
        if not action.isnumeric() or int(action) > zone.get_num_of_cards() or int(action) <= 0:
            print("Error: Invalid card number.")
            time.sleep(1.5)
        else:
            return action
        return "invalid"

    def event_phase(self,curr_player = Player,global_actions = list,is_first_phase = bool):
        action = ""
        event_phase_actions = ["summon","effect","event","market"]
        self.display_field()
        print("It's Player " + str(len(self.turns) % 2 + 1) + "'s turn.")
        print("ACP: " + str(curr_player.get_acp()))

        action = input("Type a command. Possible commands: "+ ", ".join(event_phase_actions) + ", " + ", ".join(global_actions) + "\nInput: ").strip()
        match action:

            case "print":
                #do whatever printing you need for testing purposes here.
                curr_player.field.print_card_list()
                action = input("press enter to continue.")
                return "print"

            case "end":
                if is_first_phase:
                    return "end 2"
                else:
                    return "end 4"

            case "summon":
                action = self.faceup_zone_input(curr_player.hand,"Type the number of a card in your hand to summon it.")
                if action != "invalid":
                    if curr_player.hand.get_card_at_index(int(action) - 1).get_type() != "Kyara":
                            print("Error: That card is not a Kyara and cannot be summoned.")
                            time.sleep(1.5)
                            return "invalid"
                    else:
                        if curr_player.get_acp() < curr_player.hand.get_card_at_index(int(action) - 1).get_cost():
                            print("Error: You don't have enough ACP to summon that card.")
                            time.sleep(1.5)
                            return "invalid"
                        else:  #success
                            curr_card = curr_player.hand.get_card_at_index(int(action) - 1).get_name()
                            curr_card = curr_player.hand.find_card(curr_card) #curr_card is now a Card object.

                            #pay ACP first. duh. (#NOTE stub for passive fx to change this if necessary)
                            curr_player.set_acp(curr_player.get_acp() - curr_card.get_cost())
                            return "summon \"" + curr_card.get_name() + "\""
                else:
                    return "invalid"

            case "effect":
                eff_cards = FaceUpZone()

                for card in curr_player.hand.get_card_list() + curr_player.field.get_card_list() + curr_player.discard.get_card_list():
                    for eftype in card.get_effect_logic():
                        if ("s " in eftype) and card.get_type() == "Kyara":

                            if card not in eff_cards.get_card_list() and ("field" in eftype and card in curr_player.field.get_card_list()) or \
                            ("hand" in eftype and card in curr_player.hand.get_card_list()) or \
                            ("discard" in eftype and card in curr_player.discard.get_card_list()):
                                eff_cards.append_card(card)

                if eff_cards.get_num_of_cards() == 0:
                    print("Error: no Kyaras with special effects are available.")
                    time.sleep(1.5)
                    return "invalid"
                else:
                    print("\nAvailable special effect cards: ",end='')
                    eff_cards.print_card_list()
                    print()
                    eff_card = self.faceup_zone_input(eff_cards,"Choose the card whose effect you would like to activate.").strip()
                    pass
                    if eff_card != "invalid" and eff_card.isnumeric():
                        eff_card = eff_cards.get_card_at_index(int(eff_card) - 1)
                        to_activate = []
                        for val in eff_card.get_effect_logic():
                            if val[0] == 's':
                                if "field" in val and eff_card in curr_player.field.get_card_list() or \
                                    "hand" in val and eff_card in curr_player.hand.get_card_list() or \
                                    "discard" in val and eff_card in curr_player.discard.get_card_list():
                                    #TODO: now I've done this same ridiculous if statement twice. Try to cut down to 1 later.
                                    to_activate.append(val)
                            
                        if len(to_activate) > 1:
                            for i in range(len(to_activate)):
                                print(str(i + 1) + ": " + str(to_activate[i]))
                            chosen_effect = input("Type in the number of an effect to activate it: ").strip()
                            if not chosen_effect.isnumeric() or int(chosen_effect) < 1 or int(chosen_effect) > len(to_activate):
                                print("Error: Invalid effect number.")
                                time.sleep(1.5)
                                return "invalid"
                            else:
                                return self.activate_effect(eff_card, str(to_activate[int(chosen_effect) - 1]))

                        else:
                            return self.activate_effect(eff_card,to_activate[0])
                    else:
                        return "invalid"

            case "event":
                event_cards = FaceUpZone()
                for card in curr_player.hand.get_card_list():
                    if card.get_type() == "Event":
                        event_cards.append_card(card)
                if event_cards.get_num_of_cards() == 0:
                    print("Error: No Event cards available.")
                    time.sleep(1.5)
                    return "invalid"
                else:
                    print("\nAvailable Event cards: ",end='')
                    event_cards.print_card_list()
                    print()
                    chosen_event = self.faceup_zone_input(event_cards,"Choose the Event card you would like to activate.")
                    if chosen_event != "invalid":
                        chosen_event = event_cards.get_card_at_index(int(chosen_event) - 1)
                        return self.activate_effect(chosen_event,chosen_event.get_effect_logic())
                    else:
                        return "invalid"
                        

            case "market":
                action = input("Enter one of the following: kyara, event, club member: ").strip(" ")
                match action:

                    case "kyara": #View Kyaras available to buy.
                        action = self.faceup_zone_input(self.market_kyaras,"Type the number of a kyara in the market to select it (1 - 4).")
                        if action != "invalid":
                            c = int(action) - 1
                            self.market_kyaras.get_card_at_index(c).print_detailed_card()
                            action = input("Commands: buy [cost = 1 ACP], replace, exit: ").strip()
                            match action:
                                case "buy": #buy a Kyara.
                                    if curr_player.get_acp() < 1:
                                        print("Error: Not enough ACP to buy this card.")
                                        time.sleep(1.5)
                                        return "invalid"
                                    else: #success
                                        bought_kyara = self.market_kyaras.remove_card(c)
                                        curr_player.hand.append_card(bought_kyara)
                                        if self.market_kyaras_pile.get_num_of_cards() > 0:
                                            self.market_kyaras.append_card(self.market_kyaras_pile.draw_card())
                                        curr_player.set_acp(curr_player.get_acp() - 1)
                                        return "buy kyara \"" + bought_kyara.get_name() + "\""

                                case "replace": #Replace a Kyara in the Market. Can only be done once per turn.
                                    if curr_player.shuffled():
                                        print("Error: already shuffled once this turn. ")
                                        time.sleep(1.5)
                                        return "invalid"
                                    else: #success
                                        if self.market_kyaras_pile.get_num_of_cards() > 0:
                                            ck = self.market_kyaras.remove_card(c)
                                            self.market_kyaras_pile.shuffle_in(ck)
                                            self.market_kyaras.append_card(self.market_kyaras_pile.draw_card())
                                            curr_player.shuffle(True)
                                            return "replace \"" + ck.get_name() + "\""
                                        else:
                                            print("Error: no more replacement cards in Market.")
                                            time.sleep(1.5)
                                            return "invalid"

                                case "exit":
                                    return "invalid"

                                case _:
                                    print("Error: Unknown command.")
                                    time.sleep(1.5)
                                    return "invalid"

                        else:
                            return "invalid"

                    case "event": #Buy an Event card from the Market.
                        action = (input("Are you sure you want to buy an Event card for 2 ACP? y/n: ").strip()).casefold()
                        match action:
                            case "yes" | "y":
                                if curr_player.get_acp() < 2:
                                    print("Error: Not enough ACP to buy an Event card.")
                                    time.sleep(1.5)
                                    return "invalid"
                                elif self.market_events.get_num_of_cards() < 1:
                                    print("Error: no Event cards left in Market.")
                                    time.sleep(1.5)
                                    return "invalid"
                                else: #success
                                    bought_event = self.market_events.draw_card()
                                    curr_player.hand.append_card(bought_event)
                                    return "buy event \"" + bought_event.get_name() + "\""
                            case _:
                                return "invalid"
                    
                    case "clubmember":
                        return "bruh"
                        #TODO stub to come back to after the rest of the game is done, if possible.

                    case _:
                        print("Error: not a known card type.")
                        time.sleep(1.5)
                        return "invalid"
                

            
            case "check":
                self.check_command()
                return "check"

            case "ff":
                print("You surrendered.")
                curr_player.lose()
                return "ff"

            case _:
                print("Command not recognized.")
                time.sleep(1.5)
                return "invalid"

    def get_effect_value(self,string = str): #get an integer value to apply to a given effect.
        if string.isnumeric():
            return int(string)
        else:
            
            #TODO: some regex shenanigans.
            #have some keywords/prompts for getting numeric values from game logic.
            pass
        return 0 #placeholder return for now.

    def activate_effect(self,eff_card,eff_string = str): #does cost-paying etc. for activated effects.

        eff_string_temp = eff_string[1:eff_string.find(">")].strip()

        zone_words = ["hand","field","discard"]
        for word in zone_words: #removes zone indicator from effect logic for ease of use. Not removed from actual string.
            eff_string_temp = eff_string_temp.replace(word,"")
        
        #finds all costs required to activate effect. Costs are separated by the '&' character in the .txt file.
        #if only one effect found, temp string is made into a list and processed as normal.
        if eff_string_temp.count('&') > 0:
            first_effect = re.search('[^&]+(?=&)',eff_string_temp).group()
            eff_string_temp = re.findall('(?<=&)[^&]+',eff_string_temp)
            eff_string_temp.insert(0,first_effect)
        else:
            #if only one cost, it still needs to be in list form to be processed. Thus this weird little line.
            eff_string_temp = [eff_string_temp]

        #NOTE: USE THIS REGEX FOR EFFECT RESOLUTION!!!!!!!!!!!!!!

        #will use exec() to execute strings of card-related code. Not very secure, but the only solution i have for now.
        costs_to_pay = []
        

        #str structure: condition [value] & condition [value] & condition [value]....
        #Not all costs have a value (e.g. tap).

        #creating variables to be updated for exec() later. Again, not secure, so try to change later.
        current_player = self.players[len(self.turns) % 2] #A current_player variable. Comes in handy.
        target_player = self.players[(len(self.turns) + 1) % 2]
        action = ""
        pay_value = ""


        for cost in eff_string_temp:
            cost = cost.strip().split()

            match cost[0]:
                case "tap": #tap a card for effect activation.
                    if eff_card.get_is_tapped():
                        print("Error: card is already tapped and cannot activate its effect.")
                        time.sleep(1.5)
                        return "invalid"
                    else:
                        costs_to_pay.append("eff_card.tap()")

                case "pay_acp": #pay ACP for effect activation.
                    pay_value = self.get_effect_value(cost[1])
                    if current_player.get_acp() < pay_value:
                        print("Error: Not enough ACP to pay for this effect activation.")
                        time.sleep(1.5)
                        return "invalid"
                    else:
                        costs_to_pay.append("current_player.set_acp(current_player.get_acp() - pay_value)")

                case "pay_hp": #pay HP for effect activation.
                    pay_value = self.get_effect_value(cost[1])
                    if current_player.get_hp() <= pay_value:
                        print("Error: Not enough HP to pay for this effect activation.")
                        time.sleep(1.5)
                        return "invalid"
                    else:
                        costs_to_pay.append("current_player.set_hp(current_player.get_hp() - pay_value)")

                case "return_to_hand": #target cards on your field to return to hand.
                    if current_player.field.get_num_of_cards() < 1:
                        print("Error: No cards to return to hand.")
                        time.sleep(1.5)
                        return "invalid"
                    else:
                        current_player.field.print_card_list()
                        print()
                        action = self.faceup_zone_input(current_player.field,"Type the number of a Kyara to return to your hand: ")
                        if action != "invalid":
                            costs_to_pay.append("current_player.hand.append_card(current_player.field.remove_card(int(action) - 1))")
                        else:
                            return "invalid"
                    
                case "sacrifice": #target cards on your field to send to the discard pile.
                    if current_player.field.get_num_of_cards() < 1:
                        print("Error: No cards to sacrifice.")
                        time.sleep(1.5)
                        return "invalid"
                    else:
                        current_player.field.print_card_list()
                        print()
                        action = self.faceup_zone_input(current_player.field,"Type the number of a Kyara to sacrifice: ")
                        if action != "invalid":
                            costs_to_pay.append("current_player.discard.append_card(current_player.field.remove_card(int(action) - 1))")
                        else:
                            return "invalid"
                
                case "target": #target cards on the opponent's field.
                    num_targets = self.get_effect_value(cost[1])
                    target_names = []
                    if(num_targets > target_player.field.get_num_of_cards()):
                        print("Error: not enough targets.")
                        time.sleep(1.5)
                        return "invalid"

                    target_player.field.print_card_list()
                    print()
                    for i in range(num_targets):
                        action = self.faceup_zone_input(target_player.field,"Type the number of a Kyara to target for this effect: ")
                        if action != "invalid":
                            targeted_card = target_player.field.get_card_at_index(int(action) - 1).get_name()
                            if targeted_card in target_names:
                                print("Kyara already targeted.")
                                time.sleep(1.5)
                                i -= 1
                                continue
                            target_names.append("\"" + targeted_card + "\"")
                        else:
                            return "invalid"
                    
                    cost[1] = "target " + ",".join(target_names)
                    eff_string = eff_string.replace("target",cost[1])
                    #nothing to send to costs_to_pay, since targeted cards are otherwise unaffected until resolution.
                
                case "event": #Events cost nothing to activate. Generally speaking.

                    #Just need to discard the event card and we're good.
                    card_to_remove = current_player.hand.find_card_index(eff_card.get_name())
                    current_player.discard.append_card(current_player.hand.remove_card(card_to_remove))

                case _:
                    print("System error: Activation cost type \"" + cost[0] + "\" not recognized.")
                    time.sleep(1.5)
                    return "invalid"

        #The offending line. I intend to replace this with cases in resolve_event, though.
        for line in costs_to_pay:
            exec(line)

        return "effect \"" + eff_card.get_name() + "\" " + eff_string


    def resolve_event(self,current_event):
            
        #current player setup. Comes in handy for targeting.
        current_player = self.players[(len(self.turns)) % 2] 
        target_player = self.players[(len(self.turns) + 1) % 2]

        match get_next_string(current_event,0," ").strip(): 

            case "end": #end of phase
                #TODO for later: wait for p fx stuff
                phase_num = current_event.split()[1]
                match phase_num:
                    case "0":
                        phase_num = "Start Phase"
                    case "1":
                        phase_num = "Standby Phase"
                    case "2":
                        phase_num = "Event Phase 1"
                    case "3":
                        phase_num = "Attack Phase"
                    case "4":
                        phase_num = "Event Phase 2"
                    case "5":
                        phase_num = "End Phase"
                print(f"{phase_num} ended.")
                self.phase = (self.phase + 1) % 6

            case "ff": #surrender
                current_player.lose()

            case "attack": #card has been designated to attack.
                attacking_card_name = re.search('"[^"]*"',current_event).group(0).replace("\""," ").strip()
                attacking_card = current_player.field.find_card(attacking_card_name)
                target_player.set_hp(target_player.get_hp() - 1)
                attacking_card.reset_attack()
                self.current_events.append("tap \"" + attacking_card_name + "\"")

            case "tap": #card has been tapped.
                tap_card = re.search('"[^"]*"',current_event).group(0).replace("\""," ").strip()
                tap_card = current_player.field.find_card(tap_card)
                tap_card.tap()

            case "summon": #card has been summoned by game mechanic (rather than by an effect).
                summon_card_name = re.search('"[^"]*"',current_event).group(0).replace("\""," ").strip()
                summon_card = current_player.hand.find_card_index(summon_card_name)
                current_player.field.append_card(current_player.hand.remove_card(summon_card))
                print(f"You summoned {summon_card_name}.")


            case "effect": #A special effect has been activated.

                #str structure: effect card_name [s/p] [zone] [conditions] > [effect] [effect_value]. 
                # the > is a key char separating conditions and effects.
                

                index_of_eff = current_event.find(">") + 2
                eff_string = current_event[index_of_eff:]

                eff_string_temp = eff_string.strip()
                if eff_string_temp.count('&') > 0:
                    first_effect = re.search('[^&]+(?=&)',eff_string_temp).group()
                    eff_string_temp = re.findall('(?<=&)[^&]+',eff_string_temp)
                    eff_string_temp.insert(0,first_effect)
                else:
                    eff_string_temp = [eff_string_temp]

                for effect in eff_string_temp:
                    effect_temp = effect.strip().split() #TODO: function to split(), keeping special strings grouped.
                    match effect_temp[0]:

                        #TODO stub for unique effects ('housepet', etc.) after everything else is finished.

                        #Generic effect resolution.
                        case "damage": #opponent loses HP.
                            damage_value = self.get_effect_value(effect_temp[1])
                            target_player.set_hp(target_player.get_hp() - damage_value)
                            print(f"Your opponent lost {damage_value} HP.")

                        case "heal": #opponent gains HP.
                            heal_value = self.get_effect_value(effect_temp[1])
                            target_player.set_hp(target_player.get_hp() + heal_value)
                            print(f"Your opponent gained {heal_value} hp.")

                        case "gain_acp": #current player gains ACP.
                            acp_value = self.get_effect_value(effect_temp[1])
                            current_player.set_acp(current_player.get_acp() + acp_value)
                            print(f"You gained {acp_value} ACP.")

                        case "gain_hp": #current player gains HP.
                            hp_value = self.get_effect_value(effect_temp[1])
                            current_player.set_hp(current_player.get_hp() + hp_value)
                            print(f"You gained {hp_value} HP.")

                        case "lose_hp": #current player loses HP.
                            hp_value = self.get_effect_value(effect_temp[1])
                            current_player.set_hp(current_player.get_hp() - hp_value)
                            print(f"You lost {hp_value} HP.")

                        case "draw": #draw card_num number of cards.
                            card_num = self.get_effect_value(effect_temp[1])
                            for i in range(card_num):
                                current_player.draw_card(False)
                                drawn_card = current_player.hand.get_card_at_index(current_player.hand.get_num_of_cards() - 1).get_name()
                                print(f"You drew {drawn_card}.")

                        case "destroy": #destroy an opponent's targeted cards.
                            card_targets = re.findall('"[^"]*"',current_event[:index_of_eff - 2])
                            card_targets.pop(0) #pops the original card name from the targeting list. Whoops.
                            for target in card_targets:
                                target = target.replace("\"","")
                                target_player.discard.append_card(target_player.field.remove_card(target_player.field.find_card_index(target)))
                                print(f"You destroyed {target}.")
                            

                        case "search":
                            #syntax: search [zone] {tags} 
                            match current_event[2]: #needs fixing. current_event is no longer split into list form.
                                case "field":
                                    pass
                                case "deck":
                                    pass
                                case "discard":
                                    pass

                        case "summon": #the 'summon' keyword always refers to self. 
                            cardname = re.search('"[^"]*"',current_event).group(0).replace("\""," ").strip()
                            match effect[1]:
                                case "hand":
                                    target_card = current_player.hand.find_card(cardname)
                                    current_player.field.append_card(current_player.hand.remove_card(target_card))
                                    print(f"You summoned {cardname} from your hand.")
                                case "discard":
                                    current_player.field.append_card(current_player.discard.remove_card(current_player.discard.find_card(cardname)))
                                    print(f"You summoned {cardname} from your discard pile.")
                            

                        case "moveto": #this keyword is for summons of cards other than self.
                            pass #TODO

                        case "print":
                            print_string = " ".join(effect[1:])
                            print(print_string)

                #add more here. Also: will likely need to be recursive. 

                        case _:
                            print(f"System error: Effect type \"{effect[0]}\" not recognized.")
                            time.sleep(1.5)
                
                #TODO stub for passive fx after base game is finished.

    #does everything. 
    def run_game(self):
        victory = False
        self.start_of_game()
        acp_amt = 1
        global_actions = ["check","end","ff"]

        while not victory:
            curr_player = self.players[len(self.turns) % len(self.players)] #can now (possibly) have more than 2 players?
            if curr_player.hasLost():
                continue
            match self.phase:

                case 0: #draw phase ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    curr_player.draw_card(True)
                    curr_player.shuffle(False)

                    #ACP gain. +1 for turn 1, +2 for turn 2, and +3 thereafter.
                    if len(self.turns) > 3:
                        acp_amt = 3
                    elif len(self.turns) > 1:
                        acp_amt = 2
                    else: acp_amt = 1
                    curr_player.set_acp(curr_player.get_acp() + acp_amt)
                    
                    #untap cards.
                    for i in range(curr_player.field.get_num_of_cards()):
                        curr_player.field.get_card_at_index(i).untap()
                    self.current_events.append("end 0")

                case 1: #standby phase, just waiting for passive effects here tbh~~~~~~~~~~~
                    self.current_events.append("end 1")

                case 2: #event phase 1~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    self.current_events.append(self.event_phase(curr_player,global_actions,True))

                case 3: #battle phase #TODO: move to separate function. None of this append() garbage in my phases.~~~~~
                    action = -1
                    self.display_field()
                    print("Type the number of an untapped card on the field to prepare it for attack. Type 'attack' to launch attack.")
                    print("Other commands: " + ", ".join(global_actions))
                    action = input("Input: ").strip()

                    #player types number of a Kyara on the field to prepare them for attack.
                    if action.isnumeric():
                        action = int(action)
                        if action > curr_player.field.get_num_of_cards() or action <= 0:
                            print("Invalid card number.")
                            time.sleep(1.5)
                            self.current_events.append("invalid")
                        else:
                            attack_card = curr_player.field.get_card_at_index(action - 1)
                            if attack_card.get_is_tapped():
                                print("That card is tapped and cannot attack.")
                                time.sleep(1.5)
                                self.current_events.append("invalid")
                            elif attack_card.get_is_attacking():
                                print("That card is already prepared to attack.")
                                time.sleep(1.5)
                                self.current_events.append("invalid")
                            else:
                                attack_card.ready_to_attack()
                                self.current_events.append("invalid")
                    else:
                        match action:
                            case "attack": #attacks with all chosen Kyaras and ends phase.
                                for i in range (0,curr_player.field.get_num_of_cards()):
                                    tempcard = curr_player.field.get_card_at_index(i)
                                    if tempcard.get_is_attacking():
                                        self.current_events.append("attack \"" + tempcard.get_name() + "\"")
                                
                                self.current_events.append("end 3")

                            case "check":
                                self.check_command()
                                self.current_events.append("check")

                            case "end": #ends phase and resets and Kyaras that were prepped to attack.
                                for i in range (0,curr_player.field.get_num_of_cards()):
                                    curr_player.field.get_card_at_index(i).reset_attack()
                                self.current_events.append("end 3")

                            case "ff":
                                print("You surrendered.")
                                self.current_events.append("ff")

                            case _:
                                print("Error: unknown command.")
                                time.sleep(1.5)
                                self.current_events.append("invalid")

                    

                case 4: #event phase 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    self.current_events.append(self.event_phase(curr_player,global_actions,False))

                        

                case 5: #end phase ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #wait for effects somehow
                    while curr_player.hand.get_num_of_cards() > 5:
                        action = self.faceup_zone_input(curr_player.hand,"Hand size too large. type the number of a card in your hand to discard it.")
                        if action != "invalid":
                            removed_card = curr_player.hand.remove_card(int(action) - 1)
                            print("Discarded \"" + removed_card.get_name() + "\"")
                            curr_player.discard.append_card(removed_card)
                            self.current_events.append("discard \"" + removed_card.get_name() + "\"")

                    self.turns.append("pizza") #doesnt really matter what is appended to this list. Could be abused to have the program record replays.
                    print("Your turn ends.")
                    self.current_events.append("end 5")

            #event/phase checks and effect resolutions to be done at the end of each loop.
            #probably going to move this for loop to a resolve_effect func.

            #print(self.current_events)
            #time.sleep(1)

            #After each action, any actions added to the current_events list are resolved in last-in first-out order.
            while len(self.current_events) > 0:
                event = self.current_events[len(self.current_events) - 1]
                self.resolve_event(event)
                self.current_events.remove(event)
            

            #Cards should not be tapped when off the field.
            for card in curr_player.hand.get_card_list() + \
                curr_player.discard.get_card_list() + \
                self.players[(len(self.turns) + 1) % 2].hand.get_card_list() + \
                self.players[(len(self.turns) + 1) % 2].discard.get_card_list():

                if card.get_type() == "Kyara" and card.get_is_tapped():
                    card.untap()
               #NOTE stub for future card mechanics (namely counters) that will need checking here if implemented

            possible_win = self.check_victory()
            if possible_win != -1:
                print("Player " + str(possible_win + 1) + " wins!")
                victory = True
                continue
            input("Press Enter to continue. ")
        

    #*NOTE*: careful when making copies of Kyaras. Game does NOT make deep copies atm, so anything you do to 1 copy of a card will happen to ALL of them.

    #HIGH PRIORITY:
    #TODO: Type up a bunch of cards in cards.txt using the existing effect language. IN PROGRESS
    #TODO: Replace text-based gameplay with Pygame. IN PROGRESS
    #TODO: Create an AI opponent to replace player 2. COMING UP

    #LOWER PRIORITY:
    #TODO: Make conditions in resolve_event for the base game mechanics (e.g. buying kyaras) for consistency.
    #TODO: Club Members, eventually.
    #TODO: when current_events[] is fully up and running for ALL COMMANDS, establish Kyara passive effect recognition/activation/resolution.
    #TODO: add conditions during summoning queries for Kyaras with alternate/additional/optional summon costs. 
    

    #Broader goals: 
    #TODO: function to read in cards from an external text file. DONE
    #TODO: get game working with non-effect cards in a text-based format. DONE
    #TODO: Full text-based game functionality. DONE (base functionality)
    #TODO: use pygame to assemble a physical display of the game. Acquire card images, if necessary.
    #TODO: AI opponent for demonstration. 
    #~~~~~~~~~~~~~~~~~~~~~~~~EXTRA GOALS IF YOU'RE FEELING SPICY~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #TODO: Streamline and improve game interface. 
    #TODO: Utilize the self.turns attribute to put replay files together, allowing players to rewatch games.
    #TODO: Create deck builder interface, allowing players to create their own decks saved as separate .txt files.
    #TODO: randomly-generated cards??????
