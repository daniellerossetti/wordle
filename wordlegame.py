
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
screen_width=600
screen_height=750
box_color = (211, 211, 211) #light gray
yellow = (255, 191, 0)
green = (60, 179, 113)
dark_gray = (105,105,105)
other_dark_gray = (169,169,169)
border_width = 3
border_color = (0,0,0)

# class the contains the highest level of the game / includes most of everything else 
# picking the answer, setting up the display, and creating all game objs start here 
class Game:
    def __init__(self):
    
        # answer str and pandas df with all possible answers
        self.answer, self.df = self.pick_word() 
        self.display_screen, self.font = self.display_setup() # pygame surface and font obj
        self.box_grid = self.make_grid() # 6x5 grid of boxes 

        self.banner_on = False # True if message is on screen
        self.over = False # True if game over

        # set where the words will be typed 
        self.curr_row = 0 # based on how many words have been guessed
        self.curr_col = 0 # based on how many ch have been typed/deleted
        self.curr_box = self.box_grid[self.curr_row][self.curr_col] # cursor

    def pick_word(self):
        # open pandas dataframe with the words from online database
        df = pd.read_csv('https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt')

        # choose number at random in the range of # of rows in dataframe 
        chosen_idx = random.choice(df.index)

        chosen_word = str(df.iloc[chosen_idx][0])
        print("The answer to this wordle is: ", chosen_word)

        return chosen_word, df

    # starts pygame, sets up stuff on screen 
    def display_setup(self):
        pygame.init()
        font = pygame.font.Font('freesansbold.ttf', 25)
        display_screen = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption("WORDLE")

        display_screen.fill(dark_gray)

        # for 'wordle' at the top
        font2 = pygame.font.Font('freesansbold.ttf', 30)
        wordle = "W      O       R       D       L       E"
        display_screen.blit(font.render(wordle, True, (0,0,0)), (50,25,500,50))

        # for banner / messages box
        pygame.draw.rect(display_screen, box_color, (50, 660,500,70))
        pygame.draw.rect(display_screen, border_color, (50, 660,500,70), width = border_width)

        return display_screen, font   

    # creates all of the boxes and puts them in a grid
    def make_grid(self):
        box_grid = []
        for i in range(6): # n of rows
            box_list = []
            for j in range(5): # n of columns
                box = Box(self.display_screen, i, j)
                box.draw_box() # draw box on display
                box_list.append(box)
            box_grid.append(box_list)
        return box_grid

    # note: args are by what you want to incr/decr the indexes by
    def update_curr_box(self, p, q):
        self.curr_row = self.curr_row + p
        self.curr_col = self.curr_col + q
        self.curr_box = self.box_grid[self.curr_row][self.curr_col]

    # to display errors and show person if they won or lost
    def display_banner(self, text):
        self.display_screen.blit(self.font.render(text, True, (0,0,0)), (100, 675,200,75))

    # after pressing enter, it changes the colors of the current row
    def update_colors(self):
        if self.curr_col > 4: self.curr_col = 4 # in case its 5!
        row = self.box_grid[self.curr_row]
        for i in range(5):
            if row[i].letter == self.answer[i]:
                row[i].draw_box(green)
                row[i].add_text(row[i].letter, self.font)
            elif row[i].letter in self.answer:
                row[i].draw_box(yellow)
                row[i].add_text(row[i].letter, self.font)
            else:
                row[i].draw_box(other_dark_gray)
                row[i].add_text(row[i].letter, self.font)

    # function called if pygame event is determined to be KEYDOWN
    def key_pressed(self, event):
        # reset banner if key pressed
        if self.banner_on:
            pygame.draw.rect(self.display_screen, box_color, (50, 660,500,70))
            pygame.draw.rect(self.display_screen, border_color, (50, 660,500,70), width = border_width)
            banner_on = False

        if event.key == pygame.K_BACKSPACE:
            # remove letter from curr box field 
            if self.curr_col != 5: self.curr_box.letter = ""

            #set curr box to previous col if not out of bounds
            if self.curr_col != 0:
                # if curr_col was moved to 5 when typing last letter, it'll be on 4 now
                self.update_curr_box(0, -1)

            # delete letter by drawing box over it
            self.curr_box.draw_box()
            
        elif event.key == pygame.K_RETURN:
            
            # check if there are 5 letters
            row = self.box_grid[self.curr_row]
            if row[0].letter and row[1].letter and row[2].letter and row[3].letter and row[4].letter:
                self.update_colors()
                # todo: check if answer is in list
                
                # todo: make sure this isnt the end of the game
                correct_count = 0
                for i in range(5):
                    if self.box_grid[self.curr_row][i].letter == self.answer[i]:
                        correct_count += 1
                print(correct_count)
                if correct_count == 5:
                    text = "Your guess was correct! You won!"
                    self.display_screen.blit(self.font.render(text, True, (0,0,0)), (100, 675,200,75))
                    self.banner_on = True
                    self.over = True
                elif self.curr_row == 6:
                    text = "You're out of guesses! You lost :("
                    self.display_screen.blit(self.font.render(text, True, (0,0,0)), (100, 675,200,75))
                    self.banner_on = True
                    self.over = True
                else:
                    # move down one row and back to first col
                    self.update_curr_box(1, -4)

            else:
                # display banner
                text = "Your guess must have 5 letters!"
                self.display_screen.blit(self.font.render(text, True, (0,0,0)), (100, 675,200,75))
                self.banner_on = True

        else: 
            ch = chr(event.key).lower() # get char and lowercase it
            if ch.isalpha(): # only move forward is its a letter
                if self.curr_col < 4:
                    self.curr_box.add_text(ch, self.font)
                    self.curr_box.letter = ch
                    self.update_curr_box(0, 1) 
                elif self.curr_col == 4: 
                    self.curr_box.add_text(ch, self.font)
                    self.curr_box.letter = ch
                    # dont want to update curr box bc there is no col at idx 5
                    # but still want to move the cursor forward
                    self.curr_col = 5
                # else: (if self.curr_col > 5)
                #   we dont want it to type anything until a backspace happens

# class for each of the boxes on the display
class Box:
    def __init__(self, display_screen, i, j):
        self.display_screen = display_screen
                
        # box's location in the grid
        self.i = i
        self.j = j
        self.box_color = box_color
        self.letter = ""

    def draw_box(self, color=box_color):
        pygame.draw.rect(self.display_screen, color, (50 + (self.j*100), 50 + (self.i*100),100,100))
        pygame.draw.rect(self.display_screen, border_color, (50 + (self.j*100), 50 + (self.i*100),100,100), width = border_width)

    def add_text(self, text, font):
        text = font.render(text, True, (0,0,0))
        self.display_screen.blit(text, (50 + (self.j*100), 50 + (self.i*100)))
        self.letter = text

def main():

    game = Game()
    
    while not game.over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.over = True
            
            if event.type == pygame.KEYDOWN:
                game.key_pressed(event)

        pygame.display.update()

if __name__ == "__main__":
    main()