# Blackjack Game
# 1 human player and 1 computer dealer

#### Win Conditions ####
# Dealer wins when it has more value than player, if player gets more than 21
# Player wins when they have more than dealer or 21 exactly
########################

import random

# Global variables create standard-52 card deck
# Face cards are worth 10, Ace can be 1 or 11
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace': 11}
playing = True  # False = game ends

# Creates each card their suit, rank, and value from their rank
class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

# Creates the standard-52 card deck
# Holds Cards as a list with random library to shuffle() 
# Cards dealt are pop() out of deck
class Deck():
    def __init__(self):
        self.deck = []     # Holds all cards

        # Appends all ranks of all suits to list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)     # Creates card of the suit and rank
                self.deck.append(created_card)

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    # Shuffles deck
    def shuffle(self):
        random.shuffle(self.deck)

    # Deals 1 card
    def deal(self):
        return self.deck.pop()

# Hand class to hold values of cards
class Hand():
    def __init__(self):
        self.cards = []           # Start with empty list
        self.value = 0            # Start with 0 value
        self.aces = 0             # Add attribute to track Ace cards

    def add_card(self, card):
        self.cards.append(card)             # from Deck.deal() ---> single Card(suit, rank)
        self.value += values[card.rank]     # Adds value of card

        # Tracks Ace cards
        if card.rank =="Ace":
            self.aces += 1

    # Changes Ace value
    def adjust_for_ace(self):
        # If total value > 21 and there are still Aces
        # Then change Ace to be 1 instead of 11
        while self.value > 21 and self.aces:
            self.value -= 10        # Changes Ace to be 1, otherwise stays at 11
            self.aces -= 1          # Removes 1 Ace card

# Player's starting, bets, and ongoing winnings
class Chips():
    def __init__(self):
        self.total = 100        # Change to change default amount of chips
        self.bet = 0

    # Increases total by bet
    def win_bet(self):
        self.total += self.bet

    # Decreases total by bet
    def lost_bet(self):
        self.total -= self.bet

# Takes player's bet
def take_bet(chips):
    while True:
        try:
            # Player inputs how much chips to bet
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:  # Error only triggers when letter is inputted instead of integer
            print("ERROR, Provide an integer")
        else:
            # Error message if bet is higher than player's total chips
            if chips.bet > chips.total:
                print("ERROR, You do not have enough Chips, You have: {}".format(chips.total))
            else:
                break

# Asks player if they want to hit or dealer's hand is less than 17
def hit(deck, hand):
    card = deck.deal()          # Takes card from deck
    hand.add_card(card)         # Adds card to hand
    hand.adjust_for_ace()       # Checks if the card is an Ace

# Takes hit() and adds cards if the player hits or stands and adjusts the Hand() accordingly
def hit_or_stand(deck, hand):
    global playing             # Controls while loop

    while True:
        x = input("Hit or Stand? Enter H or S ")

        # Adds another card to Player's hand
        if x[0].upper() == 'H':
            hit(deck, hand)

        # Moves to Dealer's turn                                 
        elif x[0].upper() == 'S':
            print("Player Stands\nDealer's Turn")           
            playing = False
        else:
            print("ERROR, Invalid Input, Enter H or S only ")
            continue
        break

# Shows all Player cards (2), Dealer shows a card (1)
def show_some(player, dealer):

    # Shows only 1 of dealer's card
    print("\nDealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])     

    # Shows all (2) of player's hand
    print("\nPlayer's hand: ")
    for card in player.cards:
        print(card)

# Shows all cards and calculates / displays values
def show_all(player, dealer):

    # Shows all (2) of dealer's hand
    print("\nDealer's hand: ")
    for card in dealer.cards:
        print(card)

    # Calculates and displays value
    print(f"Value of Dealer's hand is: {dealer.value}")

    # Shows all (2) of player's hand
    print("\nPlayer's hand: ")
    for card in player.cards:
        print(card)

    # Calculates and displays value
    print(f"Value of Player's hand is: {player.value}")

# Handles endgame scenarios, who wins and loses
def player_busts(player, dealer, chips):
    print("PLAYER BUSTS!")
    chips.lost_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("DEALER BUSTS!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("DEALERS WINS! PLAYER LOSES!")
    chips.lost_bet()

# Both Dealer and Player have 21, tie
def push(player, dealer):
    print("Dealer and Player tie! PUSH")

# Sets up game
while True:
    # Print an opening statement
    print("BLACKJACK, GET AS CLOSE TO 21 WITHOUT GOING OVER")

    # Create & shuffle the deck, deal two cards to Player and Dealer
    play_deck = Deck()
    play_deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(play_deck.deal())
    player_hand.add_card(play_deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(play_deck.deal())
    dealer_hand.add_card(play_deck.deal())
        
    # Sets up the Player's chips
    player_chips = Chips()
    
    # Player makes their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(play_deck, player_hand)
        
        # Show some cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)    # Player loses
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(play_deck, dealer_hand)
    
        # Show all cards in both player and dealer hands
        show_all(player_hand, dealer_hand)

        # Checks different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)    # Dealer loses
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)     # Dealer Wins
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)     # Player Wins
        else:
            push(player_hand, dealer_hand)                          # Tie
    
    # Prints Player's total chips
    print("\nPlayer's winnings stand at ", player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'Y' or 'N' ")

    if new_game[0].upper() =='Y':
        playing = True
        continue
    else:
        print("Thanks for playing!\nClosing Game...")
        break