import pandas as pd
from sklearn.neighbors import NearestNeighbors
from text_to_speech import *

data_dir = "Speech_tictactoe\class_responses.csv"
ClassData = pd.read_csv(data_dir)
student_names = ClassData["Name"].values

ClassDataNums = pd.read_csv(data_dir)  # this stores the data without the names
ClassDataNums = ClassDataNums.drop(["Name"], axis=1)

neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(ClassDataNums)

SpeakText(
    "Welcome to the Friend Locator program, powered by KNN. Follow the prompts to find a friend."
)
SpeakText("On a scale of 1-10, how interested are you in sports?")
sports_interest_value = int(getMove())

SpeakText("On a scale of 1-10, how interested are you in anime and manga?")
anime_interest_value = int(getMove())

SpeakText("On a scale of 1-10, how much do you use Twitter?")
twitter_interest_value = int(getMove())

SpeakText("On a scale of 1-10, how much do you go out?")
going_out_interest_value = int(getMove())

SpeakText("On a scale of 1-10, how much do you like dogs?")
dogs_interest_value = int(getMove())

person_index = neigh.kneighbors(
    [
        [
            sports_interest_value,
            anime_interest_value,
            twitter_interest_value,
            going_out_interest_value,
            dogs_interest_value,
        ]
    ]
)[1][0][0]
SpeakText(
    "Thank you for your input. Based on our magical critically acclaimed match making algorithm, the perfect fit for you from this class is "
    + student_names[person_index]
    + ". Consider approaching them and starting a hopefully great friendship",
)

print(
    "Thank you for your input. Based on our magical critically acclaimed match making algorithm, the perfect fit for you from this class is "
    + student_names[person_index]
    + ". Consider approaching them and starting a hopefully great friendship"
)
