import pygame
import sys
from config import *

pygame.init()

FONT = pygame.font.SysFont("Brux font", 48, bold=True) #Brux font
MESSAGE_FONT = pygame.font.SysFont("Arial", 20, bold=True)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORDLE EXAMEN")

def show_start_screen():
    while True:
        SCREEN.fill(BACKGROUND)
        title_letters = ["W", "O", "R", "D", "L", "E"]
        colors = [(147, 128, 181), (223, 98, 98), (218, 199, 94), (133, 206, 127), (122, 136, 218), (225, 163, 101)]
        offset_x = (WIDTH - (6 * 70 + 5 * 10)) // 2
        offset_y = HEIGHT // 2 - 100

        for i, letter in enumerate(title_letters):
            x = offset_x + i * 80
            pygame.draw.rect(SCREEN, colors[i], (x, offset_y, 70, 70), border_radius=8)
            text = FONT.render(letter, True, WHITE)
            SCREEN.blit(text, (x + 35 - text.get_width() // 2, offset_y + 35 - text.get_height() // 2))

        play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
        pygame.draw.rect(SCREEN, GREEN, play_button, border_radius=10)
        button_text = MESSAGE_FONT.render("START", True, BLACK)

        SCREEN.blit(button_text, (play_button.centerx - button_text.get_width() // 2,
                                  play_button.centery - button_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return

def draw_board():
    SCREEN.fill(BACKGROUND)
    offset_x = (WIDTH - (5 * 70 + 4 * 10)) // 2
    offset_y = 50

    for row, attempt in enumerate(ATTEMPTS):
        for col, letter in enumerate(attempt):
            color = GRAY
            if letter == SECRET_WORD[col]:
                color = GREEN
            elif letter in SECRET_WORD:
                color = YELLOW

            x = offset_x + col * 80
            y = offset_y + row * 80
            pygame.draw.rect(SCREEN, color, (x, y, 70, 70), border_radius=8)
            text = FONT.render(letter, True, WHITE)
            SCREEN.blit(text, (x + 35 - text.get_width() // 2, y + 35 - text.get_height() // 2))

    if not GAME_OVER:
        row = len(ATTEMPTS)
        for i in range(5):
            x = offset_x + i * 80
            y = offset_y + row * 80
            pygame.draw.rect(SCREEN, BORDERS, (x, y, 70, 70), 2, border_radius=8)
            if i < len(CURRENT_LETTERS):
                letter = CURRENT_LETTERS[i]
                text = FONT.render(letter, True, TEXT_COLOR)
                SCREEN.blit(text, (x + 35 - text.get_width() // 2, y + 35 - text.get_height() // 2))

def display_message(text):
    surface = MESSAGE_FONT.render(text, True, WHITE)
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    SCREEN.blit(surface, rect)

def add_word(word):
    if word not in WORDS:
        with open("palabrasx 1747.txt", 'a') as file:
            file.write(word + '\n')
        WORDS.append(word)

clock = pygame.time.Clock()
show_start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not GAME_OVER:
            if event.key == pygame.K_RETURN:
                if len(CURRENT_LETTERS) == 5:
                    if CURRENT_LETTERS not in WORDS:
                        invalid_word_timer = 120
                        add_word(CURRENT_LETTERS)
                        continue
                    ATTEMPTS.append(CURRENT_LETTERS)
                    if CURRENT_LETTERS == SECRET_WORD:
                        WON = True
                        GAME_OVER = True
                    elif len(ATTEMPTS) >= MAX_ATTEMPTS:
                        GAME_OVER = True
                    CURRENT_LETTERS = ""
            elif event.key == pygame.K_BACKSPACE:
                CURRENT_LETTERS = CURRENT_LETTERS[:-1]
            elif event.unicode.isalpha() and len(CURRENT_LETTERS) < 5:
                CURRENT_LETTERS += event.unicode.upper()

    draw_board()

    if invalid_word_timer > 0:
        warning = MESSAGE_FONT.render("Esta palabra no está registrada", True, RED)
        warning_rect = warning.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        SCREEN.blit(warning, warning_rect)
        invalid_word_timer -= 1

    if GAME_OVER:
        if WON:
            display_message("You won!")
        else:
            display_message(f"The word was: {SECRET_WORD}")

    pygame.display.flip()
    clock.tick(60)

