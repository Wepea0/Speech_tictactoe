"""
This file contains the program for finding the best possible pair of a user based on their input.
A tictactoe game is played between asking for user input and revealing the results of the algorithm.
"""


import pandas as pd
from sklearn.neighbors import NearestNeighbors
from text_to_speech import *
from tictactoe import *


data_dir = "class_responses.csv"
ClassData = pd.read_csv(data_dir)
student_names = ClassData["Name"].values
ClassDataNums = pd.read_csv(data_dir)  # this stores the data without the names
ClassDataNums = ClassDataNums.drop(["Name"], axis=1)


valid_answers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
REPEAT_INPUT_QUESTION = "Please enter a valid number"


def validate_answer(answer):
    """
    If the answer is in the list of valid answers, return True, otherwise return False

    :param answer: The answer the user gave
    :return: True or False
    """
    if answer in valid_answers:
        return True
    return False


SpeakText(
    "Welcome to the Friend Locator program, powered by KNN. Follow the prompts to find a friend. Only speak when you hear the command Speak Now. Thank you"
)
SpeakText("How many friends would you like to find?")
num_friends = getMove()
while not validate_answer(num_friends):
    SpeakText(REPEAT_INPUT_QUESTION)
    num_friends = getMove()
num_friends = int(num_friends)
neigh = NearestNeighbors(n_neighbors=num_friends)
neigh.fit(ClassDataNums)

SpeakText("Let's get started. Speak only after you hear the command Speak Now.")
SpeakText("On a scale of 1-10, how interested are you in sports?")
sports_interest_value = getMove()
while not validate_answer(sports_interest_value):
    SpeakText(REPEAT_INPUT_QUESTION)
    sports_interest_value = getMove()

sports_interest_value = int(sports_interest_value)

SpeakText("On a scale of 1-10, how interested are you in anime and manga?")
anime_interest_value = getMove()
while not validate_answer(anime_interest_value):
    SpeakText(REPEAT_INPUT_QUESTION)
    anime_interest_value = getMove()

anime_interest_value = int(anime_interest_value)

SpeakText("On a scale of 1-10, how much do you use Twitter?")
twitter_interest_value = getMove()
while not validate_answer(twitter_interest_value):
    SpeakText(REPEAT_INPUT_QUESTION)
    twitter_interest_value = getMove()

twitter_interest_value = int(twitter_interest_value)

SpeakText("On a scale of 1-10, how much do you enjoy going out?")
going_out_interest_value = getMove()
while not validate_answer(going_out_interest_value):
    SpeakText(REPEAT_INPUT_QUESTION)
    going_out_interest_value = getMove()

going_out_interest_value = int(going_out_interest_value)

SpeakText("On a scale of 1-10, how much do you like dogs?")
dogs_interest_value = getMove()
while not validate_answer(dogs_interest_value):
    SpeakText(REPEAT_INPUT_QUESTION)
    dogs_interest_value = getMove()

dogs_interest_value = int(dogs_interest_value)
friends_list = neigh.kneighbors(
    [
        [
            sports_interest_value,
            anime_interest_value,
            twitter_interest_value,
            going_out_interest_value,
            dogs_interest_value,
        ]
    ]
)[1][0]

SpeakText(
    "While our matchmaking elves work on finding the right person for you, let's play a game of Tic Tac Toe."
)
play_game()
SpeakText("Thank you for playing")
SpeakText(
    "Thank you for your input. Based on our magical critically acclaimed match making algorithm, these people fit you perfectly! "
)
for i in friends_list:
    SpeakText(student_names[i])
    print(student_names[i])
SpeakText("Thank you for using the Friend Locator program, powered by KNN.")
