import pulldata
import datapreprocessing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
import statsmodels.api as sm


pd.set_option("display.max_columns", None)
# pulldata.pull_data()
df = pd.read_csv("Data.csv")
print(df.head())
# print(df.info())
# print(df.corr())
# print(df.isnull().sum())
# print(df.describe())
# print(df[["Genre"]].describe())

# sns.countplot(x="Genre", data=df)
# sns.catplot(x="Genre", y="Ranked", data=df)
# sns.barplot(x="Genre", y="Popularity", data=df)
# sns.distplot(df[(df.Genre=="Action")]["Score"])
# plt.bar(df["Score"], df["Genre"])
# plt.show()

x, y, X, Y = datapreprocessing.preprocessing(df)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, test_size=0.33)

# Linear Regression
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(x_train, y_train)
predict_lr = lr.predict(x_test)

print(r2_score(y_test, predict_lr))

plt.scatter(y_test, predict_lr)
plt.show()

# Backward Elimination Control
X_sm = np.append(arr=np.ones((1000, 1)).astype(int), values=x, axis=1)

x_l = x.iloc[:, [0, 1, 2, 3]].values
x_l = np.array(x_l, dtype=float)
model = sm.OLS(y, x_l).fit()
print(model.summary())

# Polynomial Regression
from sklearn.preprocessing import PolynomialFeatures

poly_reg = PolynomialFeatures(degree=2)
x_poly = poly_reg.fit_transform(X)

x_p_train, x_p_test, y_p_train, y_p_test = train_test_split(x_poly, y, random_state=0, test_size=0.33)
poly_linear = LinearRegression()
poly_linear.fit(x_p_train, y_p_train)
poly_predicts = poly_linear.predict(x_p_test)

plt.scatter(y_test, poly_predicts)
plt.show()

# pred_list = [[28, 72871, 2166, 0]]
# pred_list_df = pd.DataFrame(pred_list, columns=["Ranked"," Popularity", "Members"," Genre"])


poly_r2 = r2_score(y_p_test, poly_predicts)
print(poly_r2)

poly_score = poly_linear.score(x_p_test, y_p_test)
print(poly_score)
