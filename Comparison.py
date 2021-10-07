import os
import numpy as np
import pandas as pd
import math
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

model = 'Test-1632167988.6723921' # our model
data = pd.read_csv(f'{model}/model-{model}_detailedoutput.csv', header = 0, index_col = 0) # csv with predictions per tile from our model
data_Fu = pd.read_csv('Data/TestSlidesPred_Fu.csv', header = 0) # csv with predictions generated by Fu et al.

slide_dict = {} # dict to store predictions per slide from our model
slide_dict_Fu = {} # dict to store predictions per slide generated by Fu et al.

count = {} # dict to count number of tiles per slide in data

bins = [0.09, 0.29, 0.39, 0.49, 0.59, 0.69, 0.79, 0.89] # list of bins used for our predictions

for idx, row in data.iterrows():

    slide = row[0].split('.')[0] # extract slide name from tile name

    pred = row[1]
    pred = pred[pred.find('[')+1:pred.find(']')].split(', ')
    pred = len(list(filter(lambda x: float(x) > 0.5, pred))) # use a 0.5 cutoff
    pred = bins[pred-1] # get predicted score based on list of bins

    if slide not in slide_dict:
        slide_dict[slide] = 0
        count[slide] = 0

    slide_dict[slide] += pred # add current score prediction to the slide
    count[slide] += 1 # increment the tile count for the slide

for slide in slide_dict:
    slide_dict[slide] /= count[slide] # calculate an average score per slide

trues_dict = {} # dict to store true scores per slide

for idx, row in data_Fu.iterrows():

    slide = row[0]
    pred = row[1]
    true = row[3]

    slide_dict_Fu[slide] = pred
    trues_dict[slide] = true

preds = [] # list to store predictions from our model
preds_Fu = [] # list to store predictions generated by Fu et al.
trues = [] # list to store true scores

for slide in slide_dict_Fu:

    if slide not in slide_dict:
        continue # skip if slide is not present in both datasets

    if math.isnan(slide_dict_Fu[slide]) or math.isnan(trues_dict[slide]):
        continue # skip if prediction or true score is NaN

    preds.append(slide_dict[slide])
    preds_Fu.append(slide_dict_Fu[slide])
    trues.append(trues_dict[slide])

MSE = mean_squared_error(trues, preds)
MSE_Fu = mean_squared_error(trues, preds_Fu)

print('MSE:', round(MSE, 4), 'MSE_Fu:', round(MSE_Fu, 4))

MAE = mean_absolute_error(trues, preds)
MAE_Fu = mean_absolute_error(trues, preds_Fu)

print('MAE:', round(MAE, 4), 'MAE_Fu:', round(MAE_Fu, 4))

print('Total Slides:', len(trues))
