#from wq_questions_v2 import *
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
    self.questions_wanted.set(how_many)
    
    # Initially set questions answered and correct answers to 0
    self.questions_answered = IntVar()
    self.questions_answered.set(0)

    self.questions_correct = IntVar()
    self.questions_correct.set(0)

    # list to hold users answers
    self.user_answers = []

    # get all the questions & answers from the csv file
    self.all_questions = self.get_all_questions()
    
    # question number heading
    self.choose_heading = Label(self.quiz_frame,
                                font=("Arial 16 bold"))
    self.choose_heading.grid(row=0)

    # creates question label
    self.question_heading = Label(self.quiz_frame,
                                font=("Arial 12"))
    self.question_heading.grid(row=1)

    # get questions and answers for heading and buttons for first round
    self.question_answer_list = []
    
    # answer buttons frame
    self.answer_frame = Frame(self.quiz_frame)
    self.answer_frame.grid(row=2)

    self.answer_button_ref = []
    
    # list to setup answer button colors
    button_color = ["#007FFF", "#FF0000", "#FFFF00", "#00CC00"]

    # loop to create buttons for each answer
    for item in range(0,4):
      self.answer_button = Button(self.answer_frame, fg=button_fg,
                                  bg=button_color[item],
                                  font=button_font, 
                                  width=20, height=2,
                                  command=lambda i=item: 
                                  self.to_answer(self.answer_label[i])
                                  )
      # add button to reference list for later configs
      self.answer_button_ref.append(self.answer_button)
      
      self.answer_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

    self.next_button = Button(self.quiz_frame, 
                              text="Next Question",
                              fg="#FFFFFF",
                              bg="#007FFF",
                              font="Arial 12 bold",
                              width=10, state=DISABLED)
    self.next_button.grid(row=3)

    # at start, get 'new round'
    self.new_round()
    
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

  # check answer if selected answer is correct
  # update correct/incorrect counters
  def to_answer(self, user_choice):
    print()
    how_many = self.questions_wanted.get()

    # add one to number of rounds played
    current_question = self.questions_answered.get()
    self.questions_answered.set(current_question + 1)

    # deactivates answer buttons
    for item in self.answer_button_ref:
      item.config(state=DISABLED)

    # temp
    # check if the user's answer is correct
    if user_choice == self.round_answers[0]:
      print("correct")
    else:
      print("incorrect")

    # remove current question from list
    self.question_answer_list.pop()

    # if quiz is over, disable all buttons then add enable next button
    if current_question == how_many:
      self.next_button.config(state=DISABLED,
                             text="Quiz Complete")
      # update start over

      # grey buttons
      for item in self.answer_button_ref:
        item['bg'] = "#C0C0C0"

    else:
      # enable next button and update heading
      self.next_button.config(state=NORMAL)
      

  def new_round(self):

    # disable next question button (renable when a question is answered)
    self.next_button.config(state=DISABLED)

    # empty button list so get new answers
    self.question_answer_list.clear()

    # get new questions & answers
    self.question_answer_list = self.get_round_questions()
    print(self.question_answer_list)

    # get answers from round questions excluding the question
    self.round_answers = self.question_answer_list[0][1:]
    print(self.round_answers) # for testing purposes remove later
    
    # shuffle round answers for answer labels
    self.answer_label = random.sample(self.round_answers, k=4)
    print(self.answer_label) # for testing purposes remove later

    # set button answers
    for count, item in enumerate(self.answer_button_ref):
      item['text'] = self.answer_label[count]
      item['state'] = NORMAL

    # get number of questions selected and update heading
    how_many = self.questions_wanted.get()
    current_question = self.questions_answered.get()
    new_heading = "Question {} of {}\n".format(current_question + 1, how_many)
    self.choose_heading.config(text=new_heading)

    # get the question for the question label
    question_label = self.question_answer_list[0][0]
    self.question_heading.config(text=question_label)
    
  
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