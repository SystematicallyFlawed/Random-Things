import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from PIL import Image, ImageDraw
import os

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}


# Function to create a deck of cards
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [f'{value} of {suit}' for value in CARD_VALUES.keys() for suit in suits]
    random.shuffle(deck)
    return deck


# Function to create card images
def create_card_image(value, suit):
    img = Image.new("RGB", (100, 140), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (100, 140)], outline="black", width=2)
    draw.text((10, 10), value, fill="black")
    draw.text((10, 120), value, fill="black")
    draw.text((80, 10), suit[0], fill="black")  # Displaying the suit abbreviation
    draw.text((80, 120), suit[0], fill="black")  # Displaying the suit abbreviation
    return img


# Create an images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Create card images and save them
card_images = {}
for value in CARD_VALUES.keys():
    for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
        img = create_card_image(value, suit)
        card_images[f'{value} of {suit}'] = img
        img.save(f'images/{value.replace(" ", "_")}_of_{suit.replace(" ", "_")}.png')


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")

        self.deck = create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_money = 100  # Starting money
        self.current_bet = 0
        self.loan_amount = 0
        self.interest_rate = 0.1  # 10% interest rate

        # Setup UI
        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        self.player_label = tk.Label(self.root, text="Player's hand:", font=("Arial", 16))
        self.player_label.pack()

        self.dealer_label = tk.Label(self.root, text="Dealer's hand:", font=("Arial", 16))
        self.dealer_label.pack()

        self.money_label = tk.Label(self.root, text=f"Total Money: ${self.player_money}", font=("Arial", 16))
        self.money_label.pack()

        self.loan_label = tk.Label(self.root, text=f"Loan: ${self.loan_amount}", font=("Arial", 16))
        self.loan_label.pack()

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit)
        self.hit_button.pack()

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand)
        self.stand_button.pack()

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack()

        self.pay_loan_button = tk.Button(self.root, text="Pay Loan", command=self.pay_loan)
        self.pay_loan_button.pack()

    def start_new_game(self):
        # Ask for the player's bet
        bet = simpledialog.askinteger("Place Your Bet", "Enter your bet:", minvalue=1)

        # Automatically take out a loan if the player runs out of money
        if bet is None:
            return  # Player canceled the bet input

        # If player has no money, they can still place a bet
        if bet > self.player_money:
            loan_needed = bet - self.player_money
            self.loan_amount += loan_needed
            self.player_money += loan_needed  # Add loan to player's money
            messagebox.showinfo("Loan Taken", f"You have taken a loan of ${loan_needed} to cover your bet.")

        self.current_bet = bet
        self.player_money -= self.current_bet  # Deduct the bet from the player's money

        self.deck = create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.update_ui()

    def calculate_score(self, hand):
        score = sum(CARD_VALUES[card.split()[0]] for card in hand)
        aces = hand.count('A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def update_ui(self):
        player_cards = ', '.join(self.player_hand)
        dealer_cards = ', '.join(self.dealer_hand[:1]) + ', Hidden'

        self.player_label.config(
            text=f"Player's hand: {player_cards} (Score: {self.calculate_score(self.player_hand)})")
        self.dealer_label.config(text=f"Dealer's hand: {dealer_cards}")
        self.money_label.config(text=f"Total Money: ${self.player_money}")
        self.loan_label.config(text=f"Loan: ${self.loan_amount}")

    def hit(self):
        self.player_hand.append(self.deck.pop())
        player_score = self.calculate_score(self.player_hand)
        if player_score > 21:
            self.update_ui()
            messagebox.showinfo("Game Over", "You bust! Dealer wins.")
            self.restart()  # Restart the game after bust
        else:
            self.update_ui()

    def stand(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self.end_game()

    def end_game(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        self.update_ui()

        if dealer_score > 21 or player_score > dealer_score:
            winnings = self.current_bet * 2  # Win bet (get back your bet plus winnings)
            self.player_money += winnings
            messagebox.showinfo("Game Over", f"You win! You gained ${winnings}.")
        elif player_score < dealer_score:
            messagebox.showinfo("Game Over", "Dealer wins!")
        else:
            self.player_money += self.current_bet  # Return the bet on a tie
            messagebox.showinfo("Game Over", "It's a tie!")

        self.restart()

    def pay_loan(self):
        if self.loan_amount <= 0:
            messagebox.showinfo("No Loan", "You have no outstanding loans.")
            return

        payment = simpledialog.askinteger("Pay Loan", "Enter the amount to pay off your loan:", minvalue=1)
        if payment is None:
            return  # Player canceled the payment input

        if payment > self.player_money:
            messagebox.showinfo("Insufficient Funds", "You can't pay more than you have.")
            return

        self.loan_amount -= payment
        self.player_money -= payment
        messagebox.showinfo("Loan Payment", f"You paid off ${payment} of your loan.")

        # If loan is fully paid off
        if self.loan_amount <= 0:
            messagebox.showinfo("Loan Paid Off", "Congratulations! You have paid off your loan.")

        self.update_ui()

    def restart(self):
        self.start_new_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()