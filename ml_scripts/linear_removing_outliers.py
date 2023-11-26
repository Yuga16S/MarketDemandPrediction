import numpy as np
import pandas as pd

import statsmodels.api as sm
from scipy.optimize import curve_fit
from sklearn import *
import numpy

data_frame_1 = pd.read_csv("/Users/yugapriya/Desktop/MarketDemandPrediction/ml_scripts/newdata.csv")
data_frame_1.drop(data_frame_1[data_frame_1['Area'] != "Nigeria"].index, inplace=True)

data_frame_2 = pd.read_csv("/Users/yugapriya/Desktop/MarketDemandPrediction/ml_scripts/yield.csv")
data_frame_2.drop(data_frame_2[data_frame_2['Area'] != "Nigeria"].index, inplace=True)


def predict(crop, start_year, end_year):
    crop_code = crop.crop_code

    data_frame = data_frame_1.copy()
    data_frame.drop(data_frame[data_frame['Item'] != crop_code].index, inplace=True)
    data_frame.drop(data_frame[data_frame['Area'] != "Nigeria"].index, inplace=True)
    data_frame.sort_values("Year", inplace=True)

    data_frame_year_codes = data_frame['Year']
    data_frame_values = data_frame['Value']

    predict_year_start_code = start_year - 1961
    predict_year_end_code = end_year - 1961

    predict_year_codes = []
    for i in range(predict_year_start_code, predict_year_end_code + 1):
        predict_year_codes.append(i)

    if crop_code == 0:
        predictions, existing_predictions = gaussian_outer(predict_year_codes, data_frame_year_codes, data_frame_values)
        return predictions, existing_predictions
    elif crop_code != 5:
        predictions, existing_predictions = polynomial(predict_year_codes, data_frame_year_codes, data_frame_values)
        return predictions, existing_predictions
    else: #Sorghum
        predictions, existing_predictions = gaussian_outer(predict_year_codes, data_frame_year_codes, data_frame_values)
        return predictions, existing_predictions


def polynomial(predict_year_codes, data_frame_year_codes, data_frame_values):
    mymodel = numpy.poly1d(numpy.polyfit(data_frame_year_codes, data_frame_values, 3))
    existing_predictions = mymodel(data_frame_year_codes).astype(int)
    predictions = mymodel(predict_year_codes).astype(int)
    return predictions, existing_predictions


def gaussian_outer(predict_year_codes, data_frame_year_codes, data_frame_values):
    initial_guess = [1, np.mean(data_frame_year_codes), np.std(data_frame_year_codes)]
    params, covariance = curve_fit(gaussian_inner, data_frame_year_codes, data_frame_values, p0=initial_guess, maxfev=1000000)
    A, mu, sigma = params

    # x_fit = np.linspace(min(data_frame_year_codes), max(data_frame_year_codes), 56)
    existing_predictions = gaussian_inner(data_frame_year_codes, A, mu, sigma).values.tolist()

    predicted_values = gaussian_inner(predict_year_codes, A, mu, sigma).astype(int)
    return predicted_values, existing_predictions


def gaussian_inner(data_frame_year_codes, A, mu, sigma):
    return A * np.exp(-(data_frame_year_codes - mu)**2 / (2 * sigma**2))


def get_chart_data(predictions, existing_predictions, crop, start_year, end_year):
    data_frame_new = data_frame_1.copy()
    data_frame_new.drop(data_frame_new[data_frame_new['Item'] != crop.crop_code].index, inplace=True)
    data_frame_new.sort_values("Year", inplace=True)  # df holds data of only the user selected crop

    data_frame_old = data_frame_2.copy()
    data_frame_old.drop(data_frame_old[data_frame_old['Item'] != crop.crop_name].index, inplace=True)
    data_frame_old.sort_values(by=['Year'], inplace=True)

    stat_values = data_frame_old['Value'].values.tolist()
    stat_years = data_frame_old['Year'].values.tolist()
    stat_year_max = data_frame_old['Year'].max()  # max year, 2016

    actual_values = {}
    regression_values = {}
    for year in stat_years:
        try:
            year_code = year - 1961
            actual_values[year] = stat_values[year_code]
            regression_values[year] = existing_predictions[year_code]
        except ValueError:
            print(f"Year {year} not found in stat_years.")

    years = data_frame_old['Year'].values.tolist()
    for year in range(stat_year_max + 1, end_year + 1):
        # total years, say user selects year range from 2020 to 2023, then it will be from 1961 - 2023
        years.append(year)
    years_str = ','.join(str(year) for year in years)

    predict_years = []
    for year in range(start_year, end_year + 1):
        predict_years.append(year)  # if user selects range 2020-2023, then this will have 2020 - 2023

    predictions_dict = {}  # user predictions with year, ie year and value
    index = 0
    for year in predict_years:
        predictions_dict[year] = predictions[index]
        index = index + 1
    predict_values = predictions_dict

    chart_data = {
        "years": years_str,
        "regression_values": regression_values,
        "actual_values": actual_values,
        "predict_values": predict_values
    }

    return chart_data
