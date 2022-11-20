import pandas as pd
from sklearn.neighbors import NearestNeighbors

data_dir = "Speech_tictactoe\class_responses.csv"
ClassData = pd.read_csv(data_dir)
student_names = ClassData["Name"].values
ClassDataNums = pd.read_csv(data_dir)
ClassDataNums = ClassDataNums.drop(["Name"], axis=1)
neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(ClassDataNums)
person_index = neigh.kneighbors([[2, 5, 2, 1, 9]])[1][0][0]
neigh.kneighbors([[2, 5, 1, 7, 3]])
print(student_names[person_index])
