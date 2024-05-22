import random
import csv

file = open("WorldQuiz_Questions.csv", "r")
all_questions = list(csv.reader(file, delimiter=","))
file.close()

# remove first row (headers)
all_questions.pop(0)

# loop 3 times for 3 questions
for item in range(0,3):
  question_list = []
  question_scores = []

  # get 1 question from the csv file
  while len(question_list) < 1:
    # choose question
    chosen_question = random.choice(all_questions)
    index_chosen = all_questions.index(chosen_question)

    # check score is not already in the list
    if chosen_question[2] not in question_scores:
      # add to question list
      question_list.append(chosen_question)

      # remove from master list
      all_questions.pop(index_chosen)

  print("Question: ", question_list)
  print("Question list length: ", len(all_questions))