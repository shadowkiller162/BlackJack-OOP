"""
Milestone Project 2 - Black Jack
# ## Game Play
# To play a hand of Blackjack the following steps must be followed:
# 1. Create a deck of 52 cards
# 2. Shuffle the deck
# 3. Ask the Player for their bet
# 4. Make sure that the Player's bet does not exceed their available chips
# 5. Deal two cards to the Dealer and two cards to the Player
# 6. Show only one of the Dealer's cards, the other remains hidden
# 7. Show both of the Player's cards
# 8. Ask the Player if they wish to Hit, and take another card
# 9. If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# 10. If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's
value meets or exceeds 17
# 11. Determine the winner and adjust the Player's chips accordingly
# 12. Ask the Player if they'd like to play again
"""

import random

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', \
'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, \
'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    """Carate card object with suit and ranks"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

class Deck:
    """Create Deck object to collect 52 Card object"""
    def __init__(self, suits, ranks):
        self.deck = []  # start with an empty list
        self.suits = suits
        self.ranks = ranks
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit, rank))
    def __repr__(self):
        return str([str(card) for card in self.deck])
    def shuffle(self):
        """shuffle Deck object"""
        random.shuffle(self.deck)
    def deal(self):
        """hit one card from deck"""
        return self.deck.pop(0)

class Hand:
    """Create difference role like player or dealer, they can keep Card object hit
    form Deck object"""
    def __init__(self, values):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        self.values = values
    def add_card(self, card):
        """add one card to hand"""
        self.cards.append(card)
        self.value += self.values[card.rank]
        if card.rank == "Ace":
            self.aces += 1
    def adjust_for_ace(self):
        """If value > 11, Ace will adjust to 1"""
        self.values["Ace"] = 1
        self.value = 0
        for card in self.cards:
            self.value += self.values[card.rank]

class Chips:
    """Create Chip object for any player and keep track they're bet and total money"""
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
    def win_bet(self):
        """player win the bet"""
        self.total += self.bet*2
    def lose_bet(self):
        """player lose the bet"""
        print("Sorry you lose")
    def __str__(self):
        return "Your account now have {}".format(self.total)

def take_bet(chip):
    """ask player how much money they want to bet"""
    while True:
        try:
            chip.bet = int(input("How much you want bet?:"))
        except ValueError:
            print("Please enter a number!")
            continue
        else:
            if chip.bet > account.total:
                print("More than your account, you'r account now have {}".format(str(account.total)))
                continue
            else:
                account.total -= chip.bet
                break

def hit(deck, hand):
    """hit card from deck"""
    card = deck.deal()
    hand.add_card(card)
    if hand.value > 11 and hand.values["Ace"] == 11:
        hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    """ask player if they want more game"""
    global PLAYING  # to control an upcoming while loop

    if input("Would you want to hit? yes/no").lower().startswith('y'):
        hit(deck, hand)
    else:
        PLAYING = False

def show_some(player, dealer):
    """Hide dealer's first card"""
    print(dealer.cards[0])
    print("========================================")
    for card in player.cards:
        print(card, end="  ")
    print("total: {}".format(str(player.value)))
    print("\n\n")

def show_all(player, dealer):
    """show all player and dealer cards"""
    for card in dealer.cards:
        print(card, end="  ")
    print("total: {}".format(str(dealer.value)))
    print("========================================")
    for card in player.cards:
        print(card, end="  ")
    print("total: {}".format(str(player.value)))
    print("\n\n")

def player_busts(chip):
    """call when player bust"""
    chip.lose_bet()
    print("you bust!")

def player_wins(chip):
    """call when player win"""
    chip.win_bet()
    print("you win!")

def dealer_busts(chip):
    """call when dealer bust"""
    chip.win_bet()
    print("dealer bust!")

def dealer_wins(chip):
    """call when dealer win"""
    chip.lose_bet()
    print("you lose!")

def push(chip):
    """call when player card value equal to dealer"""
    chip.lose_bet()
    print("push! dealer win!")

PLAYING = True
account = Chips()

while True:
    # Print an opening statement
    print("Welcome to my black jack game.")

    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck(SUITS, RANKS)
    new_deck.shuffle()
    new_player = Hand(VALUES)
    new_dealer = Hand(VALUES)

    for i in range(0, 2):
        hit(new_deck, new_player)
        hit(new_deck, new_dealer)

    # Prompt the Player for their bet
    take_bet(account)

    # Show cards (but keep one dealer card hidden)
    show_some(new_player, new_dealer)

    while PLAYING:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(new_deck, new_player)

        # Show cards (but keep one dealer card hidden)
        show_some(new_player, new_dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if new_player.value > 21:
            player_busts(account)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while new_player.value <= 21 and new_dealer.value < 17:
        hit(new_deck, new_dealer)

    # Show all cards
    show_all(new_player, new_dealer)

    # Run different winning scenarios
    if new_dealer.value > 21:
        dealer_busts(account)
    elif new_dealer.value == new_player.value:
        dealer_wins(account)
    elif new_dealer.value > new_player.value:
        dealer_wins(account)
    elif new_dealer.value < new_player.value and new_player.value <= 21:
        player_wins(account)

    # Inform Player of their chips total
    print(account)

    # Ask to play again
    if input("Would you want play again? yes/no").lower().startswith("y"):
        PLAYING = True
        continue
    else:
        print("Thank you for play!")
        break
