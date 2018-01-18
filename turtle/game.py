
import turtle
import random
import pygame
import time

"""
    Constants and variables
"""
pygame.init()
pygame.mixer.init(buffer=16)
bg_sound = pygame.mixer.Sound('Sound.wav')
lost_sound = pygame.mixer.Sound('lost.wav')
bg1_sound = pygame.mixer.Sound('Sound1.wav')
bg2_sound = pygame.mixer.Sound('Sound2.wav')
ball_sound = pygame.mixer.Sound('ball.wav')
kill_sound = pygame.mixer.Sound('kill.wav')
kick_sound = pygame.mixer.Sound('kick.wav')
invulnerable_sound = pygame.mixer.Sound('invulnerable.wav')
turtle.bgpic('bg.gif')
# Window size
window_height = 600
window_width = 600
rank = []
# The screen update interval
update_interval = 25
ball_order = 0
ball_index = []
stones = []
stone_speed = []
bomb_number = []
dead_bomber = []
bomber = []
stun = False
Gauss = False
stone_state = False
bomb_stage = False
passed = False
# Parameters for controlling the width of the river
river_width = 300
minimum_width = 100
davis_ball_count = 0

# Border parameters
border_height = 600

# Parameters for gradually decreasing river width
river_width_update = 0.5

# How far should we stay away from the borders
safe_distance_from_border = border_height / 2 + 3

# Parameters for crocodiles
turtle.tracer(False)
crocodile_number = 4
stone_number = 45
crocodiles = []
crocodile_speeds = []
crocodile_width = 100
crocodile_height = 40
crocodile_speed_min, crocodile_speed_max = 1, 4
score = 0
time_survived = 0
stop_number = 0
stopped = False
state = False
item_state = True
stuned = False
kill_number = 0
invulnerable_number = 0
davis_number = 0
julian_number = 0
kick_count = 0
# How far should we stay away from the crocodiles
safe_distance_from_crocodile = 25
return_button = turtle.Turtle()
return_button.hideturtle()
david_ball = []
david_balls = []
ball_order = 0
ability_number = 0
ball_state = False
kick_state = False
bell = True
user = "davis"


turtle.addshape("upper_border.gif")
turtle.addshape("lower_border.gif")
turtle.addshape("crocodile.gif")
turtle.addshape("davis.gif")
turtle.addshape("dennis.gif")
turtle.addshape("davis0.gif")
turtle.addshape("davis1.gif")
turtle.addshape("davis2.gif")
turtle.addshape("davis3.gif")
turtle.addshape("stone.gif")
for i in range(0, 5):
    turtle.addshape("julian" + str(i) + ".gif")
    turtle.addshape("davis_" + str(i) + ".gif")


turtle.addshape("davis_death.gif")
turtle.addshape("dennis_death.gif")
turtle.addshape("davis_ball.gif")


for i in range(0, 4):
    turtle.addshape("dennis" + str(i) + ".gif")
    turtle.addshape("dennis_" + str(i) + ".gif")
    turtle.addshape("bomb_" + str(i) + ".gif")
    
turtle.title("Little FighterEscape Extra Version 1.3.0")
'''--------------------------------'''


"""
    Helper function and event handler functions
"""

# Show a message when the game end
def gameover(message):
    global ball_order
        
    bg_sound.stop()
    bg2_sound.stop()
    lost_sound.play()
    global retry_button
    global state
    global rank
    global Gauss
    label_turtle.goto(0, 150)
    #Display message, score and survived time
    label_turtle.write(message, align="center", font=("Arial", 24, "normal"))
    label_turtle.goto(0, 100)
    label_turtle.write("Your Score: " + str(score) , align="center", font=("Arial", 24, "normal"))
    label_turtle.goto(0, 50)
    label_turtle.write("Time survived: " + str(time_survived) , align="center", font=("Arial", 24, "normal"))
    turtle.ondrag(None)
    state = False
    Gauss = True
    retry_button.goto(-40, 25)
    retry_button.color("black")
    retry_button.begin_fill()
    for _ in range(2):
        retry_button.forward(80)
        retry_button.left(90)
        retry_button.forward(25)
        retry_button.left(90)
    retry_button.end_fill()
    retry_button.color("white")
    retry_button.goto(0, 30)
    retry_button.write("Retry", font=("Arial", 10, "bold"), align="center")
    retry_button.goto(0, 38)
    retry_button.color("")
    retry_button.showturtle()
    turtle.shape(str(user) + "_death.gif") #Play death animation
    for i in range(len(david_ball)):
        david_ball[i].hideturtle()
        david_ball[i].goto(9999,9999)
        
    turtle.update()
    if score > min(rank): #Check if your score can enter the rank
        label_turtle.goto(0, -50)
        label_turtle.write("You achieve a Record!" , align="center", font=("Arial", 24, "normal"))
        rank.pop()
        rank.append(score) #Replace the lowest score with your score
        rank = sorted(rank, reverse=True) #Sort the ranking descendingly
                
        ranking_file = open('ranking.txt', 'w') #Clear the file content and write new thing
        for i in range(len(rank)):
            score_lin = str(rank[i]) + '\t' + '\n'
            ranking_file.write(score_lin)

        ranking_file.close()
        

# Event handler for the turtle.ondrag() event
def moveturtle(x, y):
    # Allow the turtle to move within the window only
    if x > -window_width / 2 and x < window_width / 2:
        if y > -window_width / 2 and y < window_width / 2:

            turtle.goto(x, y)
            

# Event handler for the turtle.ontimer() event
def updatescreen():
    global river_width
    global lower_border_height
    global upper_border_height
    global river_width_update
    global score
    global ball_order
    global ball_index
    global stuned

    
    # Decrease the width of the river by river_width_update
    upper_border.sety(upper_border.ycor() - river_width_update)
    lower_border.sety(lower_border.ycor() + river_width_update)
    river_width = river_width - 2*river_width_update

    if not state:
        return    
    #upper_border_height = upper_border_height - river_width_update
    #lower_border_height = lower_border_height + river_width_update
 
    # Check if the player has won the game
    if river_width <= minimum_width or bomb_stage:
        river_width_update = 0
    # If the player survives until the river gets to its narrowest 
    # width, the river stop decreasing in width
    
    # Check if the player has hit the borders
    if upper_border.ycor() - turtle.ycor() < safe_distance_from_border:
        gameover("OMG!! You touch the border!!!")
        return
    if  turtle.ycor() - lower_border.ycor() < safe_distance_from_border:
        gameover("OMG!! You touch the border!!!")
        return
    # The vertical distance between the player's turtle and the 
    # borders must be large enough, otherwise the player loses
    # the game

    # Move the crocodiles
    # For every crocodile in crocodiles
    if not stun and not bomb_stage:#Originally, this condition is use for the stunning effects,but has been gave up, so ignore it
        for i in range(crocodile_number):
            # Move the crocodile to the left
            crocodiles[i].forward(crocodile_speeds[i])
            # If the crocodile moves out of the screen, move it 
            #    to the right hand side and generate its speed and 
            #    position randomly
            if crocodiles[i].xcor() < -(window_width+crocodile_width)/2:
                x = (window_width + crocodile_width)/2
                y = random.uniform(-(river_width - crocodile_height)/2, (river_width - crocodile_height)/2)
                crocodiles[i].goto(x, y)
                crocodile_speeds[i] = random.uniform(crocodile_speed_min, crocodile_speed_max)
                # increase the score if the crocodile move out the screen
                score += 250
                score_text.clear()
                score_text.write(str(score),font=("Arial", 15, "bold"), align="center")
                turtle.update()

            # Check collision
            if turtle.distance(crocodiles[i]) < safe_distance_from_crocodile:
                if kick_state:
                    a = (window_width + crocodile_width)/2
                    b = random.uniform(-(river_width - crocodile_height)/2, (river_width - crocodile_height)/2)
                    crocodiles[i].goto(a, b)
                    crocodile_speeds[i] = random.uniform(crocodile_speed_min, crocodile_speed_max)
                    score += 250

                else:
                    gameover("Oh!! you lost the battle to the evil!!!")
                    return
    
    #For every stone 
    if stone_state:
        for i in range(stone_number):
            stones[i].forward(stone_speed[i])
            #move the stone downward

            #If stone touch the botton, kick it back to the top
            if stones[i].ycor() < -(window_width+crocodile_width)/2:
                y = 325
                x = random.uniform(-325, 325)
                stones[i].goto(x, y)
                stone_speed[i] = random.uniform(10, 25)

            #If the turtle touch the stone, stop the drage function for 3 second by induce another function
            if turtle.distance(stones[i]) < 30:
                if not kick_state and not stuned:
                    stuned = True
                    turtle.shape(user + ".gif")
                    #chage the turtle animation to 'stand'
                    turtle.ondrag(None)
                    turtle.ontimer(stone_stun, 3000)

                #If whirlwind Kick is turned on, kill the touching stone
                elif user == "dennis" and kick_state:
                    b = 325
                    a = random.uniform(-325, 325)
                    stones[i].goto(a, b)
                    stone_speed[i] = random.uniform(10, 25)                
                    score += 450 
                


    #For davis energy blast
    for ball in david_ball :
        if ball.xcor() <= (window_width+crocodile_width)/2:
            ball.forward(15)
            #Move the ball
                
            #Check if the skull touch the ball, if so, kick the skull back to the right
            for j in range(crocodile_number):
                if ball.distance(crocodiles[j]) < 25:
                    a = (window_width + crocodile_width)/2
                    b = random.uniform(-(river_width - crocodile_height)/2, (river_width - crocodile_height)/2)
                    crocodiles[j].goto(a, b)
                    crocodile_speeds[j] = random.uniform(crocodile_speed_min, crocodile_speed_max)                
                    score += 250                   
                    ball.hideturtle()
                    david_ball.remove(ball)
                    ball.goto(-9999,9999)
                    ball_order -= 1
                    break

            #If the ball touch the stone, remove the stone and add score
            for i in range(stone_number):
                if ball.distance(stones[i]) < 25:
                    b = 325
                    a = random.uniform(-325, 325)
                    stones[i].goto(a, b)
                    stone_speed[i] = random.uniform(10, 25)                
                    score += 450                   
                    ball.hideturtle()
                    david_ball.remove(ball)
                    ball.goto(-9999,9999)
                    ball_order -= 1
                    break
            
        #If the ball move out of screen, thrown it away
        elif ball.xcor() > (window_width+crocodile_width)/2:
                david_ball.remove(ball)
                ball.hideturtle()
                ball.goto(-9999,-9999)
                ball_order -= 1

    #Dont touch the Julian!!!
    if turtle.distance(julian) < safe_distance_from_crocodile + 10 and not bomb_stage:
            gameover("Oh!! you are killed by Julian!!!")
            return
    # survival score

    if bomb_stage:
        score += 0
    else:
        score += 1
    score_text.clear()
    score_text.write(str(score),font=("Arial", 15, "bold"), align="center")
    
    if passed:
        gameover("You Win!!")
        return
    
    turtle.update() 
    # Schedule an update in 'update_interval' milliseconds
    turtle.ontimer(updatescreen, update_interval)


'''

-----------Some function for spinner control---------------

'''
def decrease_speed(x, y):
    global crocodile_speed_max
    if crocodile_speed_max > crocodile_speed_min + 1 :
        crocodile_speed_max = crocodile_speed_max - 1
        speed_text.clear()
        speed_text.write(str(crocodile_speed_max), align="center")
        turtle.update()
        
def increase_speed(x, y):
    global crocodile_speed_max
    if crocodile_speed_max < 39 :
        crocodile_speed_max = crocodile_speed_max + 1
        speed_text.clear()
        speed_text.write(str(crocodile_speed_max), align="center")
        turtle.update()

def decrease_number(x, y):
    global crocodile_number
    if crocodile_number > 2 :
        crocodile_number = crocodile_number - 1
        number_text.clear()
        number_text.write(str(crocodile_number), align="center")
        turtle.update()

def increase_number(x, y):
    global crocodile_number
    if crocodile_number < 39 :
        crocodile_number = crocodile_number + 1
        number_text.clear()
        number_text.write(str(crocodile_number), align="center")
        turtle.update()

def decrease_width(x, y):
    global minimum_width
    if minimum_width > 50 :
        minimum_width = minimum_width - 10
        width_text.clear()
        width_text.write(str(minimum_width), align="center")
        turtle.update()

def increase_width(x, y):
    global minimum_width
    if minimum_width < 250 :
        minimum_width = minimum_width + 10
        width_text.clear()
        width_text.write(str(minimum_width), align="center")
        turtle.update()


'''

----------------Game control ----------------

'''

def instrution():
    label_turtle.color("cyan")
    label_turtle.goto(0, 240)
    label_turtle.write("Welcome to the 'Little Fighter Escape' ", font=("Consolas", 15, "bold"), align="center")
    label_turtle.goto(0, 215)
    label_turtle.write("Davis and Dennis is now encompassed by the evil Julian at the dark castle", font=("Consolas", 10, "bold"), align="center")
    label_turtle.goto(0, 200)
    label_turtle.write("Your mission is to drag one of them with your mouse", font=("Consolas", 10, "bold"), align="center")
    label_turtle.goto(0, 185)
    label_turtle.write("Avoid touching the skull and the border", font=("Consolas", 10, "bold"), align="center")
    label_turtle.goto(0, 170)
    label_turtle.write("And survive as long as you can", font=("Consolas", 10, "bold"), align="center")
    label_turtle.goto(0, 155)
    label_turtle.write("You can adjust the difficulty by using the spinner control", font=("Consolas", 10, "bold"), align="center")
    label_turtle.goto(0, 140)
    label_turtle.write("Press the 'start' button to began. Good luck!!!", font=("Consolas", 10, "bold"), align="center")
    label_turtle.color("white")
    
def counter():
    global time_survived
    global stone_state
    global stone_number
    if state:
        time_survived += 1
        turtle.ontimer(counter, 1000)
        time_text.clear()
        time_text.write(str(time_survived),font=("Arial", 15, "bold"), align="center")
        turtle.update()
        #Turn on the falling of stone 
        if time_survived == 30 and not bomb_stage:
            stone_state = True
            passed = True
        elif time_survived%30 == 0 and time_survived > 30 and stone_number < 50:
                stone_number += 5           
        elif time_survived%295 == 0 and time_survived > 100:
            if not bomb_state:
                bg_sound.play() #Looping the bg music
        

def start_game(x, y):
    global kill_number
    global invulnerable_number
    global river_width_update 
    global state
    global turtle_number 
    global ball_order
    global davis_ball_order
    global ball_state
    global david_ball
    global davis_ball_count 
    global kick_count
    global stuned
    global stone_state
    global ability_number
    global davis_number
    global kick_state
    global stone_number
    global bomb_stage

    turtle.bgpic('bg.gif')
    davis_ball_count = 30
    kick_count = 0
    ball_order = 0
    davis_ball_order = 0
    ability_number = 0
    davis_number = 0
    kick_count = 0
    ball_state = False
    kick_state = False
    stone_state = False
    bomb_stage = False
    stone_number = 10
    stuned = False
    david_ball = []
    bg1_sound.stop()
    for i in range(crocodile_number):
        crocodile_speeds[i] = random.uniform(crocodile_speed_min, crocodile_speed_max)
    for i in range(stone_number):
        stone_speed.append(random.uniform(10, 25))
    rank_button.hideturtle()
    rank_button.clear()
    start_button.hideturtle()
    kill_text.clear()
    invulnerable_text.clear()
    davis_ball_button.clear()
    dennis_kick_button.clear()
    label_turtle.clear()
    arrow_left.hideturtle()
    arrow_right.hideturtle()
    width_arrow_right.clear()
    width_arrow_right.hideturtle()
    width_arrow_left.clear()
    width_arrow_left.hideturtle()
    number_arrow_left.hideturtle()
    number_arrow_right.hideturtle()
    speed_text.clear()
    number_text.clear()
    start_button.clear()
    user_label.clear()
    user_change_button.clear()
    width_text.clear()
    user_change_button.hideturtle()
    stage_2_button.hideturtle()
    stage_2_button.clear()
    turtle.update()

    label_turtle3.goto(0, 180)
    label_turtle3.write("3" , font=("Arial", 25, "bold"), align="center")
    time.sleep(1)
    label_turtle3.clear()
    turtle.update()
    label_turtle3.write("2" , font=("Arial", 25, "bold"), align="center")
    time.sleep(1)
    label_turtle3.clear()
    turtle.update()
    label_turtle3.write("1" , font=("Arial", 25, "bold"), align="center")
    time.sleep(1)
    label_turtle3.clear()
    turtle.update()

    turtle_number = 0
    state = True
    julian.showturtle()
    river_width_update = 0.3
    kill_number = 3
    invulnerable_number = 3
    bg_sound.play()
    turtle.ontimer(updatescreen, update_interval)
    turtle.ontimer(counter, 1000)
    turtle.ontimer(davis_ball_counting, 5000)
    
    kill_text.goto(-52,-276)
    kill_text.write(str(kill_number)+")",font=("Arial", 10, "bold"), align="center")
    invulnerable_text.goto(13,-291)
    invulnerable_text.write(str(invulnerable_number)+")",font=("Arial", 10, "bold"), align="center")
    if user == "davis":
        davis_ball_button.goto(-30, -260)
        davis_ball_button.write("(Remaining: " + str(davis_ball_count)+")", font=("Arial", 10, "bold"), align="center")
    elif user == "dennis":
        dennis_kick_button.write("(Cool Down: " + str(kick_count) + ")",font=("Arial", 10, "bold") ,align="center")
    
    label_turtle4.color("black")
    label_turtle4.goto(-290,-260)
    label_turtle4.write("Press 'a' to use character's ability  ",font=("Agency FB", 10, "bold"))
    label_turtle4.goto(-290,-275)
    label_turtle4.write('Press "q" to kill all skull (Remaining:',font=("Agency FB", 10, "bold"))
    label_turtle4.goto(-290,-290)
    label_turtle4.write('Press "w" to become invulnerable (Remaining:',font=("Agency FB", 10, "bold"))
    
    turtle.ondrag(moveturtle)
    turtle.update()
    turtle.listen()

    

def retry_game(x, y):
    global score
    global time_survived
    global river_width
    global Gauss
    global user
    return_button.clear()
    return_button.hideturtle()
    label_turtle4.clear()
    label_turtle5.clear()
    davis_ball_button.clear()
    dennis_kick_button.clear()
    stop_text.clear()
    
    turtle.bgpic('bg.gif')
    user = "davis"
    user_label.goto(0,-40)
    user_label.write('Davis: A gay guy who is the most toxic boy in the entire world. Ability: Energy Blast ',font=("Arial", 10, "bold") ,align="center")
    user_label.goto(20,-80)
    user_label.write('Davis ',font=("Arial", 10, "bold") ,align="center")
    turtle.shape(user + ".gif")

    julian.hideturtle()
    turtle.goto(0, 0)
    river_width = 300
    rank_button.showturtle()
    rank_button.goto(-150, -25)
    rank_button.color("black")
    rank_button.begin_fill()
    for _ in range(2):
        rank_button.forward(80)
        rank_button.left(90)
        rank_button.forward(25)
        rank_button.left(90)
    rank_button.end_fill()
    rank_button.color("white")
    rank_button.goto(-110, 30)
    rank_button.write("Ranking", font=("Arial", 10, "bold"), align="center")
    rank_button.goto(-110, 38)
    rank_button.color("")
    rank_button.shape("square")

    user_change_button.showturtle()
    user_change_button.goto(40, -85)
    user_change_button.color("black")
    user_change_button.begin_fill()
    for _ in range(2):
        user_change_button.forward(80)
        user_change_button.left(90)
        user_change_button.forward(25)
        user_change_button.left(90)
    user_change_button.end_fill()
    user_change_button.color("white")
    user_change_button.goto(80, -80)
    user_change_button.write("Change", font=("Arial", 10, "bold"), align="center")
    user_change_button.goto(80, -72)
    user_change_button.color("")
    user_change_button.shape("square")
    
    for i in range(crocodile_number):
        x = (window_width + crocodile_width)/2
        y = random.uniform(-(river_width - crocodile_height)/2, (river_width - crocodile_height)/2)
        crocodiles[i].goto(x, y)
    for i in range(stone_number):
        x = random.uniform(-325, 325)
        y = 325
        stones[i].goto(x, y)

    score = 0
    time_survived = 0
    upper_border.sety((border_height + river_width) / 2)
    lower_border.sety(-(border_height + river_width) / 2)

    if Gauss:
        bg1_sound.play()
        Gauss = False
    start_button.clear()
    start_button.showturtle()
    start_button.goto(-40, 25)
    start_button.color("black")
    start_button.begin_fill()
    for _ in range(2):
        start_button.forward(80)
        start_button.left(90)
        start_button.forward(25)
        start_button.left(90)
    start_button.end_fill()
    start_button.color("white")
    start_button.goto(0, 30)
    start_button.write("Start", font=("Arial", 10, "bold"), align="center")
    start_button.goto(0, 38)
    start_button.color("")
    start_button.shape("square")
    kill_text.clear()
    invulnerable_text.clear()

    stage_2_button.showturtle()
    stage_2_button.goto(-40, -115)
    stage_2_button.color("black")
    stage_2_button.begin_fill()
    for _ in range(2):
        stage_2_button.forward(80)
        stage_2_button.left(90)
        stage_2_button.forward(25)
        stage_2_button.left(90)
    stage_2_button.end_fill()
    stage_2_button.color("white")
    stage_2_button.goto(0, -110)
    stage_2_button.write("Bomb mode", font=("Arial", 10, "bold"), align="center")
    stage_2_button.goto(0, -102)
    stage_2_button.shape("square")
    stage_2_button.shapesize(1.25, 4) 
    stage_2_button.color("")
    stage_2_button.onclick(stage_2_start)

    label_turtle.clear()
    label_turtle.hideturtle()
    instrution()
    label_turtle.goto(-223, 75) 
    label_turtle.write("Maximum Speed of Skull (maximum 39):", font=("Arial", 10, "bold"))
    label_turtle.goto(-165, 55)
    label_turtle.write("Number of Skull (maximum 39):", font=("Arial", 10, "bold"))
    label_turtle.goto(-165, -80)
    label_turtle.write("Change your user turtle: ", font=("Arial", 10, "bold"))
    label_turtle.goto(-116, 95)
    label_turtle.write("Minimum width of river:", font=("Arial", 10, "bold"))
    
    arrow_left.showturtle()
    arrow_right.showturtle()

    number_arrow_left.showturtle()
    number_arrow_right.showturtle()
    width_arrow_right.showturtle()
    width_arrow_left.showturtle()

    speed_text.clear()
    speed_text.write(str(crocodile_speed_max), align="center")
    
    width_text.clear()
    width_text.write(str(minimum_width), align="center")

    
    number_text.clear()
    number_text.write(str(crocodile_number), align="center")

    score_text.clear()
    score_text.write(str(score),font=("Arial", 15, "bold"), align="center")

    time_text.clear()
    time_text.write(str(time_survived),font=("Arial", 15, "bold"), align="center")

    
    retry_button.hideturtle()
    retry_button.clear()

    turtle.update()
'''

---------animation--------

'''

#character animation(not just for davis)
def davis():
    global davis_number
    if state and not ball_state and not kick_state and not stuned:
        turtle.shape(str(user)+ str(davis_number) + ".gif")
        davis_number +=1
        if davis_number == 4:
            davis_number = 0
        turtle.update()
    turtle.ontimer(davis, 250)
        

def julia():
    global julian_number
    if state:
        julian.shape("julian" + str(julian_number) + ".gif")
        julian_number +=1
        if julian_number == 5:
            julian_number = 0
        turtle.update()
    turtle.ontimer(julia, 200)


def davis_ball_ani():
    global ability_number
    global davis_number
    global state
    global ball_state
    
    if state and ball_state:
        turtle.shape("davis_" + str(ability_number) + ".gif")
        ability_number +=1
        if ability_number == 5:
            ability_number = 0
            davis_number = 0
            ball_state = False
            return
        turtle.update()
        turtle.ontimer(davis_ball_ani, 200)

def dennis_kick_ani():
    global ability_number
    global davis_number
    global state
    global kick_state

    if state and kick_state:
        kick_sound.play()
        turtle.shape("dennis_" + str(ability_number) + ".gif")
        ability_number +=1
        if ability_number == 4:
            ability_number = 0
            if not kick_state:
                davis_number = 0
                return
        turtle.update()
        turtle.ontimer(dennis_kick_ani, 200)

'''





----------------item and ability------------------






'''

def kill_crocodile():
    global kill_number
    global score
    global item_state
    if kill_number > 0 and item_state and state and not bomb_stage:
        kill_sound.play()
        item_state = False
        label_turtle3.goto(0,200)
        label_turtle3.write("You kill all the skull!!", font=("Times", 20, "italic"), align="center")
        for i in range(crocodile_number):
            x = (window_width + crocodile_width)/2
            y = random.uniform(-(river_width - crocodile_height)/2, (river_width - crocodile_height)/2)
            crocodiles[i].goto(x, y)
        score += crocodile_number*250
        kill_number = kill_number - 1
        kill_text.clear()
        kill_text.write(str(kill_number)+")", font=("Arial", 10, "bold"), align="center")
        turtle.update()
        turtle.ontimer(clearwaterbay, 5000)

def clearwaterbay():
    global item_state
    label_turtle3.clear()
    item_state = True
    
def invulnerable():
    global invulnerable_number
    global safe_distance_from_crocodile
    global item_state
    if invulnerable_number > 0 and item_state and state and not bomb_stage:
        invulnerable_sound.play()
        item_state = False
        label_turtle3.goto(0,200)
        label_turtle3.write("You become invulnerable for 5 seconds!", font=("Times", 20, "italic"), align="center")
        safe_distance_from_crocodile = -15
        invulnerable_number -= 1
        turtle.ontimer(invulnerable2, 5000)
        invulnerable_text.clear()
        invulnerable_text.write(str(invulnerable_number)+")", font=("Arial", 10, "bold"), align="center")
        turtle.update()
        
def invulnerable2():
    global invulnerable_number
    global safe_distance_from_crocodile
    global item_state
    label_turtle3.clear()
    safe_distance_from_crocodile = 25
    item_state = True

def check_rank(x, y):
    start_button.hideturtle()
    rank_button.hideturtle()
    rank_button.clear()
    label_turtle.clear()
    arrow_left.hideturtle()
    arrow_right.hideturtle()
    number_arrow_left.hideturtle()
    number_arrow_right.hideturtle()
    speed_text.clear()
    number_text.clear()
    start_button.clear()
    turtle.update()
    user_label.clear()
    user_change_button.clear()
    user_change_button.hideturtle()
    width_arrow_right.hideturtle()
    width_arrow_left.hideturtle()
    width_text.clear()
    stage_2_button.clear()
    stage_2_button.hideturtle()

    label_turtle.goto(0, 240)
    label_turtle.color("green")
    label_turtle.write("Ranking", font=("Times", 25, "bold"), align="center")
    #Open the file and read the ranking
    filename = 'ranking.txt'
    myfile = open(filename, 'r')
    scorer = 0
    del rank[0:len(rank)] #clear the list
    for line in myfile:
        scorer = line.rstrip().split("\t")
        scorer[0] = int(scorer[0])
        rank.append(scorer[0])
    myfile.close()
    #Write out the ranking
    for i in range(1, len(rank)+1):
        label_turtle.goto(-140, 210-30*i)
        label_turtle.write(str(i) + "\t\t\t" + str(rank[i - 1]), font=("Times", 15, "bold"))
    turtle.update()

    #Create the menu button
    return_button.showturtle()
    return_button.up()
    return_button.goto(200, -180)
    return_button.color("black")
    return_button.begin_fill()
    for _ in range(2):
        return_button.forward(80)
        return_button.left(90)
        return_button.forward(25)
        return_button.left(90)
    return_button.end_fill()
    return_button.color("white")
    return_button.goto(240, -175)
    return_button.write("Menu", font=("Arial", 10, "bold"), align="center")
    return_button.goto(240, -167)
    return_button.shape("square")
    return_button.shapesize(1.25, 4) 
    return_button.color("")
    return_button.onclick(retry_game)

    turtle.update()

def user_ability():
    global ball_state
    global ball_order
    global davis_ball_count
    global kick_state
    global kick_count

    if not stuned and not bomb_stage:
        if user == "dennis":
            if state and not kick_state and kick_count == 0:
                kick_state = True            
                kick_count = 25
                dennis_kick_ani()
                dennis_kick_cd()
                turtle.ontimer(dennis_kick2, 10000)
        elif user == "davis":
            if state and ball_order < 10 and davis_ball_count > 0:
                davis_ball_count -= 1
                davis_ball_button.clear()
                davis_ball_button.write("(Remaining: "+str(davis_ball_count)+")", font=("Arial", 10, "bold"), align="center")
                davis_ball = turtle.Turtle()
                davis_ball.shape("davis_ball.gif")
                davis_ball.up()
                david_ball.append(davis_ball)
                ball_sound.play()
                ball_order += 1
                davis_ball.goto(turtle.xcor(), turtle.ycor())
                ball_state = True
                davis_ball_ani()

def davis_ball_counting():
    global davis_ball_count

    if state and davis_ball_count < 100 and user == "davis" :
        davis_ball_count += 1
        davis_ball_button.clear()
        davis_ball_button.write("(Remaining: "+str(davis_ball_count)+")", font=("Arial", 10, "bold"), align="center")
        turtle.update()
    if state == False:
        return
    turtle.ontimer(davis_ball_counting, 5000)
        
def user_change(x, y):
    global user
    
    if user == "davis" :
        user = "dennis"
        user_label.clear()
        user_label.goto(0,-40)
        user_label.write('Dennis: A feminine guy who is desired to date with davis. Ability: Whirlwind Kick ',font=("Arial", 10, "bold") ,align="center")
        user_label.goto(20,-80)
        user_label.write('Dennis ',font=("Arial", 10, "bold") ,align="center")
    elif user == "dennis" :
        user = "davis"
        user_label.clear()
        user_label.goto(0,-40)
        user_label.write('Davis: A gay guy who is the most toxic boy in the entire world. Ability: Energy Blast ',font=("Arial", 10, "bold") ,align="center")
        user_label.goto(20,-80)
        user_label.write('Davis ',font=("Arial", 10, "bold") ,align="center")
    turtle.shape(user + ".gif")
    turtle.update()
'''

-----------------thrown code---------------------

def stun2():
    global stun
    global item_state 

    label_turtle3.clear()
    stun = False
    item_state = True
    
def stun():
    global stun
    global item_state
    
    if state and item_state:
            label_turtle3.goto(0,200)
            label_turtle3.write("You stun all the skull for 5 second!!", font=("Times", 20, "italic"), align="center")
            stun = True
            item_state = False
            turtle.ontimer(stun2, 5000)

---------------end of thrown code-------------------
'''
def dennis_kick2():
    global kick_state

    kick_state = False


def dennis_kick_cd():
    global kick_count

    if kick_count > 0 and state:
        kick_count -= 1
        dennis_kick_button.clear()
        dennis_kick_button.write("(Cool Down: " + str(kick_count) + ")",font=("Arial", 10, "bold") ,align="center")
        turtle.update()
        if kick_count == 0:
            return
        else:
            turtle.ontimer(dennis_kick_cd, 1000)

        
def stone_stun():
    global davis_number 
    global stuned
    turtle.ondrag(moveturtle)
    davis_number = 0
    stuned = False
    
"""

---------stage 2---------

"""
'''    
def stage_1_finish():
    global ball_order
    global state
    global stone_state
    global kick_state
    global stun_state
        
    bg_sound.stop()
    lost_sound.play()

    label_turtle.goto(0, 150)
    label_turtle.write("You have passed Stage 1!!! ", align="center", font=("Arial", 24, "normal"))
    turtle.ondrag(None)
    state = False
    stone_state = False
    kick_state = False
    turtle.shape(user+".gif")
    stun_state = False

    for i in range(len(david_ball)):
        david_ball[i].hideturtle()
        david_ball[i].goto(9999,9999)
    ball_order = 0

    for i in range(crocodile_number):
        a = (window_width + crocodile_width)/2
        b = random.uniform(-(river_width - crocodile_height)/2, (river_width - crocodile_height)/2)
        crocodiles[j].goto(a, b)
        crocodile_speeds[j] = random.uniform(crocodile_speed_min, crocodile_speed_max)                                    

    for i in range(stone_number):
        b = 325
        a = random.uniform(-325, 325)
        stones[i].goto(a, b)
        tone_speed[i] = random.uniform(10, 25)
    turtle.update()

    time.sleep(5)
    
    label_turtle.clear()
    label_turtle.goto(0, 150)
    label_turtle.write("Stage 2 ", align="center", font=("Arial", 24, "normal"))
    label_turtle.goto(0, 100)
    label_turtle.write("Bomb will randomly appear in the screen, be careful!!", align="center", font=("Arial", 24, "normal"))
    state = True
    turtle.ondrag(moveturtle)
'''

def bomb_create():
    bomb = turtle.Turtle()
    bomb.up()
    bomb.shape("bomb_3.gif")
    x = random.uniform(-280,280)
    y = random.uniform(-280,280)
    bomb.goto(x,y)
    bomb_number.append(3)
    bomber.append(bomb)
    
def bomb_ani():
    global bomb_number
    if not state:
        return
    if not stopped :
        for i in range(len(bomber)):
            bomb_number[i] -= 1
            if bomb_number[i] >= 0:
                bomber[i].shape("bomb_"+str(bomb_number[i])+".gif")        
            if bomb_number[i] == 0:
                explode(bomber[i])
                dead_bomber.append(bomber[i])
    turtle.update()
    turtle.ontimer(bomb_ani, 1000)

def removal():
    global dead_bomber
    if not state:
        return
    for i in range(len(dead_bomber)):
        dead_bomber[i].goto(9999, -9999)
        dead_bomber[i].hideturtle()
    dead_bomber = []
    turtle.ontimer(removal, 1000)
    
    
def explode(thing):
    global state
    if turtle.distance(thing) < 90 and state and not stopped:
        gameover("You become a piece of shit!!!")
        for i in range(len(bomber)):
            bomber[i].goto(9999,-9999)
            bomber[i].hideturtle()        
        for i in range(len(dead_bomber)):
            dead_bomber[i].goto(9999, -9999)
            dead_bomber[i].hideturtle()
        turtle.update()
        state = False

            
        
def stage_2_update():
    if not state:
        return
    if not stopped:
        for _ in range(random.randint(3, 7)):
            bomb_create()
    turtle.ontimer(stage_2_update, 1000)

def stage_2_start(x, y):
    global kill_number
    global invulnerable_number
    global river_width_update 
    global state
    global turtle_number 
    global ball_order
    global davis_ball_order
    global ball_state
    global david_ball
    global davis_ball_count 
    global kick_count
    global stuned
    global stone_state
    global ability_number
    global davis_number
    global kick_state
    global stone_number
    global bomb_stage
    global bomber
    global bomb_number
    global dead_bomber
    global stopped
    global stop_number

    turtle.bgpic('bg2.gif')
    label_turtle4.clear()
    label_turtle5.clear()
    bomber = []
    bomb_number = []
    dead_bomber = []
    upper_border.sety(border_height + river_width)
    lower_border.sety(-(border_height + river_width))
    davis_ball_count = 30
    stop_number = 0
    stopped = False
    kick_count = 0
    ball_order = 0
    davis_ball_order = 0
    ability_number = 0
    davis_number = 0
    kick_count = 0
    ball_state = False
    kick_state = False
    stone_state = True
    stone_number = 30
    stuned = False
    david_ball = []
    bg1_sound.stop()
    rank_button.hideturtle()
    rank_button.clear()
    start_button.hideturtle()
    kill_text.clear()
    invulnerable_text.clear()
    davis_ball_button.clear()
    dennis_kick_button.clear()
    label_turtle.clear()
    arrow_left.hideturtle()
    arrow_right.hideturtle()
    width_arrow_right.clear()
    width_arrow_right.hideturtle()
    width_arrow_left.clear()
    width_arrow_left.hideturtle()
    number_arrow_left.hideturtle()
    number_arrow_right.hideturtle()
    speed_text.clear()
    number_text.clear()
    start_button.clear()
    user_label.clear()
    user_change_button.clear()
    width_text.clear()
    user_change_button.hideturtle()
    stage_2_button.hideturtle()
    stage_2_button.clear()
    turtle.update()

    label_turtle3.goto(0, 180)
    label_turtle3.write("3" , font=("Arial", 25, "bold"), align="center")
    time.sleep(1)
    label_turtle3.clear()
    turtle.update()
    label_turtle3.write("2" , font=("Arial", 25, "bold"), align="center")
    time.sleep(1)
    label_turtle3.clear()
    turtle.update()
    label_turtle3.write("1" , font=("Arial", 25, "bold"), align="center")
    time.sleep(1)
    label_turtle3.clear()
    turtle.update()

    bg2_sound.play()
    turtle_number = 0
    state = True
    julian.showturtle()
    river_width_update = 0.3
    kill_number = 5
    stop_number = 3
    turtle.ontimer(stage_2_update, 500)
    turtle.ontimer(counter, 1000)
    turtle.ontimer(bomb_ani, 1000)
    turtle.ontimer(removal, 1000)
    turtle.ontimer(updatescreen, update_interval)
    bomb_stage = True

    label_turtle4.color("black")
    label_turtle4.goto(-290,-260)
    #label_turtle4.write("Press 'a' to use character's ability  ",font=("Agency FB", 10, "bold"))
    label_turtle4.goto(-290,-275)
    label_turtle4.write('Press "t" to stop all bomb ',font=("Agency FB", 10, "bold"))
    label_turtle4.goto(-290,-290)
    label_turtle4.write('Press "r" to explode bomb beside you',font=("Agency FB", 10, "bold"))
    kill_text.goto(0, -290)
    kill_text.write("(Remaining: " + str(kill_number)+")", font=("Arial", 10, "bold"), align="center")
    stop_text.goto(-80, -275)
    stop_text.write("(Remaining: " + str(stop_number)+")", font=("Arial", 10, "bold"), align="center")
    turtle.ondrag(moveturtle)
    turtle.update()
    turtle.listen()


'''

-----------------------------------

'''

def kill_bomb():
    global kill_number
    global score
    global item_state
    global bomber
    global bomb_number
    if kill_number > 0 and item_state and bomb_stage:
        kill_sound.play()
        item_state = False
        label_turtle3.goto(0,200)
        label_turtle3.write("You remove all the bomb!!", font=("Times", 20, "italic"), align="center")
        for i in range(len(bomber)):
            bomber[i].goto(9999,-9999)
            bomber[i].hideturtle()
        bomber = []
        bomb_number = []
        kill_number = kill_number - 1
        kill_text.clear()
        kill_text.write("(Remaining: " + str(kill_number)+")", font=("Arial", 10, "bold"), align="center")
        turtle.update()
        turtle.ontimer(clearwaterbay, 5000)

def stop_bomb():
    global stop_number
    global item_state
    global stopped
    if stop_number > 0 and item_state and bomb_stage:
        invulnerable_sound.play()
        item_state = False
        stopped = True
        label_turtle3.goto(0,200)
        label_turtle3.write("All bomb are stopped for 5 seconds!", font=("Times", 20, "italic"), align="center")
        stop_number -= 1
        turtle.ontimer(stop_bomb_2, 5000)
        stop_text.clear()
        stop_text.write("(Remaining: " + str(stop_number)+")", font=("Arial", 10, "bold"), align="center")
        turtle.update()
        
def stop_bomb_2():
    global invulnerable_number
    global stopped
    global item_state
    label_turtle3.clear()
    stopped = False
    item_state = True

   
"""
    Here is the entry point of the game
    
    First of all, we create turtles for each component
    in the game with turtle.Turtle().
    The components are:
        1. The player turtle
        2. Two big boxes used as borders of the river
        3. Ten crocodiles
    
    Then we set up the event handlers for:
        1. The ondrag handler to handle the player's control
        2. The ontimer handler to handle timer event for 
           regular screen update

    After all the components are ready, start the game
"""

turtle.setup(window_width, window_height) # Set the window size
turtle.bgcolor("DarkBlue")

# Turn off the tracer here
turtle.tracer(False)

# Create ten crocodiles
for _ in range(39):

    # Create a new turtle instance which is facing left
    crocodile = turtle.Turtle()

    # Set the shape
    crocodile.shape("crocodile.gif")

    # Rotate the crocodile
    crocodile.left(180)
    
    # Place the crocodile in the right hand side randomly
    crocodile.up()
    x = (window_width + crocodile_width) / 2
    y = random.uniform(-(river_width-crocodile_height)/2, (river_width-crocodile_height)/2)
    crocodile.goto(x, y)

    # Add the new crocodile to the list 'crocodiles'
    crocodiles.append(crocodile)

    # Generate a random speed and store it in 'crocodile_speeds'
    crocodile_speeds.append(random.uniform(crocodile_speed_min, crocodile_speed_max))


# Create the big boxes for upper border and lower border
upper_border = turtle.Turtle()
upper_border.up()
lower_border = turtle.Turtle()
lower_border.up()

# Set the shape of the borders to "square"
upper_border.shape("upper_border.gif")
lower_border.shape("lower_border.gif")


# Set the size of the borders
upper_border.shapesize(30, 40)
lower_border.shapesize(30, 40)

# Set the initial y position of the borders
upper_border.sety((border_height + river_width) / 2)
lower_border.sety(-(border_height + river_width) / 2)

for _ in range(50):
    stone = turtle.Turtle()
    stone.shape("stone.gif")
    stone.right(90)
    stone.up()
    stones.append(stone)
    stone_speed.append(random.uniform(10, 25))
    x = random.uniform(-325, 325)
    y = 325
    stone.goto(x, y)

# Prepare the player turtle
turtle.shape(str(user) + ".gif")
turtle.color("GreenYellow")
turtle.up()

# The event handler for turtle.ontimer
turtle.update() 


# It starts the main loop and starts the game


'''
-------------read rank------------
'''
rank = []
filename = 'ranking.txt'
myfile = open(filename, 'r')
scores = 0

for line in myfile:
    scores = line.rstrip().split("\t")
    scores[0] = int(scores[0])
    rank.append(scores[0])
    

myfile.close()

'''



--------------button setting--------------------




'''


retry_button = turtle.Turtle()
retry_button.hideturtle()
retry_button.color("black")
retry_button.onclick(retry_game)
retry_button.shape("square")
retry_button.shapesize(1.25, 4)
retry_button.up()

start_button = turtle.Turtle()
start_button.up()
start_button.goto(-40, 25)
start_button.color("black")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()
start_button.color("white")
start_button.goto(0, 30)
start_button.write("Start", font=("Arial", 10, "bold"), align="center")
start_button.goto(0, 38)
start_button.shape("square")
start_button.shapesize(1.25, 4) 
start_button.color("")
start_button.onclick(start_game)

label_turtle = turtle.Turtle()
label_turtle.color("white")
label_turtle.up()
label_turtle.goto(-223, 75)
label_turtle.hideturtle()
label_turtle.write("Maximum Speed of Skull (maximum 39):", font=("Arial", 10, "bold"))
label_turtle.goto(-165, 55)
label_turtle.write("Number of Skull (maximum 39):", font=("Arial", 10, "bold"))
label_turtle.goto(-116, 95)
label_turtle.write("Minimum width of river:", font=("Arial", 10, "bold"))
label_turtle.goto(-165, -80)
label_turtle.write("Change your user turtle: ", font=("Arial", 10, "bold"))

label_turtle2 = turtle.Turtle()
label_turtle2.color("white")
label_turtle2.up()
label_turtle2.hideturtle()
label_turtle2.goto(-260,275)
label_turtle2.write('Score: ',font=("Arial", 15, "bold") ,align="center")
label_turtle2.goto(210,275)
label_turtle2.write('Time: ',font=("Arial", 15, "bold") ,align="center")
label_turtle2.color("white")

label_turtle3 = turtle.Turtle()
label_turtle3.up()
label_turtle3.hideturtle()
label_turtle3.color("white")

label_turtle4 = turtle.Turtle()
label_turtle4.up()
label_turtle4.hideturtle()
label_turtle4.color("white")

label_turtle5 = turtle.Turtle()
label_turtle5.color("white")
label_turtle5.up()
label_turtle5.hideturtle()

speed_text = turtle.Turtle()
speed_text.hideturtle()
speed_text.up()
speed_text.goto(70,75)
speed_text.color("white")
speed_text.write(str(crocodile_speed_max), align="center")

arrow_left = turtle.Turtle() 
arrow_left.shape("arrow")
arrow_left.shapesize(0.5, 1)
arrow_left.up()
arrow_left.goto(50, 82)
arrow_left.color("white")
arrow_left.left(180)
arrow_left.onclick(decrease_speed)

arrow_right = turtle.Turtle() 
arrow_right.shape("arrow")
arrow_right.shapesize(0.5, 1)
arrow_right.up()
arrow_right.goto(90, 82)
arrow_right.color("white")
arrow_right.onclick(increase_speed)

number_text = turtle.Turtle()
number_text.hideturtle()
number_text.up()
number_text.goto(70,55)
number_text.color("white")
number_text.write(str(crocodile_number), align="center")

score_text = turtle.Turtle()
score_text.hideturtle()
score_text.up()
score_text.goto(-205,275)
score_text.color("white")
score_text.write(str(score),font=("Arial", 15, "bold"), align="center")

time_text = turtle.Turtle()
time_text.hideturtle()
time_text.up()
time_text.goto(260,275)
time_text.color("white")
time_text.write(str(time_survived),font=("Arial", 15, "bold"), align="center")

number_arrow_left = turtle.Turtle() 
number_arrow_left.shape("arrow")
number_arrow_left.shapesize(0.5, 1)
number_arrow_left.up()
number_arrow_left.goto(50, 62)
number_arrow_left.color("white")
number_arrow_left.left(180)
number_arrow_left.onclick(decrease_number)

number_arrow_right = turtle.Turtle() 
number_arrow_right.shape("arrow")
number_arrow_right.shapesize(0.5, 1)
number_arrow_right.up()
number_arrow_right.goto(90, 62)
number_arrow_right.color("white")
number_arrow_right.onclick(increase_number)

kill_text = turtle.Turtle()
kill_text.hideturtle()
kill_text.up()
kill_text.goto(-200,240)
kill_text.color("black")

stop_text = turtle.Turtle()
stop_text.hideturtle()
stop_text.up()
stop_text.goto(-20,-275)
stop_text.color("black")

invulnerable_text = turtle.Turtle()
invulnerable_text.hideturtle()
invulnerable_text.up()
invulnerable_text.goto(-200,215)
invulnerable_text.color("black")

invulnerable_text = turtle.Turtle()
invulnerable_text.hideturtle()
invulnerable_text.up()
invulnerable_text.goto(-200,215)
invulnerable_text.color("black")

julian = turtle.Turtle()
julian.up()
julian.shape("julian0.gif")
julian.goto(270,0)
julian.hideturtle()

rank_button = turtle.Turtle()
rank_button.up()
rank_button.goto(-150, 25)
rank_button.color("black")
rank_button.begin_fill()
for _ in range(2):
    rank_button.forward(80)
    rank_button.left(90)
    rank_button.forward(25)
    rank_button.left(90)
rank_button.end_fill()
rank_button.color("white")
rank_button.goto(-110, 30)
rank_button.write("Ranking", font=("Arial", 10, "bold"), align="center")
rank_button.goto(-110, 38)
rank_button.shape("square")
rank_button.shapesize(1.25, 4) 
rank_button.color("")
rank_button.onclick(check_rank)

davis_ball_button = turtle.Turtle()
davis_ball_button.hideturtle()
davis_ball_button.up()
davis_ball_button.goto(-80,-260)
davis_ball_button.color("black")

user_label = turtle.Turtle()
user_label.color("green")
user_label.up()
user_label.hideturtle()
user_label.goto(0,-40)
user_label.write('Davis: A gay guy who is the most toxic boy in the entire world. Ability: Energy Blast ',font=("Arial", 10, "bold") ,align="center")
user_label.goto(20,-80)
user_label.write('Davis ',font=("Arial", 10, "bold") ,align="center")

user_change_button = turtle.Turtle()
user_change_button.up()
user_change_button.goto(40, -85)
user_change_button.color("black")
user_change_button.begin_fill()
for _ in range(2):
    user_change_button.forward(80)
    user_change_button.left(90)
    user_change_button.forward(25)
    user_change_button.left(90)
user_change_button.end_fill()
user_change_button.color("white")
user_change_button.goto(80, -80)
user_change_button.write("Change", font=("Arial", 10, "bold"), align="center")
user_change_button.goto(80, -72)
user_change_button.shape("square")
user_change_button.shapesize(1.25, 4) 
user_change_button.color("")
user_change_button.onclick(user_change)

dennis_kick_button = turtle.Turtle()
dennis_kick_button.hideturtle()
dennis_kick_button.up()
dennis_kick_button.goto(-30,-260)
dennis_kick_button.color("black")

width_arrow_left = turtle.Turtle() 
width_arrow_left.shape("arrow")
width_arrow_left.shapesize(0.5, 1)
width_arrow_left.up()
width_arrow_left.goto(50, 102)
width_arrow_left.color("white")
width_arrow_left.left(180)
width_arrow_left.onclick(decrease_width)

width_arrow_right = turtle.Turtle() 
width_arrow_right.shape("arrow")
width_arrow_right.shapesize(0.5, 1)
width_arrow_right.up()
width_arrow_right.goto(90, 102)
width_arrow_right.color("white")
width_arrow_right.onclick(increase_width)

width_text = turtle.Turtle()
width_text.hideturtle()
width_text.up()
width_text.goto(70,95)
width_text.color("white")
width_text.write(str(minimum_width), align="center")

stage_2_button = turtle.Turtle()
stage_2_button.up()
stage_2_button.goto(-40, -115)
stage_2_button.color("black")
stage_2_button.begin_fill()
for _ in range(2):
    stage_2_button.forward(80)
    stage_2_button.left(90)
    stage_2_button.forward(25)
    stage_2_button.left(90)
stage_2_button.end_fill()
stage_2_button.color("white")
stage_2_button.goto(0, -110)
stage_2_button.write("Bomb mode", font=("Arial", 10, "bold"), align="center")
stage_2_button.goto(0, -102)
stage_2_button.shape("square")
stage_2_button.shapesize(1.25, 4) 
stage_2_button.color("")
stage_2_button.onclick(stage_2_start)


'''





-----------button setting ended-----------






'''




        
instrution()
turtle.onkeyrelease(kill_crocodile, 'q')
turtle.onkeyrelease(invulnerable, 'w')
turtle.onkeyrelease(user_ability, 'a')
turtle.onkeyrelease(kill_bomb, 'r')
turtle.onkeyrelease(stop_bomb, 't')
davis()    
julia()

davis_ball_counting()
bg1_sound.play()

# Start the main loop, start the game
turtle.update()
turtle.done()



