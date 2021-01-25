import RPi.GPIO as GPIO
from graphics import *
from time import sleep
import random


# initialize pin num
GREEN = 11
YELLOW = 13
RED = 15
FAN = 37

# window size
HEIGHT = 350
WIDTH = 350


# print start screen to window
def start_screen(win):
    txt = Text(Point(HEIGHT/2, WIDTH/3), 'Game will start in 3 seconds!')
    txt.setSize(16)
    txt.setFace('times roman')
    txt.draw(win)
    for i in range(30):
        r = random.randint(0, 255)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        txt.setTextColor(color_rgb(r, b, g))
        sleep(0.1)
        

# clear window of all objects
def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()


# print watch_sequence screen to window
def print_watch_sequence(win):
    txt = Text(Point(HEIGHT/2, WIDTH/3), 'WATCH_THE_SEQUENCE_!')
    txt.setSize(17)
    txt.setFace('times roman')
    txt.setTextColor(color_rgb(255, 0, 127))
    txt.draw(win)
    

# print current sequence number to window
def print_sequence_number(win, score):
    output = 'SEQUENCE_NUMBER: ' + str(score)
    level = Text(Point(HEIGHT/2, 200), output)
    level.setSize(13)
    level.setFace('times roman')
    level.setTextColor(color_rgb(255, 255, 255))
    level.draw(win)
    

# print directions for user to window
def print_directions(win):
    green = Text(Point(HEIGHT/2, 250), 'PRESS 1 FOR GREEN')
    green.setSize(6)
    green.setFace('times roman')
    green.setTextColor(color_rgb(0, 204, 0))
    
    yellow = Text(Point(HEIGHT/2, 265), 'PRESS 2 FOR YELLOW')
    yellow.setSize(6)
    yellow.setFace('times roman')
    yellow.setTextColor(color_rgb(255, 255, 51))
    
    red = Text(Point(HEIGHT/2, 280), 'PRESS 3 FOR RED')
    red.setSize(6)
    red.setFace('times roman')
    red.setTextColor(color_rgb(255, 0, 0))
    
    txt = Text(Point(HEIGHT/2, 235), 'CLICK ANYWHERE TO SUBMIT')
    txt.setSize(7)
    txt.setFace('times roman')
    txt.setTextColor(color_rgb(255, 255, 255))
    
    txt.draw(win)
    green.draw(win)
    yellow.draw(win)
    red.draw(win)
    

# print game over screen to window
def game_over_screen(win):
    end_prompt = Text(Point(HEIGHT/2, WIDTH/3), 'GAME_OVER_!')
    end_prompt.setSize(28)
    end_prompt.setFace('times roman')
    end_prompt.draw(win)
    for i in range(30):
        r = random.randint(0, 255)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        end_prompt.setTextColor(color_rgb(r, b, g))
        sleep(0.1)


# return user guess
def get_user_input(win):
    entry_box = Entry(Point(HEIGHT/2, WIDTH/2), 25)
    entry_box.draw(win)
    win.getMouse()
    guess = entry_box.getText()
    return guess


# set pins to output mode
def pins_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(YELLOW, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    

# set pins output to false    
def pins_false():
    GPIO.output(GREEN, False)
    GPIO.output(YELLOW, False)
    GPIO.output(RED, False)


# flash led sequence to user
def flash_pins(sequence, length):
    random_light = random.randint(1,3)
    sequence.append(random_light)
    for i in range(length):
        sleep(0.2)
        if sequence[i] == 1:
            GPIO.output(GREEN, GPIO.HIGH)
            sleep(0.4)
            GPIO.output(GREEN, GPIO.LOW)
        elif sequence[i] == 2:
            GPIO.output(YELLOW, GPIO.HIGH)
            sleep(0.4)
            GPIO.output(YELLOW, GPIO.LOW)
        elif sequence[i] == 3:
            GPIO.output(RED, GPIO.HIGH)
            sleep(0.4)
            GPIO.output(RED, GPIO.LOW)
    length += 1


# main
def main():
    # create game window
    win = GraphWin('Blinky Game', HEIGHT, WIDTH)
    win.config(bg='black')

    # setup pins
    GPIO.setwarnings(False)
    pins_setup()
    pins_false()
    
    # setup game varibles
    game_over = False
    sequence = []
    length = 1
    score = 1
    
    start_screen(win)
    clear(win)
    while not game_over:
        print_watch_sequence(win)
        sleep(1.5)
        
        flash_pins(sequence, length)
        length += 1
        
        print_sequence_number(win, score)
        print_directions(win)
        guess = list(get_user_input(win))
        guess = [int(i) for i in guess]
        
        clear(win)
        if guess != sequence:
            print_sequence_number(win, score)
            game_over_screen(win)
            game_over = True
        else:
            score += 1
            

    # close window, reset pins
    win.close()
    GPIO.cleanup()

main()