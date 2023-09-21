
""" 
Wordle game 

Sept 2023 

Alison and Danielle 

""" 

import pandas as pd 
import csv
import random 
import pygame 


#Setting up the display
clock = pygame.time.Clock()
screen_width=1000
screen_height=1000
background_color = (255, 255, 255) #white
box_color = (211, 211, 211) #light gray
border_width = 3
border_color = (0,0,0)
user_input_color = (135, 206, 235)
Letter_class_list = []

class Letter: 
    def __init__ (self, color, text, left_x, top_y): 
        self.color = color 
        self.text = text
        self.left_x = left_x
        self.top_y = top_y

# Functional component

# Part 1: Random five letter word (import online database)

df = pd.read_csv('https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt')

word_list = []
for each_word in df.iterrows():
    word_list.append(each_word[1][0])

word_answer = random.choice(word_list)
word_answer_char = list(word_answer) #putting the word into a list of individual char

# Part 2: Function (param: user's word guess)(returns a dictionary of what letters of the game board should change)

def every_input(user_word): 
    color_change_Dict = {green: [], gray: []}
    char_list = list(user_word) #putting the word into a list of individual char
    for i in range(len(char_list)): 
        for j in range(len(word_answer_char)): 
            if char_list[i] == word_answer_char[j]:
                if i == j: 
                    og_list = color_change_Dict[green]
                    color_change_Dict[green] = og_list.append(char_list[i])
                else: 
                    og_list = color_change_Dict[gray]
                    color_change_Dict[gray] = og_list.append(char_list[i])

    return color_change_Dict

# Game Display: 

pygame.init()

not_done = True

while not_done:

    display_screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("WORDLE")

    display_screen.fill(background_color)

    #set boxes for each letter: 
    for i in range(5): 
        for j in range(5): 
            letter_box = Letter(box_color, "", 50 + (j*100),50 + (i*100))
            Letter_class_list.append(letter_box)

            pygame.draw.rect(display_screen, box_color, (50 + (j*100), 50 + (i*100),100,100))
            pygame.draw.rect(display_screen, border_color, (50 + (j*100), 50 + (i*100),100,100), width = border_width)

    #creating a border 
    pygame.draw.rect(display_screen, border_color, (50, 453, 500, 10))

    #section for user input 
    for k in range(5): 
        pygame.draw.rect(display_screen, user_input_color, (50 + (j*100), 463 + (i*100),100,100))
        pygame.draw.rect(display_screen, border_color, (50 + (j*100), 463 + (i*100),100,100), width = border_width)

    pygame.display.update()
    clock.tick(60)

    
