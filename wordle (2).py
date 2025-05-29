import pygame
import sys

# aqui traemos todas las variables y colores que tenemos guardados en el archivo 
from config import *  

pygame.init()  

# estas son las fuentes que vamos a usar para dibujar letras en pantalla.
# FONT es para las letras grandes (como las del tablero, y no la pude enviar al otro archivo xd)
# MESSAGE_FONT es para los mensajes que aparecen cuando ganamos o perdemos
FONT = pygame.font.SysFont("Arial", 48, bold=True)
MESSAGE_FONT = pygame.font.SysFont("Arial", 20, bold=True)

# creamos la ventana del juego con el tamaño que dijimos en config.py (esta variable no puede colocarse en otro archivo)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORDLE EXAMEN")  # Título de la ventana

# esta función se encarga de dibujar el tablero en la pantalla
def draw_board():
    SCREEN.fill(BACKGROUND)  # pintamos el fondo del color que pusimos en BACKGROUND

    # calculamos cuánto mover a la derecha el tablero para que quede centrado
    offset_x = (WIDTH - (5 * 70 + 4 * 10)) // 2
    offset_y = 50  # dejamos un espacio arriba del tablero

    # recorremos los intentos que el jugador ya ha hecho
    for row, attempt in enumerate(ATTEMPTS):
        for col, letter in enumerate(attempt):
            color = GRAY  # por defecto todo es gris
            # si la letra está en la posicion correcta, la pintamos verde
            if letter == SECRET_WORD[col]:
                color = GREEN
            # si la letra está pero en otra posicion, la pintamos amarilla
            elif letter in SECRET_WORD:
                color = YELLOW

            # calculamos la posicion del cuadro donde va la letra
            x = offset_x + col * 80
            y = offset_y + row * 80

            # dibujamos el recuadro de la letra
            pygame.draw.rect(SCREEN, color, (x, y, 70, 70), border_radius=8)

            # dibujamos la letra en el centro del recuadro
            text = FONT.render(letter, True, WHITE)
            SCREEN.blit(text, (x + 35 - text.get_width() // 2, y + 35 - text.get_height() // 2))

    # si el juego no ha terminado, dibujamos la fila donde el jugador esta escribiendo
    if not GAME_OVER:
        row = len(ATTEMPTS)  # Nos dice en qué fila estamos escribiendo
        for i in range(5):  # Son 5 letras
            x = offset_x + i * 80
            y = offset_y + row * 80
            # dibujamos el recuadro vacío
            pygame.draw.rect(SCREEN, BORDERS, (x, y, 70, 70), 2, border_radius=8)

            # si ya se ha escrito una letra en esa posicion, la mostramos
            if i < len(CURRENT_LETTERS):
                letter = CURRENT_LETTERS[i]
                text = FONT.render(letter, True, TEXT_COLOR)
                SCREEN.blit(text, (x + 35 - text.get_width() // 2, y + 35 - text.get_height() // 2))

# esta funcion solo sirve para mostrar un mensaje al final (cuando ganas o pierdes)
def display_message(text):
    surface = MESSAGE_FONT.render(text, True, WHITE)  # Creamos el texto
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT - 40))  # Lo centramos abajo
    SCREEN.blit(surface, rect)  # Lo mostramos en la pantalla

# creamos un reloj para controlar los FPS (cuántas veces se actualiza por segundo)
clock = pygame.time.Clock()

# este es el bucle principal del juego, aquí pasa todo
while True:
    for event in pygame.event.get():  # revisamos cada evento (tecla, cerrar ventana, etc.)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # si cerramos la ventana, salimos del juego

        # si se presiona una tecla y todavía no se ha acabado el juego
        if event.type == pygame.KEYDOWN and not GAME_OVER:
            if event.key == pygame.K_RETURN:  # si se presiona Enter
                if len(CURRENT_LETTERS) == 5:  # solo se puede enviar si hay 5 letras
                    if CURRENT_LETTERS not in WORDS:
                        invalid_word_timer = 120  # mostrará el mensaje por 2 segundos (a 60 FPS)
                        continue  # la palabra no es válida

                ATTEMPTS.append(CURRENT_LETTERS)  # guardamos el intento

                # si adivinamos la palabra, ganamos
                if CURRENT_LETTERS == SECRET_WORD:
                        WON = True
                        GAME_OVER = True
                # si ya hicimos el número máximo de intentos, perdemos
                elif len(ATTEMPTS) >= MAX_ATTEMPTS:
                        GAME_OVER = True

                CURRENT_LETTERS = ""  # reiniciamos la fila actual

            elif event.key == pygame.K_BACKSPACE:
                # si presionamos borrar, quitamos la última letra
                CURRENT_LETTERS = CURRENT_LETTERS[:-1]

            elif event.unicode.isalpha() and len(CURRENT_LETTERS) < 5:
                # si presionamos una letra (y no hemos escrito 5), la agregamos
                CURRENT_LETTERS += event.unicode.upper()

    draw_board()  # dibujamos todo el tablero

     # si la palabra no está registrada, mostramos el mensaje
    if invalid_word_timer > 0:
        warning = MESSAGE_FONT.render("Esta palabra no está registrada", True, (RED))
        warning_rect = warning.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        SCREEN.blit(warning, warning_rect)
        invalid_word_timer -= 1

    if GAME_OVER:
        if WON:
            display_message("You won!")  # si ganamos, mostramos mensaje
        else:
            display_message(f"The word was: {SECRET_WORD}")  # si perdimos, mostramos la palabra correcta

    pygame.display.flip()  # actualiza la pantalla
    clock.tick(60)  # el juego va a 60 FPS

'''aun hay muchas cosas en las cuales trabajar. es el codigo principal que uso toñito, 
solamente que se ve visualmente un poquito diferente y tambien la mayoria de variables, 
constantes, funciones recuerden que deben ir en ingles, por eso se ve de esta manera
'''

'''movi la funcion que es practicamente la que da y carga las palabras al archivo de config.py'''