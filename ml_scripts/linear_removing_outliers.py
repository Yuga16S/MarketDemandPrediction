import pandas as pd

import statsmodels.api as sm
from sklearn import *

data_frame_1 = pd.read_csv("/Users/yugapriya/Desktop/MarketDemandPrediction/ml_scripts/newdata.csv")
data_frame_1.drop(data_frame_1[data_frame_1['Area'] != "Nigeria"].index, inplace = True)

data_frame_2 = pd.read_csv("/Users/yugapriya/Desktop/MarketDemandPrediction/ml_scripts/yield.csv")
data_frame_2.drop(data_frame_2[data_frame_2['Area'] != "Nigeria"].index, inplace = True)

def predict(crop, start_year, end_year):
    data_frame = data_frame_1.copy()
    data_frame.drop(data_frame[data_frame['Item'] != crop.crop_code].index, inplace=True)
    data_frame.sort_values("Year", inplace=True)

    if start_year >= 2016:
        predict_year_start_code = ((start_year - 2016) + 56)
    else:
        predict_year_start_code = (56 - (2016 - start_year))

    if end_year >= 2016:
        predict_year_end_code = ((end_year - 2016) + 56)
    else:
        predict_year_end_code = (56 - (2016 - end_year))

    predict_year_codes = []
    for i in range(predict_year_start_code, predict_year_end_code + 1):
        predict_year_codes.append([i])

    stat_year_codes = data_frame[['Year']]
    stat_values = data_frame['Value']

    regr = linear_model.LinearRegression()
    regr.fit(stat_year_codes, stat_values)

    predictions = regr.predict(predict_year_codes)

    return predictions #will be shown to the user

def getChartData(predictions, crop, start_year, end_year):
    data_frame_new = data_frame_1.copy()
    data_frame_new.drop(data_frame_new[data_frame_new['Item'] != crop.crop_code].index, inplace=True)
    data_frame_new.sort_values("Year", inplace=True)

    stat_year_codes = data_frame_new[['Year']]
    stat_values = data_frame_new['Value']

    stat_year_codes = sm.add_constant(stat_year_codes)
    model = sm.OLS(stat_values, stat_year_codes).fit()
    stat_predictions = model.predict(stat_year_codes).values.tolist() #predictions for 1960 - 2016 using sm from new csv

    data_frame_old = data_frame_2.copy()
    data_frame_old.drop(data_frame_old[data_frame_old['Item'] != crop.crop_name].index, inplace=True)
    data_frame_old.sort_values(by=['Year'], inplace=True)

    stat_values = data_frame_old['Value'].values.tolist()
    stat_years = data_frame_old['Year'].values.tolist()
    stat_year_max = data_frame_old['Year'].max()

    years = data_frame_old['Year'].values.tolist()
    for year in range(stat_year_max + 1, end_year + 1):
        # total years, say user selects year range from 2020 - 2023, then it will be from 1961 - 2023
        years.append(year)

    predict_years = []
    for year in range(start_year, end_year + 1):
        predict_years.append(year) # if user selects range 2020-2023, then this will have 2020 - 2023

    predictions_dict = {} # user predictions with year, ie year and value
    index = 0
    for year in predict_years:
        predictions_dict[year] = predictions[index]
        index = index + 1

    values_dict = {}
    index = 0
    for year in stat_years:
        values_dict[year] = stat_predictions[index]
        index = index + 1
    values_dict.update(predictions_dict) # merging 1960 - 2016 and 2020 - 2023

    stat_values_dict = {}
    index = 0
    for year in stat_years:
        stat_values_dict[year] = stat_values[index]
        index = index + 1

    predict_years_str = ','.join(str(predict_year) for predict_year in predict_years)
    stat_years_str = ','.join(str(stat_year) for stat_year in stat_years)
    years_str = ','.join(str(year) for year in years)

    chart_data = {
        "predictions": predictions_dict,
        "predictYears": predict_years_str,
        "statValues": stat_values_dict,
        "statYears": stat_years_str,
        "values": values_dict,
        "years": years_str
    }

    return chart_data


