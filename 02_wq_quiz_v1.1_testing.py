from tkinter import *
from functools import partial # to prevent unwanted windows
import csv
import random

button_fg = "#FFFFFF"
button_font = ("Arial 13 bold")


# users choose 15, 20 or 30 rounds
class ChooseQuestions:
  
  def __init__(self):
    # play class with 15 questions for testing
    self.to_play(15)

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

    # question number heading
    num_questions_heading = "Question 1 of {}\n".format(how_many)
    self.choose_heading = Label(self.quiz_frame,
                                text=num_questions_heading,
                                font=("Arial 16 bold"))
    self.choose_heading.grid(row=0)

    # question label
    questions_list = "e.g. What is the capital of France?" # placeholder
    self.question_label = Label(self.quiz_frame,
                                text=questions_list,
                                font=("Arial 12"))
    self.question_label.grid(row=1)

    # answer buttons
    self.answer_frame = Frame(self.quiz_frame)
    self.answer_frame.grid(row=2)

    # list to setup answer buttons
    # item represents the bg color
    btn_ans_value = [
      ["#007FFF", "A"], ["#FF0000", "B"], ["#FFFF00", "C"], ["#00CC00", "D"]
    ]

    for item in range(0,4):
      self.answer_button = Button(self.answer_frame, fg=button_fg,
                                     bg=btn_ans_value[item][0],
                                     text="{}".format(btn_ans_value[item][1]),
                                     font=button_font, width=10,
                                     command=lambda i=item: self.to_answer(btn_ans_value[i][1])
                                    )
      self.answer_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

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