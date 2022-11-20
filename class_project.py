import pandas as pd
from sklearn.neighbors import NearestNeighbors

data_dir = "Speech_tictactoe\class_responses.csv"
ClassData = pd.read_csv(data_dir)
student_names = ClassData["Name"].values

ClassDataNums = pd.read_csv(data_dir)  # this stores the data without the names
ClassDataNums = ClassDataNums.drop(["Name"], axis=1)

neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(ClassDataNums)

sports_interest_value = 0
anime_interest_value = 0
twitter_interest_value = 0
going_out_interest_value = 0
dogs_interest_value = 0
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
print(student_names[person_index])
