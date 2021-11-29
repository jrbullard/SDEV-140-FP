 # Program name : Death by Letters
 # Author : Jordan Bullard
 # Date finished : TBD
from ctypes import windll
import tkinter.font as font
from tkinter import *
import random
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk, Image

 # To fix blurriness
windll.shcore.SetProcessDpiAwareness(1)

 # Clearing out old stuff to restart
def restart():
    attRemLabel.destroy()
    wrongLet.destroy()
    for fr in letterLabels:
        fr.destroy()
    actualGame()

 # Messagebox choices
def messageAns(again):
    global attRemLabel, wrongLet, rightLetters, letterLabels, wrongLetters
    if again == True:
            restart()
    if again == False:
        root.destroy()

 # Hiding the letters of the right word
def makeDashes():
    dx = 200
    for fr in letterLabels:
        fr.configure(text = '_',
                     font = mainFont)
        fr.place(x = dx, y = 450)
        dx += 75
    
 # Function to subtract attempts and replace stick figure image
def subtractAttempt():
    global incorrectAttempts, attRemLabel, picLabels, attempt, wrongLetters, wrongLet, chosenWord, rightLetters
    incorrectAttempts -= 1
    wrongLetters.append(attempt)
    wrongLet.configure(text = "Incorrect guesses: " + (str(wrongLetters).replace("'", "")[7:-1]))
    attRemLabel.configure(text = "INCORRECT ATTEMPTS REMAINING: " + str(incorrectAttempts))
    if incorrectAttempts == 5:
        picLabels[0].destroy()
        picLabels[1].place(x = 295, y = 120)
    elif incorrectAttempts == 4:
        picLabels[1].destroy()
        picLabels[2].place(x = 295, y = 120)
    elif incorrectAttempts == 3:
        picLabels[2].destroy()
        picLabels[3].place(x = 295, y = 120)
    elif incorrectAttempts == 2:
        picLabels[3].destroy()
        picLabels[4].place(x = 295, y = 120)
    elif incorrectAttempts == 1:
        picLabels[4].destroy()
        picLabels[5].place(x = 295, y = 120)
     # If no attempts remain then a message to play again or exit will come up
    elif incorrectAttempts == 0:
        picLabels[5].destroy()
        picLabels[6].place(x = 295, y = 120)
        again = tk.messagebox.askyesno('Loser :(',
                                       'You lost. The word was: ' + str(chosenWord)[2:-2] +'. Would you like to play again?',
                                       icon = 'info')
        messageAns(again)

 # Function to check and replace letters if they are correct       
def check():
    global wordLetters, box, letterLabels, correctLet, attempt, wrongLet, attRem, rightLetters, wrongLetters
    attempt = box.get()
    box.delete(0)
    if attempt.isdigit():
        return
    attempt = attempt.upper()
    if attempt not in wordLetters or attempt in rightLetters:
        subtractAttempt()
        return
    for m, ch in enumerate(wordLetters):
        if ch == attempt:
            letterLabels[m].configure(text = ch)
            correctLet += 1
            rightLetters.append(attempt)
    if correctLet == 6:
        again = tk.messagebox.askyesno('Winner!!',
                                       'You Won! Would you like to play again?',
                                       icon = 'info')
        messageAns(again)
    
 # Function for the whole game after title screen
def actualGame():
    global incorrectAttempts, attRemLabel, picLabels, box, wordLetters, letterLabels, correctLet, wrongLet, wrongLetters, rightLetters, chosenWord
    exitButton.configure(text = "Exit",
                         height = 1,
                         width = 10,
                         fg = 'oldlace',
                         bg = 'indianred4')
    exitButton.place(x = 450, y = 800)
    retryButton = Button(root,
                         text = "Start Over",
                         font = otherFont,
                         height = 1,
                         width = 10,
                         fg = 'oldlace',
                         bg = 'indianred4',
                         command = restart)
    retryButton.place(x = 200, y = 800)
    correctLet = 0
    rightLetters = [None]
    incorrectAttempts = 6
    root.configure(bg = 'oldlace')
    intro.configure(bg = 'oldlace',
                    fg = 'indianred4')
     # Choosing word from list and separating the letters
    f = open('stuff/words.txt', 'r')
    words = []
    for line in f:
        line = line.strip()
        line = line.upper()
        wordList = line.split()
        words.append(wordList)
    f.close()
    chosenWord = random.choice(words)
    wordLetters = list(chosenWord[0])

     # Label list so they can be replaced later
    letterLabels = [Label(root,
                            text = ch,
                            font = mainFont,
                            bg = 'oldlace',
                            fg = 'indianred4') for ch in wordLetters]

    makeDashes()

     # Stick picture labeling into a list and placing the default
    stickPics = ['s1', 's2', 's3', 's4', 's5', 's6', 's7']
    picLabels = []
    for pic in stickPics:
        pic = PhotoImage(file= 'stuff/' + pic + '.png')
        picLabel = Label(image = pic,
                         bg = 'oldlace')
        picLabels.append(picLabel)
        picLabel.image = pic
    picLabels[0].place(x = 300, y = 120)

     # Label to display incorrect attempts remaining
    attRemLabel = Label(root,
                     text = "INCORRECT ATTEMPTS REMAINING: " + str(incorrectAttempts),
                     font = otherFont,
                     bg = 'oldlace',
                     fg = 'black')
    attRemLabel.pack()

     # Label to keep track of incorrect guesses for user
    wrongLetters = [None]
    wrongLet = Label(root,
                     text = "Incorrect guesses: ",
                     font = otherFont,
                     bg = 'oldlace',
                     fg = 'black')
    wrongLet.place(x = 150, y = 700)

     # Entry box for guess
    box = Entry(root,
                font = mainFont,
                fg = 'indianred4',
                width = 2)
    box.place(x = 650, y = 575)
    box.bind("<Return>",
                  lambda event: check())

     # Label for the entry box to let user know to put guess in the box
    attLabel = Label(root,
                     text = "Enter your guess:",
                     font = mainFont,
                     bg = 'oldlace',
                     fg = 'indianred4')
    attLabel.place(x = 50, y = 575)
        
 # Function to define what happens when the user presses start from the title screen
def startPressed():
    instructions.destroy()
    startButton.destroy()
    actualGame()

 # Setting up the title screen 
root = tk.Tk()
root.title('Death by Letters')
root.geometry('805x900+600+35')
root.resizable(False, False)
root.iconbitmap('stuff/skull_bw.ico')
root.configure(bg = 'indianred4')
mainFont = tk.font.Font(family = "system",
                         size = 37,
                         weight = 'bold')
    
otherFont = tk.font.Font(family = "system",
                         size = 15)
 # Header label
intro = tk.Label(root,
                 text = "DEATH  BY  LETTERS",
                 font = mainFont,
                 bg = 'indianred4',
                 fg = 'oldlace')
intro.pack()

 # Instructions on how to play
instructions = tk.Label(root,
                        text = "Instructions: Guess the letters in the word or die trying.\nWould you like to play?",
                        font = otherFont,
                        bg = 'indianred4',
                        fg = 'oldlace')
instructions.pack()

 # Start button to initiate game
startButton = tk.Button(root,
                        height = 2,
                        width = 20,
                        text = "I guess.",
                        font = otherFont,
                        bg = 'oldlace',
                        fg = 'indianred4',
                        command = startPressed)
startButton.place(x = 230, y = 300)

 # Exit button to end program
exitButton = tk.Button(root,
                       height = 2,
                       width = 20,
                       text = "Nah, I'm good.",
                       font = otherFont,
                       bg = 'oldlace',
                       fg = 'indianred4',
                       command = lambda: root.destroy())
exitButton.place(x = 230, y = 500)
    
 # To make sure the program runs
root.mainloop()
