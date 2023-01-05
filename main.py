import pygame
import random

#Creating window
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.image.load('title card.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

pygame.display.set_caption("Hangman game!")
pygame.mouse.set_cursor()

# scenes
won_img = pygame.image.load('win_screen.png')
won_img = pygame.transform.scale(won_img, (WIDTH, HEIGHT))
lose_img = pygame.image.load('lose_screen.png')
lose_img = pygame.transform.scale(lose_img, (WIDTH, HEIGHT))
c_1 = pygame.image.load('cutscene_1.jpeg')
c_1 = pygame.transform.scale(c_1, (WIDTH, HEIGHT))
c_2 = pygame.image.load('cutscene_2.jpeg')
c_2 = pygame.transform.scale(c_2, (WIDTH, HEIGHT))

# load images into list
images = []
for i in range(6):
    image = pygame.image.load("hangman" + str(i) + ".png")
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    images.append(image)

# button variables
GAP = 15
RADIUS = 20
letters = []
#determines the starting position according to Radius and gap
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65
#stores the position,letter and visibility of all buttons
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

#font
LETTER_FONT = pygame.font.SysFont("comicsans",40)

counter = 0
speed = 3

# game variables
hangman_status = 0

#words to be guessed
words = ["class", "integer", "string", "def", "print", "input", "list", "dictionary"]
word = random.choice(words).upper()
guessed = []

#color
maroon = (124, 0, 0)


# drawing everything
def draw():
    #background is being drawn
    #win.blit(bg_img, (0, 0))
    win.blit(images[hangman_status], (0, 0))

    #drawing the word
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    display_text = LETTER_FONT.render(display_word, 1, maroon)
    win.blit(display_text, (400, 200))

    #draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, maroon, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, maroon)
            win.blit(text,(x - text.get_width() / 2, y -text.get_height() / 2))  #shifting the center of the letters

    pygame.display.update()

  
#resetting the game variables

def reset_game():
    global hangman_status
    global word
    global guessed
    global letters
    global i
    global x
    global y
    global counter
    counter = 0
    hangman_status = 0
    word = random.choice(words).upper()
    guessed = []
    letters = []
    for i in range(26):
        x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = start_y + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


#This is the main logic of the game

def main():
    run = True
    #Frame rate
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        global hangman_status
        clock.tick(FPS)
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        #checking for collision
                        dist = ((m_x - x)**2 + (m_y - y)**2)**(1 / 2)
                        if dist < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()
        #to check if we won or lost
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            win.blit(won_img, (0, 0))
            pygame.display.update()
            pygame.mixer.init()
            win_s = pygame.mixer.Sound("win sound.wav")
            pygame.mixer.Sound.play(win_s)
            pygame.time.delay(7000)
            reset_game()
            break
            
        if hangman_status == 5:
            pygame.time.delay(1000)
            win.blit(lose_img, (0, 0))
            pygame.display.update()
            pygame.mixer.init()
            lose_s = pygame.mixer.Sound("lose sound.wav")
            pygame.mixer.Sound.play(lose_s)
            pygame.time.delay(7000)
            reset_game()
            break
    reset_game()



#creating the cutscene
def cutscene():
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        win.blit(c_2,(0,0))
        pygame.display.update()
        pygame.time.delay(10000)
        pygame.display.update()
        win.blit(c_1,(0,0))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        pygame.display.update()
        break
    


#This is the main menu of the game
def main_menu():
    play_game = True
    global counter

    clock = pygame.time.Clock()
    while play_game:
        clock.tick(60)
        win.blit(bg_img, (0, 0))
        #pygame.mixer.init()
        #menu_s = pygame.mixer.Sound("main menu.wav")
        #pygame.mixer.Sound.play(menu_s)
        s = "Click the Mouse Button to Play"
        rules="All the words are related to python"
        if counter < speed * len(rules):
            counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #pygame.mixer.Sound.stop(menu_s)
                main()
        text = LETTER_FONT.render(s[0:counter // speed], 1, maroon)
        rule = LETTER_FONT.render(rules[0:counter // speed], 1, maroon)

        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 300))
        win.blit(rule, (WIDTH / 2 - text.get_width() / 2, 350))

        pygame.display.update()
        
    pygame.quit()


cutscene()

while True:
    main_menu()
pygame.quit()

#Satvik will explain the variable part
#Akshat will explain main function
#Aradhya will explain draw function
#Khushi will explain reset_game function
#Sargam will explain main menu function
#Yashi will explain cutscene function
