from django.test import TestCase
import matplotlib.pyplot as plt
import numpy as np


# Create your tests here.
class Ans():
    def __init__(self, text, votes):
        self.text = text
        self.votes = votes


a1 = Ans('Tak', 8)
a2 = Ans('Nie', 6)
a3 = Ans('Nie', 1)
a4 = Ans('Nie', 8)
a5 = Ans('Nie', 3)
a6 = Ans('Nie', 11)

aList = [a1, a2, a3, a4, a5, a6]
questions = []
votes = []
for a in aList:
    questions.append(a.text)
    votes.append(a.votes)
plt.rcdefaults()
fig, ax = plt.subplots()

# Example data

y_pos = range(0, len(questions))
ax.barh(y_pos, votes)
ax.set_yticks(y_pos, labels=questions)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Głosy')
ax.set_title('Wyniki ankiety')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
# ax.xaxis.set_visible(False)
# ax.yaxis.set_visible(False)
plt.show()
