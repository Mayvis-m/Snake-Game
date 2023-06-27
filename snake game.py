from tkinter import *
import random


# the constance are variables that do not change (kinda like the settings)
GAME_WIDTH = 650
GAME_HEIGHT = 600
SPEED = 50                                  # lower the number, faster the game
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#C39BD3"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):                     # will construct the snake

        self.body_size = BODY_PARTS         # I have a snake that has a body size
        self.coordinates = []               # a list if coordinates
        self.squares = []                   # and a list of square graphics

        for i in range(0, BODY_PARTS):          # creates a list of coordinates
            self.coordinates.append([0, 0])     # coordinates set at 0,0 so snake appears at the top left corner

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")  # creates squares
            self.squares.append(square)

class Food:
    
    def __init__(self):                     # will construct a food object

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE             # random.randint places food object randomly
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]           # list of x and y

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")       # draws food object on canvas

def next_turn(snake, food):
    
    x,y = snake.coordinates[0]        # head of the snake

    if direction == "up":               # if the direction is up (y axis)
        y -= SPACE_SIZE                 # moves up (y axis)
    elif direction == "down":
        y += SPACE_SIZE                 # moves down (y yaxis)
    elif direction == "left":
        x -= SPACE_SIZE                 # moves to the left (x axis)
    elif direction == "right": 
        x += SPACE_SIZE                 # moves to the right (x axis)

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)    # new graphic for the head of the snake

    snake.squares.insert(0, square)     # updated snake's list of squares

    # makes the food consumable 
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else: 

        del snake.coordinates[-1]           # deletes the last body part of the snake

        canvas.delete(snake.squares[-1])     # updates the canvas

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:    
     
        window.after(SPEED, next_turn, snake, food)     # calls the next_turn function again

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
        
# stops the snake from leaving the canvas/prints game over
def check_collisions(snake):
    
    x,y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
        
    return False

# displays game over in red
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# the window
window = Tk()
window.title("Snake game")              # title of window
window.resizable(False, False)          # false, false means window is not resizable

# the score label
score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# creates the gameboard
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# centers window when it appears
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# bind keys
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
