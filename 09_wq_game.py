#from test_stats_v2 import *
from tkinter import *
from functools import partial # to prevent unwanted windows
import csv
import random
from tkinter import font
from datetime import date
import re

button_fg = "#FFFFFF"
button_font = ("Arial 13 bold")


# users choose 15, 20 or 30 rounds
class ChooseQuestions:

  def __init__(self):

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

    # list to setup selection button
    # First item represents the bg color
    # Second item is the number of questions
    btn_color_value = [
      ["#28900D", 15], ["#D89E00", 20], ["#E21C3D", 30]
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

    # Variables used to note statistcs, when the game ends
    self.questions_wanted = IntVar()
    self.questions_wanted.set(how_many)
    
    # Initially set questions answered and correct answers to 0
    # variable to hold users score (questions correct)
    self.questions_answered = IntVar()
    self.questions_answered.set(0)

    self.questions_correct = IntVar()
    self.questions_correct.set(0)

    # list to hold questions
    self.answered_questions_list = []
    # list to hold users answers
    self.user_answers = []
    # list to hold correct answers
    self.correct_answers = []

    # get all the questions & answers from the csv file
    self.all_questions = self.get_all_questions()
    
    # question number heading
    self.choose_heading = Label(self.quiz_frame,
                                font=("Arial 16 bold"))
    self.choose_heading.grid(row=0)

    # creates question label
    self.question_heading = Label(self.quiz_frame,
                                font=("Arial 12"))
    self.question_heading.grid(row=1, pady=10)

    # get questions and answers for heading and buttons for first round
    self.question_answer_list = []
    
    # answer buttons frame
    self.answer_frame = Frame(self.quiz_frame)
    self.answer_frame.grid(row=2)

    self.answer_button_ref = []
    
    # list to setup answer button colors
    button_color = ["#1369CE", "#E21C3D", "#D89E00", "#28900D"]

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

    self.answer_indicate_label = Label(self.quiz_frame,
                                  font="Arial 12 bold")
    self.answer_indicate_label.grid(row=3, pady=10)

    self.next_button = Button(self.quiz_frame, 
                              text="Next Question",
                              fg="#FFFFFF",
                              bg="#004C99",
                              font=button_font,
                              width=12, state=DISABLED,
                              command=self.new_round)
    self.next_button.grid(row=4)

    self.blank_space = Label(self.quiz_frame, text="\n\n")
    self.blank_space.grid(row=5)
    
    # at start, get 'new round'
    self.new_round()
    
    self.control_frame = Frame(self.quiz_frame)
    self.control_frame.grid(row=6)

    control_buttons = [
      ["#CC6600", "Help", "get help"],
      ["#004C99", "Statistics", "get stats"],
      ["#808080", "Start Over", "start over"]
    ]

    # list to hold references for control buttons
    # so that the text of the 'start over' can easily
    # be configured when the quiz ends
    self.control_button_ref = []

    for item in range(0, 3):
      self.make_control_button = Button(self.control_frame,
                                        fg="#FFFFFF",
                                        bg=control_buttons[item][0],
                                        text=control_buttons[item][1],
                                        width=12, font=button_font,
                                        command=lambda i=item: 
                                        self.to_do(control_buttons[i][2]))
      self.make_control_button.grid(row=0, column=item, padx=5, pady=5)
      
      # add buttons to control list
      self.control_button_ref.append(self.make_control_button)

    self.to_help_btn = self.control_button_ref[0]
    self.to_stats_btn = self.control_button_ref[1]
    self.to_start_over_btn = self.control_button_ref[2]
    self.to_stats_btn.config(state=DISABLED)

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

    # add to list: answered questions, user answers, correct answers
    self.answered_questions_list.append(self.question_answer_list[0][0])
    self.user_answers.append(user_choice)
    self.correct_answers.append(self.round_answers[0])
    print(self.answered_questions_list)
    print(self.user_answers)
    print(self.correct_answers)

    # check if the user's answer is correct
    if user_choice == self.round_answers[0]:
      self.answer_indicate_label.config(text="Correct! The answer is {}"
                                        .format(self.round_answers[0]),
                                        fg="#009900")
      print("correct") # for testing
      score = self.questions_correct.get()
      self.questions_correct.set(score + 1)
    else:
      self.answer_indicate_label.config(text="Incorrect! The answer is {}"
                                        .format(self.round_answers[0]),
                                        fg="#FF0000")
      print("incorrect") # for testing

    # update score label
    print(self.questions_correct.get()) # for testing

    # if quiz is over, disable all buttons then add enable next button
    if current_question == how_many - 1:
      self.next_button.config(state=DISABLED,
                             text="Quiz Complete")
      # update start over
      self.to_start_over_btn.config(bg="#28900D",
                                    text="Restart Quiz")

      # grey buttons
      for item in self.answer_button_ref:
        item['bg'] = "#C0C0C0"

    else:
      # enable next button and update heading
      self.next_button.config(state=NORMAL)

    self.to_stats_btn.config(state=NORMAL)

  # starts a new round with a new question
  def new_round(self):

    # disable next question button (renable when a question is answered)
    self.next_button.config(state=DISABLED)
    self.answer_indicate_label.config(text="")

    # empty button list so get new answers
    self.question_answer_list.clear()

    # get new questions & answers
    self.question_answer_list = self.get_round_questions()
    #print(self.question_answer_list) # for testing purposes remove later

    # get answers from round questions excluding the question
    self.round_answers = self.question_answer_list[0][1:]
    #print(self.round_answers) # for testing purposes remove later
    
    # shuffle round answers for answer labels
    self.answer_label = random.sample(self.round_answers, k=4)
    #print(self.answer_label) # for testing purposes remove later

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

  # opens the help/stats GUI, start over restarts quiz
  def to_do(self, action):
    if action == "get help":
      DisplayHelp(self)
    elif action == "get stats":
      DisplayStats(self, self.questions_correct.get(), 
                   self.questions_answered.get(),
                   self.answered_questions_list, 
                   self.user_answers, 
                   self.correct_answers)
    else:
      self.close_play()
    
  # closes current quiz and redisplays ChooseQuestions window 
  def close_play(self):
    # redisplay ChooseQuestions (root) window
    # and end current quiz / allow a new quiz to start
    root.deiconify()
    self.play_box.destroy()

class DisplayHelp:

  def __init__(self, partner):
  
      # setup dialogue box and background color
      background = "#ffe6cc"
      self.help_box = Toplevel()
  
      #disable help button
      partner.to_help_btn.config(state=DISABLED)
  
      # If user press cross at top, close help and
      # 'releases' help button
      self.help_box.protocol('WM_DELETE_WINDOW',
                             partial(self.close_help,partner))
  
      self.help_frame = Frame(self.help_box, width=300, 
                              height=200,
                              bg=background)  
      self.help_frame.grid()
  
      self.help_heading_label = Label(self.help_frame, 
                                      bg=background,
                                      text="Help / Info",
                                      font=("Arial 14 bold"))
      self.help_heading_label.grid(row=0, pady=10)
  
      help_text = "\nHow well you know the world? Test your knowledge and discover " \
                  "how well you know the world! \n\n" \
                  "You will be give a randomly selected question with 4 possible " \
                  "answers. You must click on an answer and if it's correct your " \
                  "will be rewarded with a point. The Next Question button will " \
                  "activate after each answer. \n\n" \
                  "The Statistics menu will display your total score at the " \
                  "current question with your correct percentage %. You can " \
                  "export your score with the question with your correct/incorrect " \
                  "answer to a text file by clicking the Export button. \n\n" \
                  "If you want to restart the quiz, Click the Start Over button " \
                  "to restart the quiz.\n\n" \
                  "Have fun and goodluck!"
      
      self.help_text_label = Label(self.help_frame, bg=background,
                                   text=help_text, wraplength=400,
                                   justify="left")
      self.help_text_label.grid(row=1, padx=10)
  
      self.dismiss_button = Button(self.help_frame,
                                   font=("Arial 12 bold"),
                                   text="Dismiss", bg="#CC6600",
                                   fg="#FFFFFF", width=10,
                                   command=partial(self.close_help,
                                                   partner))
      self.dismiss_button.grid(row=2, padx=10, pady=10)
  
  # closes help dialogue (used by button and x at top of dialogue)
  def close_help(self, partner):
      # put help button back to normal
      partner.to_help_btn.config(state=NORMAL)
      self.help_box.destroy()
    
class DisplayStats:
  def __init__(self, partner, score, current_ques, questions, user_ans, correct_ans):

    # Set variables to hold filename and date
    # for when writing to file
    self.var_filename = StringVar()
    self.var_todays_date = StringVar()

    self.questions = questions
    self.user_ans = user_ans
    self.correct_ans = correct_ans

    # setup dialogue box and background color
    self.stats_box = Toplevel()

    stats_bg_color = "#DAE8FC"

    # disable stats button
    partner.to_stats_btn.config(state=DISABLED)

    # If user press cross at top, close stats and
    # release stats button
    self.stats_box.protocol('WM_DELETE_WINDOW',
                            partial(self.close_stats, partner))

    self.stats_frame = Frame(self.stats_box, width=300, 
                             height=200, bg=stats_bg_color)
    self.stats_frame.grid()

    # heading
    self.stats_heading_label = Label(self.stats_frame,
                                    text="Statistics",
                                    font="Arial 14 bold",
                                    bg=stats_bg_color)
    self.stats_heading_label.grid(row=0, pady=10)

    # stats label
    stats_text = "Here are your quiz statistics..."
    self.stats_text_label = Label(self.stats_frame, text=stats_text,
                                  wraplength=200,
                                 justify="left", bg=stats_bg_color)
    self.stats_text_label.grid(row=1,pady=5)

    # frame to hold stats table
    self.data_frame = Frame(self.stats_frame, bg=stats_bg_color,
                           borderwidth=1, relief="solid")
    self.data_frame.grid(row=2, padx=10, pady=10)

    # get stats
    self.statistics = self.get_stats(score, current_ques)

    # bg formatting for heading, odd and even rows
    odd_rows = "#A9C4EB"
    even_rows = stats_bg_color

    row_names = ["Score:       ", "Question #", "Correct %  "]
    row_format = [odd_rows, even_rows, odd_rows]

    # data for labels (one label / sub list)
    all_labels = []
  
    for count, item in enumerate(range(0, len(self.statistics))):
      all_labels.append([row_names[item], row_format[count]])
      all_labels.append([self.statistics[item], row_format[count]])

    # create labels for each sub list
    for item in range(0, len(all_labels)):
      self.data_label = Label(self.data_frame, text=all_labels[item][0],
                              font="Arial 11 normal",bg=all_labels[item][1],
                              width=12, height=2, padx=5)
      self.data_label.grid(row=item // 2, column=item % 2, padx=0, pady=0)

    # export heading
    export_text = "Either choose a custom filename (and click " \
                  "<Export>) or click <Export> to save your statistics " \
                  "and answered questions and answers to a text file. " \
                  "If the file already exists, it will be overwritten!\n\n" \
                  "Exports display additional information on your previously " \
                  "answered questions and answers."
    self.export_instructions_label = Label(self.stats_frame,
                                           text=export_text,
                                           wraplength=300,
                                           justify="left", bg=stats_bg_color,
                                           width=40, padx=10)
    self.export_instructions_label.grid(row=3, pady=10)

    # Filename entry widget, white background to start
    self.filename_entry = Entry(self.stats_frame,
                                font=("Arial 14 normal"),
                                bg="#FFFFFF", width=25)
    self.filename_entry.grid(row=4, padx=10, pady=10)

    self.filename_feedback_label = Label(self.stats_frame,
                                         text="",
                                         fg="#9C0000", 
                                         bg=stats_bg_color,
                                         wraplength=300,
                                         font=("Arial 12 bold"))
    self.filename_feedback_label.grid(row=5)

    # export and dismiss buttons
    self.button_frame = Frame(self.stats_frame, bg=stats_bg_color)
    self.button_frame.grid(row=6)

    self.export_button = Button(self.button_frame,
                                font=("Arial 12 bold"),
                                text="Export", bg="#004C99",
                                fg="#FFFFFF", width=10,
                                command=self.make_file)
    self.export_button.grid(row=0, column=0, padx=10, pady=10)
    
    self.dismiss_button = Button(self.button_frame,
                                 font=("Arial 12 bold"),
                                 text="Dismiss", bg="#666666",
                                 fg="#FFFFFF", width=10,
                                 command=partial(self.close_stats, partner))
    self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)
    

  # calculates stats into a columm
  @staticmethod
  def get_stats(score, current_ques):
    average = round((score / current_ques) * 100, 2), "%"

    return[score, current_ques, average]

  # function to convert
  @staticmethod
  def list_to_string(list):
    # initialize an empty string
    string = " "

    # return string
    return (string.join([str(elem) for elem in list]))

  # create to file
  def make_file(self):
    # get filename from entry widget
    filename = self.filename_entry.get()

    filename_ok = ""
    date_part = self.get_date()
    
    if filename == "":
      # get date and create default filename
      date_part = self.get_date()
      filename = "{}_world_quiz_results".format(date_part)
    else:
      # check that filename is valid
      filename_ok = self.check_filename(filename)

    if filename_ok == "":
      filename += ".txt"
      success = "Success! Your statistics and results have " \
                "been saved as {}".format(filename)
      self.var_filename.set(filename)
      self.filename_feedback_label.config(text=success,
                                          font="Arial 11 bold",
                                          fg="dark green")
      self.filename_entry.config(bg="#FFFFFF")

      # Write content to file!
      self.write_to_file()

    else:
      self.filename_feedback_label.config(text=filename_ok,
                                          font="Arial 11 bold",
                                          fg="dark red")
      self.filename_entry.config(bg="#F8CECC")
  
  # gets todays date and creates YYYY_MM_DD string
  def get_date(self):
    today = date.today()

    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")

    todays_date = "{}/{}/{}".format(day, month, year)
    self.var_todays_date.set(todays_date)

    return "{}_{}_{}".format(year, month, day)

  # checks that filename is valid
  @staticmethod
  def check_filename(filename):
      problem = ""

      # Regular expression to check filename is valid
      valid_char = "[A-Za-z0-9_]"

      # iterates through filename and checks each letter.
      for letter in filename:
          if re.match(valid_char, letter):
              continue

          elif letter == " ":
              problem = "Sorry, no spaces allowed"

          else:
              problem = ("Sorry, no {}'s allowed".format(letter))
          break

      if problem != "":
          problem = "{}. Use letters / numbers / " \
                  "underscores only.".format(problem)

      return problem

  # creates file
  def write_to_file(self):
    # get date, filename and answered questions and answers...
    filename = self.var_filename.get()
    generated_date = self.var_todays_date.get()

    # set up strings to be written to file
    heading = "**** World Quiz - Results ****\n"
    generated = "Generated: {}".format(generated_date)
    sub_heading = "Here are your statistics and results:\n" 
    stats_heading = "Your score: {}/{} ({})\n".format(
      str(self.statistics[0]),
      str(self.statistics[1]),
      self.list_to_string(self.statistics[2]))

    # set up empty lists to write questions and answers
    qna_content = []
    
    all_ques = []
    all_correct_ans = []
    all_user_ans = []

    # add questions and answers to lists
    for i in range(len(self.questions)):
      all_ques.append(self.questions[i])
      all_correct_ans.append(self.correct_ans[i])
      all_user_ans.append(self.user_ans[i])

      # add questions and answers to qna content
      qna_content.append("Question {}: \n{}\n" \
                         "Correct answer: {}\n" \
                         "Your answer: {}\n\n".format(
                           i+1, all_ques[i], 
                           all_correct_ans[i], 
                           all_user_ans[i]))
      i+=1

    to_output_list = [heading, generated, sub_heading, stats_heading,
                     qna_content]

    # write to file
    # write output to file
    text_file = open(filename, "w+")

    for item in to_output_list:
        for i in range(len(item)):
          text_file.write(item[i])
        text_file.write("\n")
      
    # close file
    print("exported!") # for testing
    text_file.close()
  
  # closes stats dialogue (used by button and x at top of dialogue)
  def close_stats(self, partner):
      # put stats button back to normal
      partner.to_stats_btn.config(state=NORMAL)
      self.stats_box.destroy()

# main routine
if __name__ == "__main__":
  root = Tk()
  root.title('World Quiz')
  ChooseQuestions()
  root.mainloop()