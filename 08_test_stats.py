#calculate stats into a columm
# heading as first item
def get_stats(total_score, total_questions):
  average = total_score / total_questions

  return[total_questions, total_score, average]

# main routine here
# bg formatting for heading, odd and even rows
head_back = "#FFFFFF"
odd_rows = "#C9D6E8"
even_rows = "yellow"

# user score
user = 15

users_stats = get_stats(user, 20)
row_names = ["", "Score", "Average %"]
row_format = [head_back, odd_rows, even_rows]

# transform stats list, heading and formatting
# into structure that can be used to make labels
all_labels = []

for count, item in enumerate(range(0, len(users_stats))):
  all_labels.append([row_names[item], row_format[count]])
  all_labels.append([users_stats[item], row_format[count]])

print(all_labels)