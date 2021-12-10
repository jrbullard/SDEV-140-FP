 # Program name : Death by Letters
 # Author : Jordan Bullard
 # Date finished : 12/9/2021
from ctypes import windll
import tkinter.font as font
from tkinter import *
import random
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk, Image

 # To fix blurriness
windll.shcore.SetProcessDpiAwareness(1)

 # Function to pick the category and make a label for it
def pickCat():
    global f, catLab
    files = ['stuff/food.txt', 'stuff/animals.txt', 'stuff/mythical.txt'] # List of file names
    cat = random.choice(files) # Assigning a random category
    f = (open(cat, 'r')) # Opening the file
    if  cat == files[0]:
        catLab = Label(root, # Label to show chosen category
                       text = ("Category is: Food"),
                       font = otherFont,
                       bg = 'oldlace',
                       fg = 'black')
        catLab.place(x = 275, y = 540)
    elif cat == files[1]:
        catLab = Label(root, # Label to show chosen category
                       text = ("Category is: Animals"),
                       font = otherFont,
                       bg = 'oldlace',
                       fg = 'black')
        catLab.place(x = 275, y = 540)
    else:
        catLab = Label(root, # Label to show chosen category
                       text = ("Category is: Mythological Creatures"),
                       font = otherFont,
                       bg = 'oldlace',
                       fg = 'black')
        catLab.place(x = 175, y = 540)

 # Clearing out old stuff to restart
def restart():
    attRemLabel.destroy()
    catLab.destroy()
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
    dx = 200 # To space out the labels
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
                                       icon = 'info') # to store if the user wants to play again
        messageAns(again)

 # Function to check and replace letters if they are correct       
def check():
    global wordLetters, box, letterLabels, correctLet, attempt, wrongLet, attRem, rightLetters, wrongLetters
    attempt = box.get() # Getting the input from entry box
    box.delete(0)
    attempt = attempt.upper() # Making the guess uppercase to be able to compare easier
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

 # Function to clear default text when clicked
def textClear(box):
    if box.get() == "here":
        box.delete(0, END)

 # Function for the whole game after title screen
def actualGame():
    global incorrectAttempts, attRemLabel, picLabels, box, wordLetters, letterLabels, correctLet, wrongLet, wrongLetters, rightLetters, chosenWord, f
    exitButton.configure(text = "Exit", # Adjusting exit button label
                         height = 1,
                         width = 10,
                         fg = 'oldlace',
                         bg = 'indianred4')
    exitButton.place(x = 450, y = 800)
    retryButton = Button(root, # Start over button
                         text = "Start Over",
                         font = otherFont,
                         height = 1,
                         width = 10,
                         fg = 'oldlace',
                         bg = 'indianred4',
                         command = restart)
    retryButton.place(x = 200, y = 800)
    correctLet = 0 # Number to keep track of correct attempts
    rightLetters = [None] # List to keep correct letters
    incorrectAttempts = 6 # Number to keep track of incorrect attempts
    root.configure(bg = 'oldlace')
    intro.configure(bg = 'oldlace',
                    fg = 'indianred4') # Editing top label
     # Choosing word from list and separating the letters
    pickCat()
    words = [] # List for words in file
    for line in f:
        line = line.strip()
        line = line.upper()
        wordList = line.split()
        words.append(wordList)
    f.close()
    chosenWord = random.choice(words) # Word to be guessed
    wordLetters = list(chosenWord[0]) # List to store the chosen word's letters

     # Label list so they can be replaced later
    letterLabels = [Label(root,
                            text = ch,
                            font = mainFont,
                            bg = 'oldlace',
                            fg = 'indianred4') for ch in wordLetters] # Labels for the word letters

    makeDashes()

     # Stick picture labeling into a list and placing the default
    stickPics = ['s1', 's2', 's3', 's4', 's5', 's6', 's7'] # List of drawn stick figure pictures
    picLabels = [] # List for the picture labels to sit in until they are needed
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
                     fg = 'black') # attempts remaining label
    attRemLabel.pack()

     # Label to keep track of incorrect guesses for user
    wrongLetters = [None] # List for incorrect guesses
    wrongLet = Label(root,
                     text = "Incorrect guesses: ",
                     font = tk.font.Font(family = "system",
                                         size = 25,
                                         weight = 'bold'),
                     bg = 'oldlace',
                     fg = 'black',) # Label for incorrect guesses
    wrongLet.place(x = 10, y = 700)

     # Entry box for guess
    box = Entry(root,
                font = mainFont,
                fg = 'indianred4',
                width = 4) # Entry box to take inputted guesses
    box.insert(0, "here")
    box.place(x = 620, y = 575)
    box.bind("<Return>",
             lambda event: check()) # Binding the box to the check()
    box.bind('<Button-1>',          # and textClear() events
             lambda event: textClear(box))

     # Label for the entry box to let user know to put guess in the box
    attLabel = Label(root,
                     text = "Enter your guess:",
                     font = mainFont,
                     bg = 'oldlace',
                     fg = 'indianred4') # Attempts remaining label
    attLabel.place(x = 10, y = 575)
        
 # Function to define what happens when the user presses start from the title screen
def startPressed():
    instructions.destroy()
    startButton.destroy()
    actualGame()

 # Setting up the title screen 
root = tk.Tk() # screen
root.title('Death by Letters')
root.geometry('805x900+600+35')
root.resizable(False, False)
root.iconbitmap('stuff/skull_bw.ico')
root.configure(bg = 'indianred4')
mainFont = tk.font.Font(family = "system",
                         size = 37,
                         weight = 'bold') # Title font used
    
otherFont = tk.font.Font(family = "system",
                         size = 15) # Smaller font
 # Header label
intro = tk.Label(root,
                 text = "DEATH  BY  LETTERS",
                 font = mainFont,
                 bg = 'indianred4',
                 fg = 'oldlace') # header label
intro.pack()

 # Instructions on how to play
instructions = tk.Label(root,
                        text = "Instructions: Guess the letters in the word or die trying.\nWould you like to play?",
                        font = otherFont,
                        bg = 'indianred4',
                        fg = 'oldlace') # instructions label
instructions.pack()

 # Start button to initiate game
startButton = tk.Button(root,
                        height = 2,
                        width = 20,
                        text = "I guess.",
                        font = otherFont,
                        bg = 'oldlace',
                        fg = 'indianred4',
                        command = startPressed) # start button and binding it to the command startPressed()
startButton.place(x = 230, y = 300)

 # Exit button to end program
exitButton = tk.Button(root, # Exit button
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
