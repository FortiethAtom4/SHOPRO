# SHOPRO
Repository of my code on a Python version of a card game I made with my friends.

As of 12/23/2022, SHOPRO will run in an interpreter as long as you have all the files. However, the code is poorly documented, so it can be a pain to read through for unfamiliar programmers. In the future I will organize/add tags to my code so the average nerd can understand it. But for now it remains as a block of text to just download and try out.

The game comes with a limited default stock of cards. HOWEVER, card creation is extremely easy and a card can be created with a single line of text.
Thus, players of SHOPRO are encouraged to use the effect logic available to create cards of their own, explained in detail below. 

In the future, card logic will be improved and given access to more interesting effects. 

~~~~~~~~~~~~~~GAME RULES~~~~~~~~~~~~~~
(Note: players familiar with complex card games such as Magic: the Gathering or Yu-Gi-Oh will recognize the general game structure.)

SHOPRO is played by two players. Both players start with a deck of cards and 20 HP (Hitpoints). The goal of the game is to
use the cards in your deck and cards bought in the Market to "beat some ass," i.e. to reduce your opponent's HP to 0. 

There are two types of cards (a third type is coming in the future):

Kyara cards: Cards which represent a character and can be 'summoned' to the field to attack or activate effects.
In the original game, Kyaras often represented anime or video game characters. 

Event cards: Cards which can be played from the hand without cost for one-time special effects. 
In the original game, Events were often styled after real-life events which happened to our friend group.

Kyaras, Market transactions, and some effects use a resource called ACP. ACP is gained passively each turn, and some
effects can grant bonus ACP. ACP can be spent immediately or saved for a future turn.

Players take turns. Each turn has a rigid structure to follow:
-Start Phase: Player gains ACP and draws a card. On a player's first turn, they gain 1 ACP, on the second they gain 2, and from the third onwards they gain 3 ACP.
(Note: If your deck is out of cards to draw, the game will deposit your discarded cards into your deck and draw from there. The concept of "decking out" does not exist in SHOPRO.)
-Standby Phase: A phase for some effect resolution. No actions can be taken at this time, except for some effects which specifically state this phase.
-Event Phase: During this phase, the player may summon Kyaras, activate effects, play Event cards, or buy new cards from the Market.
-Attack Phase: During this Phase, the player may choose to attack with a set number of untapped Kyaras (explained below) they control. Damage dealt is equal to the number of Kyaras chosen to attack.
-Event Phase 2: During this phase, the player may again summon Kyaras, activate effects, play Event cards, and buy new cards from the Market.
-End Phase: A phase indicating the end of a turn. A player may not take actions during this phase, except for some specific effects which mention this phase.

Kyara effects often come with a cost. A typical cost for a Kyara effect is to "tap" that Kyara. In the original version of the game, this was represented by turning the Kyara card sideways, reminiscent of the tapping mechanic in Magic. A Kyara that has been tapped cannot be untapped until the beginning of your next turn. Some other effect costs may include paying HP, ACP, or even sacrificing other cards you control. 

Event cards are one-time-use and typically do not have a cost (though a cost can be included, if desired). 


~~~~~~~~~~~~~~INSTRUCTIONS FOR MAKING NEW CARDS~~~~~~~~~~~~~~
The file "cards.txt" contains all the cards the game will use. Anyone can easily add cards to the game or edit existing ones by editing this file.
Each card is a collection of text and logic on one line.

Cards can have as many effects on them as you want, even 0 if you would like. 
HOWEVER, each effect MUST have a corresponding effect text (texts separated by the \ symbol).
Even a blank effect explanation is fine, as long as there is at least one \ to show where the text would be. 
Otherwise that effect WILL NOT BE PROCESSED.

Kyara card structure:
Kyara "Name" [gender/sex (or whatever)] [age] [acp_cost] "Effect Type: 'Effect Name' - Effect text" [ effect_logic ]

Example Kyara card:
Kyara "Test Dummy 3" F 22 1 "Special Effect: 'Cool Effect Name' - Lose 3 HP and gain 3 ACP" [s field tap > lose_hp 3 & gain_acp 3 ]

Event card structure: 
Event "Name" "Effect text" [effect_logic]

Example Event card:
Event "Get Flamed" "Deal 2 damage to your opponent." [s event > damage 2]

As the reader can likely tell, there are special characters which the interpeter recognizes. Below is a comprehensive list of them with explanations:

'[]' - All effect logic for a card must be placed between square brackets at the end of the card line.

'>' - The dividing character between effect cost and effect resolution. this character is necessary for any effect, otherwise it will not work.

'&' - This character can be used to concatenate costs or resolutions to make more complex effects.
Example usage:
Event "All or Nothing" "Lose 5 HP. Draw 2 cards. gain 2 ACP." [s event & pay_hp 5 > draw 2 & gain_acp 2]
This Event card has only one effect. However, it has two costs (the 'event' placeholder cost and 5 HP) and two resolutions (draw 2 cards and gain 2 ACP).

'\' - This symbol is used between effect texts so the interpreter can tell between them. This symbol is necessary, even if an effect has no effect description text, along with the '|' logic character described below.
Here is an example of a Kyara with 3 effects:
Kyara "Test Dummy 1" M 400000 1 " eftext1 \eftext2 \eftext3 " [s hand sacrifice > summon hand |s field target 2 > destroy & gain_acp 5 |s field tap > damage 1 ]

'|' - A dividing character between two effects. Cards which have multiple effects use this character so the interpreter can tell between them.
Here is an example of a Kyara with 3 effects:
Kyara "Test Dummy 1" M 400000 1 " ef1 \ef2 \ef3 " [s hand sacrifice > summon hand |s field target 2 > destroy & gain_acp 5 |s field tap > damage 1 ]


There are several different types of effect costs and resolutions. Below is a comprehensive list of them, along with explanations:

's' - this letter goes at the beginning of every effect. It is currently just a placeholder letter which stands for 'special effect,' but in the future other effect types (such as 'r' - reaction and 'p' - passive) will exist.

'field','hand','discard' - Markers referring to the zone an effect can be activated in (the player's hand, field, and discard pile, respectively). If the card is not in the given zone, the effect cannot be activated.

EFFECT COSTS:
'tap' - Taps the Kyara. Kyaras are untapped at the beginning of the player's turn. (DOES NOT WORK FOR EVENT CARDS)

'pay_acp [value]' - Player must pay [value] ACP in order to activate the effect. Otherwise, effect activation fails.

'pay_hp [value]' - Player must pay [value] HP in order to activate this effect. Otherwise, effect activation fails.

'return_to_hand' - Player must return a card on their field to their hand. If no cards are on their field, activation fails.

'sacrifice' - Player must sacrifice a card they control (i.e. send it to their discard pile). If no cards are on their field, activation fails.

'target [value]' - Player must select [value] number of Kyaras on the opponent's side of the field. Adds the selected cards to the activated effect for resolution. If the opponent has fewer Kyaras than [value], activation fails.

'event' - a placeholder cost which sacrifices the card. Used to activate Event cards. 

EFFECT RESOLUTIONS:

'damage [value]' - Deals [value] damage to the opponent.

'heal [value]' - Opponent gains [value] HP.

'gain_acp [value]' - Player gains [value] ACP.

'gain_hp [value]' - Player gains [value] HP.

'lose_hp [value]' - Player loses [value] HP.

'draw [value]' - Player draws [value] cards from their deck. If [value] exceeds the size of the player's deck, all cards in the deck are added to the player's hand and any remaining draws are wasted.

'destroy' - Requires use of the 'target' effect cost. Destroys all Kyaras the opponent controls targeted in this way.

'summon [zone]' - Summons the card to the field. The given [zone] refers to where the card is being summoned from (e.g. 'summon hand' summons the card from the hand).

'print [string]' - Prints a message. Generally reserved for testing purposes, or to be funny.
Example usage (prints "STD prevented ;)" when tapped):
Kyara "Test Dummy 2" M 18 1 "Special Effect: 'The Clap ;)' - Prevent the next STD. Deal 2 damage. " [s field tap > damage 2 & print STD prevented ;) ]

As of 12/23/22, this list is exhaustive. HOWEVER, other effects and effect types are planned for the future. This README will be updated accordingly when these changes are made.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ENJOY THE GAME~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

