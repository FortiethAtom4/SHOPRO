from abc import ABC, abstractmethod

class Effect(ABC):


















    #this class MAY NOT BE defunct???? But very overcomplicated. Only needs name, logic string, and maybe a func to do effect resolution to make my life easier. 



    @abstractmethod
    def __init__(self,card,condition,zone,type,target,value): #this seems clunky, may need more lists.
        self.card = card
        self.condition = condition
        self.zone = zone #what zone it can be activated in
        self.type = type #what type of effect is it
        self.target = target
        self.value = value

        self.conditionMet = False
        self.isKyara = False
   
    def is_kyara(self):
        self.isKyara = True
    
    def resolve_effect(self): #target keywords in txt doc: self, player, card [card_name or prompt]
        if self.conditionMet:
            match self.type:
                case "damage": #target is player.
                    self.target.set_hp(self.target.get_hp() - self.value)

                case "gainACP": #target is player (typically self).
                    self.target.set_acp(self.target.get_acp() + self.value)

                case "gainHP": #target is player (typically self).
                    self.target.set_hp(self.target.get_hp() + self.value)

                case "coinflip": #because of course. Syntax in txt file: coinflip [effect to activate if heads] [effect to activate if tails]
                    pass

                case "summon": #target is card [prompt player, or otherwise choose target].
                    pass
            self.conditionMet = False


class SpecialEffect(Effect):
    def __init__(self): #this seems clunky, may need more lists.
        super().__init__()

    def get_zone(self):
        return self.zone

    def resolve_effect(self):
        super().resolve_effect()            

    def activate_effect(self):
        match self.condition:
            case "tap": #activation cost is tap, zone is field.
                if self.card.get_is_tapped():
                    print("card is already tapped and cannot activate. ")
                    # time.sleep(1.5)
                else:
                    self.card.tap()
                    self.conditionMet = True
                    

            case "sacrifice": #activation cost is sacrifice, zone is (typically) field.
                pass

class PassiveEffect(Effect):
    def __init__(self):
        super().__init__()

    def resolve_effect(self):
        super().resolve_effect() 
    
    def activate_effect(self):
        match self.condition:
            case "summon":
                pass
            case "tap": #for other cards besides self.
                pass
        pass

    
