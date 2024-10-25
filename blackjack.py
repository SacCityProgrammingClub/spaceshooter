import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
CARD_WIDTH = 100
CARD_HEIGHT = 145
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 50

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Blackjack')

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.name = f"{value} of {suit}"
        # Calculate card's numerical value
        if value in ['Jack', 'Queen', 'King']:
            self.numeric_value = 10
        elif value == 'Ace':
            self.numeric_value = 11
        else:
            self.numeric_value = int(value)

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player_cards = []
        self.dealer_cards = []
        self.player_score = 0
        self.dealer_score = 0
        self.player_chips = 1000
        self.current_bet = 0
        self.game_state = "betting"  # betting, playing, dealer_turn, game_over
        
        # Create buttons
        self.hit_button = Button(50, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Hit", WHITE)
        self.stand_button = Button(230, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Stand", WHITE)
        self.bet_button = Button(410, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Bet 50", WHITE)
        self.play_again_button = Button(590, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Play Again", WHITE)
        
        self.font = pygame.font.Font(None, 36)

    def deal_initial_cards(self):
        self.player_cards = [self.deck.draw(), self.deck.draw()]
        self.dealer_cards = [self.deck.draw(), self.deck.draw()]
        self.calculate_scores()

    def calculate_scores(self):
        self.player_score = self.calculate_hand(self.player_cards)
        self.dealer_score = self.calculate_hand(self.dealer_cards)

    def calculate_hand(self, cards):
        score = 0
        aces = 0
        
        for card in cards:
            if card.value == 'Ace':
                aces += 1
            else:
                score += card.numeric_value
        
        # Add aces
        for _ in range(aces):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
                
        return score

    def hit(self):
        self.player_cards.append(self.deck.draw())
        self.calculate_scores()
        if self.player_score > 21:
            self.game_state = "game_over"

    def dealer_play(self):
        while self.dealer_score < 17:
            self.dealer_cards.append(self.deck.draw())
            self.calculate_scores()
        self.game_state = "game_over"

    def place_bet(self, amount):
        if self.player_chips >= amount:
            self.current_bet = amount
            self.player_chips -= amount
            self.game_state = "playing"
            self.deal_initial_cards()

    def determine_winner(self):
        if self.player_score > 21:
            return "Dealer wins! Player busted!"
        elif self.dealer_score > 21:
            self.player_chips += self.current_bet * 2
            return "Player wins! Dealer busted!"
        elif self.player_score > self.dealer_score:
            self.player_chips += self.current_bet * 2
            return "Player wins!"
        elif self.dealer_score > self.player_score:
            return "Dealer wins!"
        else:
            self.player_chips += self.current_bet
            return "Push! It's a tie!"

    def draw_card(self, surface, card, x, y, face_up=True):
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(surface, WHITE, card_rect)
        pygame.draw.rect(surface, BLACK, card_rect, 2)
        
        if face_up:
            # Draw card value and suit
            text = self.font.render(f"{card.value}", True, BLACK)
            suit_text = self.font.render(f"{card.suit[0]}", True, RED if card.suit in ['Hearts', 'Diamonds'] else BLACK)
            
            surface.blit(text, (x + 10, y + 10))
            surface.blit(suit_text, (x + 10, y + 30))

        else:
            # Draw card back
            pygame.draw.rect(surface, RED, card_rect.inflate(-10, -10))

    def draw(self, surface):
        # Clear screen
        surface.fill(GREEN)
        
        # Draw dealer's cards
        for i, card in enumerate(self.dealer_cards):
            face_up = True if i == 0 or self.game_state in ["dealer_turn", "game_over"] else False
            self.draw_card(surface, card, 50 + i * 110, 50, face_up)

        # Draw player's cards
        for i, card in enumerate(self.player_cards):
            self.draw_card(surface, card, 50 + i * 110, 300)

        # Draw scores and chips
        dealer_text = self.font.render(f"Dealer: {self.dealer_score if self.game_state in ['dealer_turn', 'game_over'] else '?'}", True, WHITE)
        player_text = self.font.render(f"Player: {self.player_score}", True, WHITE)
        chips_text = self.font.render(f"Chips: ${self.player_chips}", True, WHITE)
        bet_text = self.font.render(f"Current Bet: ${self.current_bet}", True, WHITE)
        
        surface.blit(dealer_text, (800, 50))
        surface.blit(player_text, (800, 300))
        surface.blit(chips_text, (800, 400))
        surface.blit(bet_text, (800, 450))

        # Draw buttons based on game state
        if self.game_state == "betting":
            self.bet_button.draw(surface)
        elif self.game_state == "playing":
            self.hit_button.draw(surface)
            self.stand_button.draw(surface)
        elif self.game_state == "game_over":
            result_text = self.font.render(self.determine_winner(), True, WHITE)
            surface.blit(result_text, (400, 500))
            self.play_again_button.draw(surface)

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if game.game_state == "betting" and game.bet_button.rect.collidepoint(mouse_pos):
                    game.place_bet(50)
                elif game.game_state == "playing":
                    if game.hit_button.rect.collidepoint(mouse_pos):
                        game.hit()
                    elif game.stand_button.rect.collidepoint(mouse_pos):
                        game.game_state = "dealer_turn"
                        game.dealer_play()
                elif game.game_state == "game_over" and game.play_again_button.rect.collidepoint(mouse_pos):
                    game = Game()  # Reset the game

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()