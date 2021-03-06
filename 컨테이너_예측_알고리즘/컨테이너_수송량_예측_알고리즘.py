# -*- coding: utf-8 -*-
"""컨테이너 수송량 예측 알고리즘.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1II2WqTmNF0MO1pHLPENp6K5H3jlOt4V7
"""

# Import the required library

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro
from scipy import stats
import scipy
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from google.colab import files

# file upload
uploaded = files.upload()

df1=pd.read_excel(io.BytesIO(uploaded['2021.xlsx']))
df2=pd.read_excel(io.BytesIO(uploaded['2020.xlsx']))
df3=pd.read_excel(io.BytesIO(uploaded['2019.xlsx']))

# dataframe information check 

print(df1.info())
print('\n',df1.dtypes,'\n')
df1.head(3)

# dataframe information check 

print(df2.info())
print('\n',df2.dtypes,'\n')
df2.head(3)

# dataframe information check 

print(df3.info())
print('\n',df3.dtypes,'\n')
df3.head(3)

# groupby FT, class. check sum distribution 

def check_sum_distribution(df):
  print(df.groupby([df['FT'],df['class']])['value'].sum())

# groupby FT, class. check avg distribution 

def check_avg_distribution(df):
  print(df.groupby([df['FT'],df['class']])['value'].mean().round(2))

# check distribution - df1

check_sum_distribution(df1)
print('\n-------------------\n')
check_avg_distribution(df1)

# check distribution - df2

check_sum_distribution(df2)
print('\n-------------------\n')
check_avg_distribution(df2)

# check distribution - df3

check_sum_distribution(df3)
print('\n-------------------\n')
check_avg_distribution(df3)

# drop vessel & class - '계'

idx = df1[df1['vessel']=='계'].index
df1.drop(idx, inplace=True)
idx = df1[df1['class']=='계'].index
df1.drop(idx, inplace=True)

idx = df2[df2['vessel']=='계'].index
df2.drop(idx, inplace=True)
idx = df2[df2['class']=='계'].index
df2.drop(idx, inplace=True)

idx = df3[df3['vessel']=='계'].index
df3.drop(idx, inplace=True)
idx = df3[df3['class']=='계'].index
df3.drop(idx, inplace=True)

# labeling
from sklearn import preprocessing

def labeling(df, column):
  le = preprocessing.LabelEncoder()
  le = le.fit(df[column])
  df[column] = le.transform(df[column])
  print(le.classes_)
  le.inverse_transform([0,1])
  return df

labeling(df1, 'class')
labeling(df1, 'vessel')

labeling(df2, 'class')
labeling(df2, 'vessel')

labeling(df3, 'class')
labeling(df3, 'vessel')

# drop unit - FT

def drop_FT(df, column):
  df[column]=df[column].str.split(' ', n=2, expand=True)[0]

drop_FT(df1, 'FT')
drop_FT(df2, 'FT')
drop_FT(df3, 'FT')

# drop FT - '기타'

idx = df1[df1['FT']=='기타'].index
df1 = df1.drop(idx)

idx = df2[df2['FT']=='기타'].index
df2 = df2.drop(idx)

idx = df3[df3['FT']=='기타'].index
df3 = df3.drop(idx)

# check result

print(df1['FT'].unique())
print(df2['FT'].unique())
print(df3['FT'].unique())

# reset index

df1.reset_index(drop=True, inplace=True)
df2.reset_index(drop=True, inplace=True)
df3.reset_index(drop=True, inplace=True)

# check result
print(df1.head(2))
print('\n--------------------\n')
print(df2.head(2))
print('\n--------------------\n')
print(df3.head(2))

"""### Concat DF"""

# concat df
df_conc=pd.concat([df1, df2, df3], axis=0)

# concat check
df_conc

from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(df_conc.drop(['value'],axis=1),df_conc['value'], test_size=0.2)

# reset index - X_train, X_val, y_train, y_val

X_train.reset_index(drop=True, inplace=True)
X_val.reset_index(drop=True, inplace=True)
y_train.reset_index(drop=True, inplace=True)
y_val.reset_index(drop=True, inplace=True)

# model fitting
from sklearn.linear_model import LinearRegression

lir = LinearRegression()
lir.fit(X_train, y_train)

# performance measurement
from sklearn.metrics import mean_absolute_error

pred = lir.predict(X_val)
mae = mean_absolute_error(pred, y_val)

print('mae: ',round(mae,3))

# final result - example test

'''
# [input data info] 1: year, 2: month, 3:vessel, 4: FT, 5:class
  * year - type int64 (ex: 2021)
  * month - type int64 (ex: 9)
  * vessel - ['국적선' '외국선'] = [0, 1]
  * FT - type object (ex: 10)
  * class - ['공' '적'] = [0, 1]

# target : value

# 연동 : predict([[ ]]) 내부에 위의 input data를 해당 규칙에 맞게 넣으면, print의 결과값을 홈페이지에 로드. (궁금한 점 있으면 한소희에게 연락하면 됩니당)
'''

pred=lir.predict([[2021, 9, 0, 40, 1]]).round(2)
print(pred)