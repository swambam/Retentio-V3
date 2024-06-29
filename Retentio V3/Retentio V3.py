import pygame
import random
import csv
from collections import Counter
import sys
sys.setrecursionlimit(20000)

with open("data.txt", newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    data =[]
    for row in rows:
        data.append(row)

#*******************************************

#Making a list of 0th elements
listof0s = []
len(data)
for i in range(len(data)):
    x = data[i][0]
    listof0s.append(x)

#Made a single list of each element in each list.
listofall = []
for i in range(len(data)):
    x = data[i]
    listofall.extend(x)

#Trying to make a list of all Origins
listoforigins = []
listofnotorigins = []
listofnot0s = []
#Made a list of all elements which are not 0th elements in order to make a list of Origins
listofnot0s = list((Counter(listofall)-Counter(listof0s)).elements())
for i in range(len(listof0s)):
    x = listof0s[i]
    if x in listofnot0s:
        listofnotorigins.append(x)
listoforigins = list((Counter(listof0s)-Counter(listofnotorigins)).elements())

#Accidentaly made a list of endpoints [note that the below method subtracts all elements unlike the Counter method which subtracts only one element per element]
listofendpoints = list(set(listofall) - set(listof0s))

#*********************************************

# Initialize Pygame
pygame.init()

# Set up the Pygame window
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Falling Bricks Game")

# Toggle fullscreen mode
fullscreen = False

# Colors
BLACK = (0, 0, 0)
RED = (255, 50, 50)
LIGHTGRAY = (250, 250, 255)
GRAY = (140, 140, 140)


# Clock for controlling the game's frame rate
clock = pygame.time.Clock()

# Player variables
player_width, player_height = 230, 50
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - 2 * player_height
player_speed = 7

# Brick variables
brick_width, brick_height = 200, 140
bricks = []
brick_speed = 2
brick_spacing = 55  # Spacing between bricks
brick_row_width = 5  # Number of bricks in a row

# Score
score = 0

# Loads the Bahnschrift Condensed font if available
font_name = "Bahnschrift Condensed"
font_size = 28
font = pygame.font.SysFont(font_name, font_size)

#Wrap text 
def wrap_text(text, font, max_width):
    """Splits text into multiple lines to fit within the max_width."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)
    return lines


# Variable to store the player's selection
playerselection = None

def main(answer):
    global brick_speed ##############
    brick_speed=2      ##############
    collisioncount = 0
    nestedlist = []
    global playerselection
    global win
    global score
    global WIDTH
    global HEIGHT
    global player_x
    global player_y
    # Main game loop
    if answer in listof0s:
        #Correct option:
        for i in range(len(data)):
            if answer == data[i][0]:
                for x in range (len(data[i])):
                    nestedlist.append(data[i][x])
        nestedlist.pop(0)           
        correctoption = random.choice(nestedlist)
        #Other options:
        finalotheroptionlist = list(set(listofall) - set(nestedlist))

        option2 = random.choice(finalotheroptionlist)
        option3 = random.choice(finalotheroptionlist)
        option4 = random.choice(finalotheroptionlist)
        option5 = random.choice(finalotheroptionlist)
        optionslist1 = [correctoption, option2, option3, option4, option5]
        random.shuffle(optionslist1)
        running = True
        while running:
            win.fill(BLACK)

            # List of text strings for each brick
            brick_texts = optionslist1

            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    player_x = min(player_x, WIDTH - player_width)
                    player_y = min(player_y, HEIGHT - player_height)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.iconify()

            # Move the player paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed

            # Generate new row of bricks
            if len(bricks) == 0:
                start_x = (WIDTH - (brick_row_width * (brick_width + brick_spacing) - brick_spacing)) // 2
                for i in range(brick_row_width):
                    brick_x = start_x + i * (brick_width + brick_spacing)
                    bricks.append([brick_x, 0, brick_texts[i]])

            # Update brick positions
            for brick in bricks:
                brick[1] += brick_speed
                pygame.draw.rect(win, RED, (brick[0], brick[1], brick_width, brick_height))

                # Render wrapped text on the brick
                wrapped_lines = wrap_text(brick[2], font, brick_width - 10)  # 10 pixels padding
                line_height = font.size("Tg")[1]  # Height of a single line of text
                for i, line in enumerate(wrapped_lines):
                    text_surface = font.render(line, True, LIGHTGRAY)  # Gray text color
                    text_rect = text_surface.get_rect(center=(brick[0] + brick_width // 2, brick[1] + line_height // 2 + i * line_height))
                    win.blit(text_surface, text_rect)

                # Check for collision with player paddle
                if (brick[1] + brick_height >= player_y and
                    brick[1] <= player_y + player_height and
                    brick[0] + brick_width >= player_x and
                    brick[0] <= player_x + player_width):
                    playerselection = brick[2]  # Store the text of the touched brick
                    bricks.remove(brick)
                    #print(f"Player selection: {playerselection}")  # Debug print
                    if playerselection:
                        collisioncount+=1
                    if collisioncount>0:    
                        if playerselection == correctoption:
                            score+=5
                            
                            main(playerselection)
                        
                        else:
                            score-=10
                            playerselection = None
                            start()

                # Remove brick if it goes off the screen
                if brick[1] > HEIGHT:
                    bricks.remove(brick)

            # Draw the player paddle
            pygame.draw.rect(win, GRAY, (player_x, player_y, player_width, player_height))

            # Display the status
            status_text = font.render("Status: MAIN", True, RED)
            win.blit(status_text, (30, 30))

            # Display the score
            score_text = font.render("Score: " + str(score), True, RED)
            win.blit(score_text, (10, 10))

            # Display the player's selection
            if playerselection:
                selection_text = font.render("Selected: " + playerselection, True, RED)
                win.blit(selection_text, (10, 50))
                #print(f"Rendering selection: {playerselection}")  # Debug print

            pygame.display.update()
            clock.tick(60)
    else:
        playerselection = None
        start()

def start():
    global brick_speed ##############
    brick_speed+=1      ##############
    global playerselection
    global win
    global score
    global WIDTH
    global HEIGHT
    global player_x
    global player_y
    # Main game loop
    running = True
    while running:
        win.fill(BLACK)

        # List of text strings for each brick
        optionelement = []
        for i in range(5):    
            optionelement.append(random.choice(listoforigins))

        brick_texts = optionelement

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                player_x = min(player_x, WIDTH - player_width)
                player_y = min(player_y, HEIGHT - player_height)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.iconify()

        # Move the player paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Generate new row of bricks
        if len(bricks) == 0:
            start_x = (WIDTH - (brick_row_width * (brick_width + brick_spacing) - brick_spacing)) // 2
            for i in range(brick_row_width):
                brick_x = start_x + i * (brick_width + brick_spacing)
                bricks.append([brick_x, 0, brick_texts[i]])

        # Update brick positions
        for brick in bricks:
            brick[1] += brick_speed
            pygame.draw.rect(win, RED, (brick[0], brick[1], brick_width, brick_height))

            # Render wrapped text on the brick
            wrapped_lines = wrap_text(brick[2], font, brick_width - 10)  # 10 pixels padding
            line_height = font.size("Tg")[1]  # Height of a single line of text
            for i, line in enumerate(wrapped_lines):
                text_surface = font.render(line, True, LIGHTGRAY)  # Gray text color
                text_rect = text_surface.get_rect(center=(brick[0] + brick_width // 2, brick[1] + line_height // 2 + i * line_height))
                win.blit(text_surface, text_rect)

            # Check for collision with player paddle
            if (brick[1] + brick_height >= player_y and
                brick[1] <= player_y + player_height and
                brick[0] + brick_width >= player_x and
                brick[0] <= player_x + player_width):
                playerselection = brick[2]  # Store the text of the touched brick
                bricks.remove(brick)
                #print(f"Player selection: {playerselection}")  # Debug print
                #score += 5

            # Remove brick if it goes off the screen
            if brick[1] > HEIGHT:
               bricks.remove(brick)

        # Draw the player paddle
        pygame.draw.rect(win, GRAY, (player_x, player_y, player_width, player_height))

        # Display the score
        score_text = font.render("Score: " + str(score), True, RED)
        win.blit(score_text, (10, 10))

        # Display the status
        status_text = font.render("Status: START", True, RED)
        win.blit(status_text, (30, 30))

        # Show that we are in the Start Function
        start_text = font.render("Select an Origin to start", True, RED)
        win.blit(start_text, (837, 50))

        # Display the player's selection
        if playerselection:
            selection_text = font.render("Selected: " + playerselection, True, RED)
            win.blit(selection_text, (10, 50))
            #print(f"Rendering selection: {playerselection}")  # Debug print
            main(playerselection)

        pygame.display.update()
        clock.tick(60)
        
        #if playerselection:
            #main(playerselection)

start()
pygame.quit()
