# -*- coding: utf-8 -*-
"""Class Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_tboMbpTlpFms-8MIomdmwIpyMgAuH0t
"""

import pandas as pd
import seaborn as sns
import os

from google.colab import drive 
drive.mount("/content/drive")

data_dir = os.path.abspath('/content/drive/My Drive/Intro to AI/class_responses.csv')

ClassData = pd.read_csv(data_dir)

student_names = ClassData['Name'].values

print(student_names)

ClassDataNums = pd.read_csv(data_dir)

ClassDataNums = ClassDataNums.drop(['Name'], axis=1)

from sklearn.neighbors import NearestNeighbors

neigh = NearestNeighbors(n_neighbors=1)

neigh.fit(ClassDataNums)

person_index = neigh.kneighbors([[2,5,2,1,9]])[1][0][0]

neigh.kneighbors([[2,5,1,7,3]])

print(student_names[person_index])