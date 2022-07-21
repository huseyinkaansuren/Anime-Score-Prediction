import pulldata
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

def preprocessing(dataframe):
    df = dataframe

    # ---- LABEL ENCODING ----

    le = LabelEncoder()
    genre = df["Genre"]
    genre = le.fit_transform(df["Genre"])
    genre = pd.DataFrame(data=genre, columns=["Genre"])

    # print(genre.head())

    df = df.drop("Genre", axis=1)

    df = pd.concat([df, genre], axis=1)
    # print(df.head())
    #print(df.corr())

    # -------------------
    score_df = df.Score
    # print(score_df.head())

    df = df.drop("Score", axis=1)

    # print(df.head())

    x = df.iloc[:, 2:]
    y = score_df
    X = x.values
    Y = y.values

    # print(x.head())
    # print(y.head())
    return x, y, X, Y
