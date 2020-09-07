import math
import random
import tkinter.messagebox as messagebox
from tkinter import *
import pygame
import pygame.mixer as mixer

import words

root = Tk()
root.withdraw()
pygame.init()
mixer.music.load("assets/music.mp3")
mixer.music.play(-1)
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
helped = True
pygame.display.set_caption("Hangman: Tough Luck!")
# Stuff about the hanger
hanger_status = 0
hanger_images = [
    pygame.image.load("assets/hangman0.png"),
    pygame.image.load("assets/hangman1.png"),
    pygame.image.load("assets/hangman2.png"),
    pygame.image.load("assets/hangman3.png"),
    pygame.image.load("assets/hangman4.png"),
    pygame.image.load("assets/hangman5.png"),
    pygame.image.load("assets/hangman6.png")
]

win_phrases = ["Nice Job!", "Cool Win!", "Hard Work Pays Off!", "You Win!", "There's More Waiting..."]
lose_phrases = ["GAME OVER", "Try Again Later...", "Tough Luck!", "Nice Try!"]
fps = 60

fps_clock = pygame.time.Clock()
# Button
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
letter_font = pygame.font.Font("freesansbold.ttf", 30)
word_font = pygame.font.Font("freesansbold.ttf", 60)
title_font = pygame.font.Font("assets/SnowtopCaps.otf", 70)
A = 65
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

word = random.choice(words.words)
guessed = []


def give_answer():
    screen.fill((255, 255, 255))
    help_font = pygame.font.Font("assets/SnowtopCaps.otf", 60)
    help_text = help_font.render(f"The Word Is {word}!", 1, (0, 0, 255))
    screen.blit(help_text, (WIDTH / 2 - help_text.get_width() / 2, HEIGHT / 2 - help_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def display_message(message):
    pygame.time.delay(1000)
    screen.fill((255, 255, 255))
    lose_text = word_font.render(message, 1, (0, 0, 0))
    screen.blit(lose_text, (WIDTH / 2 - lose_text.get_width() / 2, HEIGHT / 2 - lose_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def draw():
    screen.fill((255, 255, 255))
    title = title_font.render("HANGMAN: TOUGH LUCK!", True, (255, 0, 0))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 20))

    display_word = ""
    for alphabet in word:
        if alphabet in guessed:
            display_word += alphabet + " "
        else:
            display_word += "_ "
        txt = word_font.render(display_word, True, (0, 0, 0))
        screen.blit(txt, (400, 200))

    for alphabet in letters:
        xcor, ycor, letter_alphabet, visible = alphabet
        if visible:
            pygame.draw.circle(screen, (0, 0, 0), (xcor, ycor), RADIUS, 3)
            letr = letter_font.render(letter_alphabet, 1, (0, 0, 0))
            screen.blit(letr, (xcor - letr.get_width() / 2, ycor - letr.get_height() / 2))
    screen.blit(hanger_images[hanger_status], (150, 100))
    pygame.display.update()


while True:
    fps_clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                helped = False
                give_answer()
                exit()
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x_cor, y_cor, ltr, visibility = letter
                if visibility:
                    distance = math.sqrt((x_cor - m_x) ** 2 + (y_cor - m_y) ** 2)
                    if distance < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hanger_status += 1

    draw()
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    if won:
        display_message(random.choice(win_phrases))
        break
    if hanger_status == 6:
        display_message(random.choice(lose_phrases))
        break

    pygame.display.update()

if hanger_status == 6:
    messagebox.askyesno("Hey!", 'Did you like "Hangman?"')
    messagebox.showinfo("Thanks!", "Thanks for your opinion!")
if won:
    messagebox.askyesno("Hey!", 'Did you like "Hangman?"')
    messagebox.showinfo("Thanks!", "Thanks for your opinion!")

pygame.quit()
