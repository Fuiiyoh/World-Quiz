# from get_all_questions_v2 import *
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

    # Variables used to note statistcs, when the game ends
    self.questions_wanted = IntVar()
    self.questions_wanted = (how_many)

    # Initially set questions answered and correct answers to 0
    self.questions_answered = IntVar()
    self.questions_answered = 0

    self.questions_correct = IntVar()
    self.questions_correct = 0

    # list to hold users answers
    self.user_answers = []

    # get all the questions from the csv file
    self.all_questions = self.get_all_questions()


    # question number heading
    num_questions_heading = "Question 1 of {}\n".format(how_many)
    self.choose_heading = Label(self.quiz_frame,
                                text=num_questions_heading,
                                font=("Arial 16 bold"))
    self.choose_heading.grid(row=0)

    # get questions for the label and answers for the buttons
    # for the first round of questions
    quiz_questions_list = self.get_round_questions()
    print(quiz_questions_list) # for testing purposes remove later

    # create question label
    question_label = quiz_questions_list[0][0]
    # question label 
    self.question_label = Label(self.quiz_frame,
                                text=question_label,
                                font=("Arial 12"))
    self.question_label.grid(row=1)

    # answer buttons
    self.answer_frame = Frame(self.quiz_frame)
    self.answer_frame.grid(row=2)

    # create answers button text
    answer_text = random.sample(quiz_questions_list[0][1:], k=4)
    print(answer_text) # for testing purposes remove later

    # list to setup answer buttons
    # item represents the bg color
    btn_ans_value = [
      ["#007FFF", answer_text[0]],
      ["#FF0000", answer_text[1]],
      ["#FFFF00", answer_text[2]],
      ["#00CC00", answer_text[3]]
    ]

    for item in range(0,4):
      self.answer_button = Button(self.answer_frame, fg=button_fg,
                                     bg=btn_ans_value[item][0],
                                     text="{}".format(btn_ans_value[item][1]),
                                     font=button_font, width=20, height=2,
                                     #command=lambda i=item: self.to_answer(btn_ans_value[i][1])
                                    )
      self.answer_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

    self.control_frame = Frame(self.quiz_frame)
    self.control_frame.grid(row=6)

    self.start_over_button = Button(self.control_frame,
                                    text="Start Over",
                                    command=self.close_play)
    self.start_over_button.grid(row=0, column=2)

  # get questions from csv file
  def get_all_questions(self):
    file = open("WorldQuiz_Questions.csv", "r")
    var_all_questions = list(csv.reader(file, delimiter=","))
    file.close()

    # remove first row (headers)
    var_all_questions.pop(0)
    return var_all_questions

  # randomly choose a question for header and buttons
  def get_round_questions(self):
    round_question_list = []
    question_scores = []

    # get 1 question from the csv file
    while len(round_question_list) < 1:
      # choose question
      chosen_question = random.choice(self.all_questions)
      index_chosen = self.all_questions.index(chosen_question)

      # check score is not already in the list
      if chosen_question[1] not in question_scores:
        # add item to questions list
        round_question_list.append(chosen_question)
        question_scores.append(chosen_question[1])

        # remove from master list
        self.all_questions.pop(index_chosen)

    return round_question_list

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