from tkinter import *
from functools import partial # to prevent unwanted windows
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

    # list to setup selection buttion
    # First item represents the bg color
    # Second item is the number of questions
    btn_color_value = [
      ["#00CC00", 15], ["#FFFF00", 20], ["#FF0000", 30]
    ]

    for item in range(0,3):
      self.questions_button = Button(self.how_many_frame, fg=button_fg,
                                     bg=btn_color_value[item][0],
                                     text="{} Questions".format(btn_color_value[item][1]),
                                     font=button_font, width=10,
                                     command=lambda i=item: self.to_play(btn_color_value[i][1])
                                    )
      self.questions_button.grid(row=0, column=item, padx=5, pady=5)

  def to_play(self, num_questions):
    PlayQuiz(num_questions)

    # Hide root window (hides ChooseQuestions window)
    root.withdraw()

class PlayQuiz:

  def __init__(self, how_many):
    # Set up GUI Frame
    self.play_box = Toplevel()

    # If user presses "x" on top right corner
    # close quiz and 'release' quiz button
    self.play_box.protocol('WM_DELETE_WINDOW',
                          partial(self.close_play))

    self.quiz_frame = Frame(self.play_box, padx=10, pady=10)
    self.quiz_frame.grid()

    num_questions_heading = "Question 1 of {}".format(how_many)
    self.choose_heading = Label(self.quiz_frame,
                                text=num_questions_heading,
                                font=("Arial 16 bold"))
    self.choose_heading.grid(row=0)

    self.control_frame = Frame(self.quiz_frame)
    self.control_frame.grid(row=6)

    self.start_over_button = Button(self.control_frame,
                                    text="Start Over",
                                    command=self.close_play)
    self.start_over_button.grid(row=0, column=2)

  def close_play(self):
    # redisplay ChooseQuestions (root) window
    # and end current quiz / allow a new quiz to start
    root.deiconify()
    self.play_box.destroy()

# main routine
if __name__ == "__main__":
  root = Tk()
  root.title('World Quiz')
  ChooseQuestions()
  root.mainloop()