import pygame
import random
import os

# dimensiones
WIDTH, HEIGHT = 500, 700

# Colores
BACKGROUND = (18, 18, 19)
BORDERS = (58, 58, 60)
TEXT_COLOR = (215, 218, 220)
GRAY = (120, 124, 126)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)

'''basicamente, sta funcion permite que el juego cargue una lista de palabras
 desde el archivo de palabras'''
def load_words(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().upper() for line in file if len(line.strip()) == 5]

# variables del juego
WORDS = load_words("palabrasx 1747.txt")
SECRET_WORD = random.choice(WORDS)
ATTEMPTS = []
CURRENT_LETTERS = ""
MAX_ATTEMPTS = 6
GAME_OVER = False
WON = False
invalid_word_timer = 0