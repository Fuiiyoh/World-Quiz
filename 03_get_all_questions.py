import csv

file = open("WorldQuiz_Questions.csv", "r")
all_questions = list(csv.reader(file, delimiter=","))
file.close()

# remove first row (headers)
all_questions.pop(0)

# get the first 15 rows
# (used to generate questions and answers for Play GUI)
print(all_questions[:15])

print("Lenght of all_questions: {}".format(len(all_questions)))