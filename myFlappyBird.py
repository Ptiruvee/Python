'''
Created on Jun 21, 2014

@author: pratyushatiruveedhula
'''
from Tkinter import *
import Tkinter
import random
import pickle
from operator import itemgetter
        
def jumpAnimation():
    canvas.move("player", 0, -canvas.data.playerSpeed)
    canvas.data.playerPos[1] -= canvas.data.playerSpeed 
    canvas.data.playerPos[3] -= canvas.data.playerSpeed 
    canvas.data.playerSpeed -= 0.09
    canvas.data.jumpCount += 3
    if canvas.data.jumpCount >= 100:
        canvas.data.playerJump = False
    if canvas.data.playerJump:
        canvas.after(10, jumpAnimation)
    
def printHighScores():
    global highScores
    highScores.append((canvas.data.score))
    highScores = sorted(highScores,reverse=True)[:5]
    highscore_id = canvas.create_text((width / 2)+10, (height / 2)+20)
    canvas.insert(highscore_id,0, "HighScores \n" + str(highScores))
    with open('highscores.txt', 'wb') as f:
        pickle.dump(highScores, f)
            
def gameOver():
    global pipe_bottom ,highScores
    canvas.delete("rect")
    canvas.delete("player")
    game_overid = canvas.create_text(width / 2, height / 2)
    canvas.insert(game_overid, 0, "Game Over! Your score was " + str(canvas.data.score) + " pipes!")
    canvas.data.pipeSpeed = 0
    canvas.data.pipe_pos = [width + 50, 0, width + 100, height]
    pipe_bottom = canvas.data.pipe_pos
    printHighScores()

def drawPipe():
    canvas.create_rectangle(list(canvas.data.pipe_pos), fill = "green", tag = "rect", outline = "black")
    canvas.create_rectangle(list(pipe_bottom), fill = "green", tag = "rect", outline = "black")
    if canvas.data.pipe_pos[2] <= -5:
        canvas.data.score += 1
        canvas.itemconfig(canvas.data.scoreId, text = "Score: " + str(canvas.data.score)) 
        generatePipes()
    canvas.after(1000, drawPipe)
    
def generatePipes():
    global pipe_bottom
    pipe_hole = random.randrange(150, height - 150)
    canvas.data.pipe_pos = [width - 50, 0, width, pipe_hole]
    pipe_bottom = [width - 50, canvas.data.pipe_pos[3] + 135, width, height]
    drawPipe()

def checkHits():
    global coun
    if not canvas.data.isGameOver:
        if canvas.data.playerPos[0] <= canvas.data.pipe_pos[2] and canvas.data.playerPos[2] >= canvas.data.pipe_pos[0] and canvas.data.playerPos[1] <= canvas.data.pipe_pos[3] and canvas.data.playerPos[3] >= canvas.data.pipe_pos[1]:
            canvas.data.isGameOver = True
            gameOver()
        if canvas.data.playerPos[0] <= pipe_bottom[2] and canvas.data.playerPos[2] >= pipe_bottom[0] and canvas.data.playerPos[3] <= pipe_bottom[3] and canvas.data.playerPos[3] >= pipe_bottom[1]:
            canvas.data.isGameOver = True
            gameOver()
        if canvas.data.playerPos[3] >= height + 5:
            canvas.data.isGameOver = True
            gameOver()
        canvas.after(10, checkHits)

def animate():
    canvas.move("rect", -canvas.data.pipeSpeed, 0)
    pipe_bottom[0] -= canvas.data.pipeSpeed
    pipe_bottom[2] -= canvas.data.pipeSpeed
    canvas.data.pipe_pos[0] -= canvas.data.pipeSpeed
    canvas.data.pipe_pos[2] -= canvas.data.pipeSpeed
    if canvas.data.playerJump == False:
        canvas.move("player", 0, canvas.data.playerSpeed)
        canvas.data.playerPos[1] += canvas.data.playerSpeed
        canvas.data.playerPos[3] += canvas.data.playerSpeed
        canvas.data.playerSpeed += 0.15
    canvas.after(10, animate)

def jump(press):
    canvas.data.playerJump = True
    canvas.data.playerSpeed = 3
    canvas.data.jumpCount = 0
    jumpAnimation()

def changeLevel():
    speed = 4
    if not canvas.data.isGameOver:
        levelCount = canvas.data.score/5
        canvas.data.level = levelCount
        speed = speed + levelCount
        canvas.data.pipeSpeed = speed
        canvas.itemconfig(canvas.data.levelId, text = "Level: " + str(canvas.data.level))
    canvas.after(2000,changeLevel)
    
def callback():
    canvas.data.setMode = "Day"
    
def callback1():
    canvas.data.setMode = "Night"
    
def redrawAll(canvas):
    canvas.delete(ALL)
   # canvas.data.dayButton.destroy()
   # canvas.data.nightButton.destroy()
   # canvas.data.bird1Button.destroy()
   # canvas.data.bird2Button.destroy()
    init()
    generatePipes()
    animate()
    checkHits()
    changeLevel()

def keyPressed(event):
    canvas = event.widget
    if event.keysym == 'Return': 
        canvas.data.setMode = canvas.data.mode.get()
        canvas.data.setBird = canvas.data.birdChoice.get()
        redrawAll(canvas)
    if event.keysym =="Left":
        canvas.data.setMode = "Night"
        print("Selected Left")
    if event.keysym =="Right":
        canvas.data.setMode = "Day"
        print("Selected Right")
    if event.keysym == "space":
        print("Game paused")
        canvas.data.pause = True
       
def init():
    if canvas.data.setMode == "Night": 
        canvas.create_image(300,500, image=canvas.data.night, anchor='se')
    else:      
        canvas.create_image(300,500, image=canvas.data.day, anchor='se')
    canvas.data.pipeSpeed = 5.0
    canvas.data.playerJump = False
    canvas.data.score = 0
    canvas.data.level = 0
    canvas.data.playerPos = [20, height / 2, 40, height / 2 + 20]
    #canvas.create_arc(canvas.data.playerPos, start = 35, extent =300, fill = "yellow", tag = "player")
    if canvas.data.setBird == "bird1":
        canvas.create_image(20,height/2, image = canvas.data.bird1, anchor = 'center',tag = "player")
    else:
        canvas.create_image(20,height/2, image = canvas.data.bird2, anchor = 'center',tag = "player")
    canvas.data.jumpCount = 0
    canvas.data.playerSpeed = 1
    canvas.bind("<Button-1>", jump)
    canvas.data.scoreId = canvas.create_text(40, 20)
    canvas.insert(canvas.data.scoreId, 0, "Score: " + str(canvas.data.score))
    canvas.data.levelId = canvas.create_text(40, 40)
    canvas.insert(canvas.data.levelId, 0, "Level: " + str(canvas.data.level))
    canvas.data.isGameOver = False
        
def run():
    root = Tk()
    global width
    global height
    global canvas
    width = 300
    height = 500
    #sky_color = '#%02x%02x%02x' % (108, 177, 218)
    canvas = Canvas(root, width = width, height = height, bg = "white")    
    canvas.pack()
    root.title("Flappy Bird")
    
    
    delay = 5000
    canvas.after(delay, run, canvas)
    
    class Struct: pass
    canvas.data = Struct()
    canvas.data.bird = Tkinter.PhotoImage(file = './bird1.gif')
    canvas.data.night = Tkinter.PhotoImage(file = './night-png.gif')
    canvas.data.day = Tkinter.PhotoImage(file = './day-png.gif')
        
    canvas.data.welcome_id = canvas.create_text(width / 2, height / 2, tag="welcome", justify ="center")
    canvas.insert(canvas.data.welcome_id, 0, "Welcome! \n Choose the game options below \n Press Enter key to Start game \n Press mouse button to levitate!")  
    v = StringVar()
    v.set("Day")
    b = StringVar()
    b.set("bird1")
    canvas.focus_set()
   
    canvas.data.bird1 = Tkinter.PhotoImage(file='bird1.gif')     
    canvas.data.bird2 = Tkinter.PhotoImage(file='bird2.gif')

    canvas.data.bird1Button = Radiobutton(canvas, text="Bird1", image = canvas.data.bird1, variable=b, value="bird1")  
    canvas.data.bird2Button = Radiobutton(canvas, text="Bird2", image = canvas.data.bird2, variable=b, value="bird2")  
    
    canvas.data.nightButton = Radiobutton(canvas, text="Night", variable=v, value="Night")  
    canvas.data.dayButton = Radiobutton(canvas, text="Day", variable=v, value="Day")  
    
    canvas.data.dayButton.pack(anchor=W, side = 'left')
    canvas.data.nightButton.pack(anchor=W, side ="left")
    canvas.data.bird1Button.pack(anchor=W, side = "right")
    canvas.data.bird2Button.pack(anchor=W, side = "right")

    canvas.data.mode = v
    canvas.data.birdChoice = b 
    canvas.bind("<Key>", keyPressed)
    root.mainloop()
   
global highScores
highScores = []
try:
    with open('highscores.txt', 'rb') as f:
        highScores = pickle.load(f)
except:
    with open('highscores.txt', 'wb') as Foo:
        pickle.dump(highScores, Foo)        
run()
