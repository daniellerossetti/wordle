
""" 
Wordle game 

Sept 2023 

Alison and Danielle 

""" 

import pandas as pd 
import csv
import random 
import pygame, sys
from pygame.locals import*

#Setting up the display
clock = pygame.time.Clock()
screen_width=1000
screen_height=1000
background_color = (255, 255, 255) #white
box_color = (211, 211, 211) #light gray
yellow = (255, 191, 0)
green = (60, 179, 113)
dark_gray = (105,105,105)
border_width = 3
border_color = (0,0,0)
user_input_color = (135, 206, 235) #light blue
button_color = (34,139,34) #green 

class Letter: 
    def __init__ (self, color, text, left_x, top_y): 
        self.color = color 
        self.text = text
        self.left_x = left_x
        self.top_y = top_y

    def addText(self, text):
        font.render(self.text, True, (0,0,0)), (self.left_x + 25, self.top_y + 25)

# Functional component

# Part 1: Random five letter word (import online database)

df = pd.read_csv('https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt')

word_list = []
for each_word in df.iterrows():
    word_list.append(each_word[1][0])

word_answer = random.choice(word_list)
print("The answer to this wordle is: ", word_answer)
word_answer_char = list(word_answer) #putting the word into a list of individual char

# Part 2: Function (param: user's word guess)(returns a dictionary of what letters of the game board should change)

def every_input(user_word): 
    color_change_Dict = {"green": [], "yellow": []}
    og_list = []
    char_list = list(user_word) #putting the word into a list of individual char
    for i in range(len(char_list)): 
        for j in range(len(word_answer_char)): 
            if char_list[i] == word_answer_char[j]:
                if i == j: 
                    print("Char: ", char_list[i])
                    color_change_Dict["green"].append(char_list[i])
                    print("APPEND: ", color_change_Dict["green"])

                else: 
                    og_list = color_change_Dict["yellow"]
                    color_change_Dict["yellow"].append(char_list[i])

    return color_change_Dict

#Update game display function: 


# Game Display: 
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 25)
text = font.render('ENTER', True, (0,0,0))
textRect = text.get_rect()
textRect.center = (300, 737.5)
display_screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("WORDLE")
Letter_class_list = []
Letter_class_list_input = []

display_screen.fill(background_color)

#set boxes for each letter: 
for i in range(5): 
    for j in range(5): 
        letter_box = Letter(box_color, "", 50 + (j*100),50 + (i*100))
        Letter_class_list.append(letter_box)

        pygame.draw.rect(display_screen, box_color, (50 + (j*100), 50 + (i*100),100,100))
        pygame.draw.rect(display_screen, border_color, (50 + (j*100), 50 + (i*100),100,100), width = border_width)

#creating a border 
pygame.draw.rect(display_screen, border_color, (50, 550, 500, 10))

#section for user input 
for k in range(5): 
    letter_box = Letter(box_color, "", 50 + (k*100), 560)
    Letter_class_list_input.append(letter_box)
    
    pygame.draw.rect(display_screen, user_input_color, (50 + (k*100), 560,100,100))
    pygame.draw.rect(display_screen, border_color, (50 + (k*100), 560,100,100), width = border_width)

#ENTER button
enter_button = pygame.draw.rect(display_screen, button_color, (200, 700,200,75))
pygame.draw.rect(display_screen, button_color, (200, 700,200,75), width = border_width)

display_screen.blit(text, textRect)

enter_button_rect = pygame.Rect(200, 700,200,75)

#For every round 
user_text = ""
user_answer = ""  

not_done = True
enter_button_active = False
letter1_input_active = False
letter2_input_active = False
letter3_input_active = False
letter4_input_active = False
letter5_input_active = False
play_counter = 0

"""def update(user_answer): 
    user_answer_char_list = list(user_answer)

    for i in range(5): 
        txt_surface = font.render(user_answer_char_list[i], True, (0,0,0))
      #  Letter_class_list[(play_counter*5)+i].text = user_answer_char_list[i]
        Letter_class_list[(play_counter*5)+i].addText(user_answer_char_list[i])
       # screen.blit(txt_surface, (Letter_class_list[(play_counter*5)+i].left_x,Letter_class_list[(play_counter*5)+i].top_y))

    play_counter = play_counter + 1

    pygame.display.update() """


while not_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            not_done = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if enter_button_rect.collidepoint(event.pos): 
                if letter1_input_active and letter2_input_active and letter3_input_active and letter4_input_active and letter5_input_active: 
                    
                    print("User answer is: ", user_answer)
                    user_answer_char_list = list(user_answer)
                    answer_Dict = every_input(user_answer)
                    
                    txt_surface = font.render(user_answer_char_list[0], True, (0,0,0))

                    print("break 1")
                    print("Play counter: ", play_counter)

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[0]: 
                            pygame.draw.rect(display_screen, green, (50,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (50,(50+(play_counter*100)),100,100), width = border_width)
                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)].left_x + 25, Letter_class_list_input[(play_counter*5)].top_y + 25))
                            print("green 1")

                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[0]: 
                                    pygame.draw.rect(display_screen, green, (50,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (50,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)].left_x + 25, Letter_class_list_input[(play_counter*5)].top_y + 25))
                                
                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)].left_x + 25, Letter_class_list_input[(play_counter*5)].top_y + 25))
                    
                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[1], True, (0,0,0))

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[1]: 
                            pygame.draw.rect(display_screen, green, (150,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (150,(50+(play_counter*100)),100,100), width = border_width)
                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+1].left_x + 25, Letter_class_list_input[(play_counter*5)+1].top_y + 25))
                            print("green 2")

                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[1]: 
                                    pygame.draw.rect(display_screen, green, (150,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (150,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+1].left_x + 25, Letter_class_list_input[(play_counter*5)+1].top_y + 25))

                                
                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+1].left_x + 25, Letter_class_list_input[(play_counter*5)+1].top_y + 25))
                    
                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[2], True, (0,0,0))

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[2]: 
                            pygame.draw.rect(display_screen, green, (250,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (250,(50+(play_counter*100)),100,100), width = border_width)
                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+2].left_x + 25, Letter_class_list_input[(play_counter*5)+2].top_y + 25))
                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[2]: 
                                    pygame.draw.rect(display_screen, green, (250,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (250,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+2].left_x + 25, Letter_class_list_input[(play_counter*5)+2].top_y + 25))

                                
                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+2].left_x + 25, Letter_class_list_input[(play_counter*5)+2].top_y + 25))
                    
                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[3], True, (0,0,0))

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[3]: 
                            pygame.draw.rect(display_screen, green, (350,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (350,(50+(play_counter*100)),100,100), width = border_width)

                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+3].left_x + 25, Letter_class_list_input[(play_counter*5)+3].top_y + 25))
                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[3]: 
                                    pygame.draw.rect(display_screen, green, (350,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (350,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+3].left_x + 25, Letter_class_list_input[(play_counter*5)+3].top_y + 25))

                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+3].left_x + 25, Letter_class_list_input[(play_counter*5)+3].top_y + 25))

                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[4], True, (0,0,0))
                    
                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[4]: 
                            pygame.draw.rect(display_screen, green, (450,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (450,(50+(play_counter*100)),100,100), width = border_width)

                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+4].left_x + 25, Letter_class_list_input[(play_counter*5)+4].top_y + 25))
                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[4]: 
                                    pygame.draw.rect(display_screen, green, (450,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (450,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+4].left_x + 25, Letter_class_list_input[(play_counter*5)+4].top_y + 25))

                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+4].left_x + 25, Letter_class_list_input[(play_counter*5)+4].top_y + 25))

                    play_counter = play_counter + 1
                    letter1_input_active = False
                    letter2_input_active = False
                    letter3_input_active = False
                    letter4_input_active = False
                    letter5_input_active = False
                    enter_button_active = False
            
            elif pygame.Rect(Letter_class_list_input[0].left_x,Letter_class_list_input[0].top_y, 100,100).collidepoint(event.pos): 
                letter1_input_active = True

            elif pygame.Rect(Letter_class_list_input[1].left_x,Letter_class_list_input[1].top_y, 100,100).collidepoint(event.pos): 
                letter2_input_active = True

            elif pygame.Rect(Letter_class_list_input[2].left_x,Letter_class_list_input[2].top_y, 100,100).collidepoint(event.pos): 
                letter3_input_active = True

            elif pygame.Rect(Letter_class_list_input[3].left_x,Letter_class_list_input[3].top_y, 100,100).collidepoint(event.pos): 
                letter4_input_active = True

            elif pygame.Rect(Letter_class_list_input[4].left_x,Letter_class_list_input[4].top_y, 100,100).collidepoint(event.pos): 
                letter5_input_active = True

        if event.type == pygame.KEYDOWN:
            if letter1_input_active or letter2_input_active or letter3_input_active or letter4_input_active or letter5_input_active: 
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                    user_answer = user_answer[:-1]
                    pygame.display.update()

                    #should change letter input active to False here technically 
                else:
                    user_text = event.unicode
                    user_answer = user_answer+user_text
                    
            txt_surface = font.render(user_text, True, (0,0,0))

            if letter1_input_active == True: 

                if letter2_input_active == True: 

                    if letter3_input_active == True: 

                        if letter4_input_active == True: 

                            if letter5_input_active == True: 

                                display_screen.blit(txt_surface, (Letter_class_list_input[4].left_x + 25,Letter_class_list_input[4].top_y + 25))
                            else: 
                                display_screen.blit(txt_surface, (Letter_class_list_input[3].left_x + 25,Letter_class_list_input[3].top_y + 25))
                        else: 
                            display_screen.blit(txt_surface, (Letter_class_list_input[2].left_x + 25,Letter_class_list_input[2].top_y + 25))
                    else: 
                        display_screen.blit(txt_surface, (Letter_class_list_input[1].left_x + 25,Letter_class_list_input[1].top_y + 25))
                else: 
                    display_screen.blit(txt_surface, (Letter_class_list_input[0].left_x + 25,Letter_class_list_input[0].top_y + 25))

    pygame.display.update()
    #pygame.display.flip()


    
