# SHOPRO
Repository of my code on a Python version of a card game I made with my friends.

As of 12/8/2022, this code is very poorly documented. 
In the future I plan to better organize/add tags to my code so the average nerd can understand it.
But for now it remains as a block of text to just download and try out.

~~~~~~~~~~~~~~INSTRUCTIONS FOR MAKING NEW CARDS~~~~~~~~~~~~~~
The file "cards.txt" contains all the cards the game will use. Anyone can easily add cards to the game by editing this file.
Each card is a collection of text and logic on one line.
Structure of a card line:

Kyara cards: (similar card type to e.g. monster cards in Yu-Gi-Oh or creature cards in Magic)
Kyara "Name" [gender/sex (or whatever)] [age] [cost] "Effect text \ Effect text" [effect logic | effect logic ]

Example Kyara card:
Kyara "Test Dummy 3" F 17 1 "Special Effect: 'TMT' - Lose 3 HP and gain 3 ACP" [s field tap > lose_hp 3 & gain_acp 3 ]

Cards can have as many effects on them as you want, even 0 if you would like. 
HOWEVER, each effect MUST have a corresponding effect text (texts separated by the \ symbol).
Even a blank space is fine, as long as there is at least one \ to show where the text would be. 
Otherwise that effect WILL NOT BE PROCESSED.

I will further update this README with better specifics on effect creation/usage, game rules, and so forth. However, I have a Japanese quiz in 20 minutes
and class is 15 minutes away from my apartment. 

~~~~~~~~~~~~~~GAME RULES~~~~~~~~~~~~~~
Just a placeholder for now. I'll be back... some day... (or just after finals.)
