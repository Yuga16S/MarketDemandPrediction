import pandas as pd
#import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
import statsmodels.api as sm

oldData = pd.read_csv("/Users/yugapriya/Desktop/Market_Demand_Prediction/ml_scripts/yield.csv")

def getCrops():
    oldData.sort_values(by=['Item'], inplace=True)
    crops = oldData['Item'].unique()
    return crops
def execute(crop_code, year):
    crop_code = crop_code
    print("year", year)
    user_year = int(year)
    if user_year >= 2016:
        year_to_predict = ((user_year - 2016) + 56)
    else:
        year_to_predict = (56 - (2016 - user_year))
    print("Year to predict", year_to_predict)
    #oldData = pd.read_csv("/Users/yugapriya/Desktop/Market_Demand_Prediction/ml_scripts/yield.csv")
    oldData.sort_values(by=['Item'], inplace=True)
    crops = oldData['Item'].unique()

    #oldData = pd.read_csv("/Users/yugapriya/Desktop/Market_Demand_Prediction/ml_scripts/yield.csv")
    oldData.sort_values(by=['Year'], inplace=True)
    oldData['Year'].unique()

    df = pd.read_csv("/Users/yugapriya/Desktop/Market_Demand_Prediction/ml_scripts/newdata.csv")
    #print(df.head())
    #print(len(df))
    df['Item'].unique()

    len(df)
    #print("test print", df[df['Item'] != crop_code])
    df.drop(df[df['Item'] != crop_code].index, inplace=True)

    len(df)

    df.columns

    x = df[['Year']]
    y = df['Value']


    regr = linear_model.LinearRegression()
    regr.fit(x, y)


    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)


    regr.predict([[year_to_predict]])

    m = regr.coef_
    c = regr.intercept_
    x = 56

    y = m * x + c

    #print(predictions)

    #print("Mean squared error: %.2f" % mean_squared_error(df['Value'], predictions))

    # plt.plot(df['Year'], predictions, color="black")
    # plt.scatter(df['Year'], df['Value'], color="blue")

    #plt.show()

    return y
