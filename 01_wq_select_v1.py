from tkinter import *
from functools import partial # to prevent unwatned windows
import csv
import random

# users choose 15, 20 or 30 rounds
class ChooseQuestions:
  
  def __init__(self):
    
    button_fg = "#FFFFFF"
    button_font = ("Arial 13 bold")
    
    # Set up GUI Frame
    self.intro_frame = Frame(padx=10,pady=10)
    self.intro_frame.grid()

    # heading and instructions
    self.heading_label = Label(self.intro_frame, 
                               text="World Quiz", 
                               font=("Arial 16 bold"))
    self.heading_label.grid(row=0)

    choose_instructions_txt = "A multiple choice quiz all about the world! \n\n" \
                              "Choose the number of questions you want to play " \
                              "and test your knowledge about the world! \n\n" \
                              "To begin select the number of questions " \
                              "you want to play..."
    self.instructions_label = Label(self.intro_frame,
                                    text=choose_instructions_txt,
                                    wraplength=300,
                                    justify="left")
    self.instructions_label.grid(row=1)

    # question no. buttons
    self.how_many_frame = Frame(self.intro_frame)
    self.how_many_frame.grid(row=2)

    self.fifteen_button = Button(self.how_many_frame, fg=button_fg,
                                 bg="#00CC00", text="15 Questions",
                                 font=button_font, width=10)
    self.fifteen_button.grid(row=0, column=0, padx=5, pady=5)

    self.twenty_button = Button(self.how_many_frame, fg=button_fg,
                                 bg="#FFFF00", text="20 Questions",
                                 font=button_font, width=10)
    self.twenty_button.grid(row=0, column=1, padx=5, pady=5)

    self.thirty_button = Button(self.how_many_frame, fg=button_fg,
                                 bg="#FF0000", text="30 Questions",
                                 font=button_font, width=10)
    self.thirty_button.grid(row=0, column=2, padx=5, pady=5)
                                 

# main routine
if __name__ == "__main__":
  root = Tk()
  root.title('World Quiz')
  ChooseQuestions()
  root.mainloop()