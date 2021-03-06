#! /usr/bin/env python3
# coding: utf-8
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import math
from mpl_finance import candlestick_ohlc
from sklearn.preprocessing import LabelEncoder
import os
from sklearn.model_selection import cross_val_score
from scipy import stats
from scipy.stats import chisquare
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import recall_score
import pickle

def format_number(s):
	return float(s.replace(',', '.'))

def date_corrector(s):
	return str(s[0:6]+'20'+s[6:8])

def preprocess(df):
	if isinstance(df, int) == False and len(df) != 0:
	    for i in df.columns:
	        if df[i].dtype == 'object':
	            df[i] = df[i].fillna(df[i].mode().iloc[0])
	        elif (df[i].dtype == 'int' or df[i].dtype == 'float'):
	            df[i] = df[i].fillna(np.nanmedian(df[i]))

	    enc = LabelEncoder()
	    for i in df.columns:
	        if (df[i].dtype == 'object'):
	            df[i] = enc.fit_transform(df[i].astype('str'))
	            df[i] = df[i].astype('object')
	else:
		print('empty dataframe')

def connect_to_db(mydb):
	try:
		mycursor = mydb.cursor()
	except:
		print('connection failed')
	return mycursor

def insert_data(mydb,sql,val):
	mycursor = connect_to_db(mydb)
	print(len(val))
	if len(val) != 0:
		try:
			if len(sql) != 0 and isinstance(sql, str) == True:
				mycursor.executemany(sql, val)
				mydb.commit()
				print(mycursor.rowcount, "was inserted.")
			else:
				print('issue in query')
		except:
			print('the insertion failed')
			pass
	else:
		print('the dataframe is empty')
	return 'ok' 

def execute_query(mydb,sql):
	mycursor = connect_to_db(mydb)
	try:
		if len(sql) != 0 and isinstance(sql, str) == True:
			query_output = mycursor.execute(sql)
		else:
			print('issue in query')
	except:
		print(query_output)
	try:
		table_rows = mycursor.fetchall()
		return table_rows
	except:
		print('transforming data failed')

def get_data(mydb, sql, name_dict):
	table_rows = execute_query(mydb,sql)
	try:
		if len(table_rows) > 0:
			df = pd.DataFrame(table_rows)
			df = df.rename(columns=name_dict)
			return df
	except:
		print('formeting failed')
		pass
	else:
		print('the dataframe is empty')
		return 0


def insert_data(mydb,sql,val):
	if len(sql) != 0 and isinstance(sql, str) == True and len(val) > 0 and  isinstance(val, list) == True:
		try:
			mycursor = mydb.cursor()
			mycursor.executemany(sql, val)
			mydb.commit()
			print(mycursor.rowcount, "was inserted.")
			return 'ok'
		except:
			print('insertion failed')
			pass
	else:
		print('sql query not defined')
		pass

def generate_sample(df1,df2):
	if isinstance(df1, pd.DataFrame) == True and len(df1) > 0 :#and  isinstance(df2, pd.DataFrame) == True and len(df2) > 0:
		try:
			SAMPLE_SIZE = min(len(df1),len(df2))
			print(SAMPLE_SIZE)
			SAMPLE_SIZE = min(SAMPLE_SIZE,10000)
			return SAMPLE_SIZE
		except:
			pass
	else:
		print('empty dataframe cannot sample')
		pass

def get_technical_indicators(df):	
	try:
		if isinstance(df, int) == False and len(df) != 0:
			df['ma20'] = df['fft_20_close'].rolling(window=20).mean()
			df['ma50'] = df['fft_20_close'].rolling(window=50).mean()
			#df['ma150'] = df[fft_100].rolling(window=150).mean()
			#df['amd20'] = df[fft_100].ewm(span=20,adjust=False).mean()
			#df['amd50'] = df[fft_100].ewm(span=50,adjust=False).mean()
			#df['var_mma'] = (df['ma50']-df['ma20'])
			#df['var_amd'] = (df['amd50']-df['amd20'])
			# Create MACD
			df['26ema'] = pd.ewma(df['fft_20_close'], span=26)
			df['12ema'] = pd.ewma(df['fft_20_close'], span=12)
			df['MACD'] = (df['12ema']-df['26ema'])
			df['signal'] = pd.ewma(df['MACD'], span=9)
			df['var_macd'] = (df['MACD']-df['signal'])
			# Create Bollinger Bands
			df['20sd'] = pd.stats.moments.rolling_std(df['fft_20_close'],20)
			df['ma21'] = df['fft_20_close'].rolling(window=21).mean()
			df['upper_band'] = df['ma21'] + (df['20sd']*2)
			df['lower_band'] = df['ma21'] - (df['20sd']*2)
			df['var_bollinger'] = df['upper_band']- df['lower_band']
			df['%K'] = STOK(df['fft_20_close'], df['fft_20_low'], df['fft_20_high'], 14)
			df['%D'] = STOD(df['fft_20_close'], df['fft_20_low'], df['fft_20_high'], 14)
			df['var_stoch'] = df['%K'] - df['%D']
			df['var_ema'] = df['26ema'] - df['12ema']
			# Create Exponential moving average
			return df	
		else:
			pritn('empty dataframe')
	except:
		print('empty dataframe')
		pass							


def bollinger_indicator(upper_band,lower_band,fft_20_close):
	if len(upper_band) > 0 and len(lower_band) > 0 and len(fft_20_close) > 0:
		bollinger_indicator = []
		i = 0
		if len(fft_20_close) > 0:
			while i < len(fft_20_close):
				if fft_20_close[i] >= upper_band[i]:
					bollinger_indicator.append(1)
				elif fft_20_close[i] <= lower_band[i]:
					bollinger_indicator.append(-1)
				else:
					bollinger_indicator.append(0)
				i += 1
			return(bollinger_indicator)
		else:
			print('empty fft_20_close')
	else:
		print('empty inputs')

def exctract_label(table_rows,label_list):
	if len(table_rows) != 0:
		i = 0
		while i < len(table_rows):
			label_list.append(table_rows[i][0])
			i += 1
		return label_list
	else:
		print('empty dataframe')

def computeRSI(data, time_window):
	if isinstance(data, int) == False and len(data) != 0 and time_window > 0:
		diff = data.diff(1).dropna()       
		up_chg = 0 * diff
		down_chg = 0 * diff
		up_chg[diff > 0] = diff[ diff > 0 ]
		down_chg[diff < 0] = diff[ diff < 0 ]
		up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
		down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
		rs = abs(up_chg_avg/down_chg_avg)
		rsi = 100 - 100/(1+rs)
		return rsi
	else:
		print('wrong inputs')

def STOK(close, low, high, n): 
	if len(close) > 0 and len(low) > 0 and len(high) > 0 and n > 0:
		STOK = ((close - pd.rolling_min(low, n)) / (pd.rolling_max(high, n) - pd.rolling_min(low, n))) * 100
		return STOK
	else:
		print('wrong imputs')

def STOD(close, low, high, n):
	if len(close) > 0 and len(low) > 0 and len(high) > 0 and n > 0:
		STOK = ((close - pd.rolling_min(low, n)) / (pd.rolling_max(high, n) - pd.rolling_min(low, n))) * 100
		STOD = pd.rolling_mean(STOK, 3)
		return STOD
	else:
		print('wrong imputs')

#to check
def fourier_transform(df,column,fft_20,fft_100):
	if isinstance(df, pd.DataFrame) == True and len(df) > 0 and isinstance(column, str) == True and len(column) > 0 and isinstance(fft_20, list) == True and len(fft_20) == 0 and isinstance(fft_100, list) == True and len(fft_100) == 0:
		try:
			data_ft = df[[column]]
			if isinstance(data_ft, pd.DataFrame) == True and len(data_ft) > 0:
				fft = np.fft.fft(np.asarray(data_ft[column].tolist()))
				fft_df = pd.DataFrame({'fft':fft})
				fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))
				fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))
				plt.figure(figsize=(14, 7), dpi=100)
				fft_list = np.asarray(fft_df['fft'].tolist())
				for num_ in [20,100]:
					if num_ == 20:
						fft_list_m10=np.copy(fft_list); fft_list_m10[num_:-num_]=0
						fft_20.append(list(np.fft.ifft(fft_list_m10).real.tolist()))	
					else:	
						fft_list_m10=np.copy(fft_list); fft_list_m10[num_:-num_]=0
						fft_100.append(list(np.fft.ifft(fft_list_m10).real.tolist()))
				return(fft_df)
			else:
				print('empty dataframe')
		except:
			pass
	else:
		print('empty columns')


def generate_query(sql, input):
	if len(input) != 0 and isinstance(input, str) == True:
		try:
			sql = sql+input
			return sql
		except:
			pass
	else:
		pass

def delete_query(sql,mydb):
	try:
		mycursor = mydb.cursor()
		if len(sql) != 0 and isinstance(sql, str) == True:
			mycursor.execute(sql)
		else:
			pass
	except:
		pass

def labelling_data(label,min_list,max_list):
	i = 0
	if len(label) > 0 and len(min_list) > 0 and len(max_list) > 0:
		while i < len(label):
			if i in min_list:
				label[i] = -1
			elif i in max_list:
				label[i] = 1
			else:
				label[i] = 0
			i += 1
		return label
	else:
		print('empty inputs')
	
def stoch_indicator(k_list,d_list):
	if len(k_list) > 0 and len(d_list) > 0:
		stoch_indicator = [0]
		i = 1
		while i < len(k_list):
			if k_list[i] >= 80 and d_list[i] >= 80:
				if k_list[i-1] >= d_list[i-1] and k_list[i] <= d_list[i]:
					stoch_indicator.append(1)
				else:
					stoch_indicator.append(0)
			elif k_list[i] <= 20 and d_list[i] <= 20:
				if k_list[i-1] <= d_list[i-1] and k_list[i] >= d_list[i]:
					stoch_indicator.append(-1)
				else:
					stoch_indicator.append(0)
			else:
				stoch_indicator.append(0)
			i += 1
		return(stoch_indicator)
	else:
		print('empty inputs')


def ema_indicator(ema_12,ema_26,index,fft_20_close):
	if len(ema_12) > 0 and len(ema_26) > 0 and len(index) > 0 and len(fft_20_close) > 0: 
		ema_indicator = [0]
		i = 1
		while i < len(fft_20_close):
			if ema_12[i-1] < ema_26[i-1] and ema_26[i] < ema_12[i]:
				ema_indicator.append(-1)
			elif ema_26[i-1] < ema_12[i-1] and ema_12[i] < ema_26[i]:
				ema_indicator.append(1)
			else:
				ema_indicator.append(0)
				pass
			i += 1
		return(ema_indicator)
	else:
		print('wrong inputs')


def ks_test(df1, df2, cols):
	if isinstance(df1, int) == False and len(df1) != 0 and isinstance(df2, int) == False and len(df2) != 0 and len(cols) > 0:
		for col in cols:
			ks = stats.ks_2samp(df1[col], df2[col])
			if ks.pvalue < 0.05 and ks.statistic>0.1:
				print(f'{col}: {ks}')
			else:
				print('nothing to display')
	else:
		print('bad formating of the dataframe')

def chi_test(df1, df2, cols):
	if isinstance(df1, int) == False and len(df1) != 0 and isinstance(df2, int) == False and len(df2) != 0 and len(cols) > 0:
		for col in cols:
			cs = chisquare(df1[col].values.tolist(), df2[col].values.tolist())
			if cs.pvalue < 0.05 and cs.statistic>0.1:
				print(f'{col}: {cs}')
			else:
				print('nothing to display')
	else:
		print('bad formating of the dataframe')

def generate_dataset_test(df1, df2):
	if isinstance(df1, int) == False and len(df1) != 0 and isinstance(df2, int) == False and len(df2) != 0:
		df1['source_training'] = 1
		df2['source_training'] = 0
		combined = df2.append(df1)
		combined.reset_index(inplace=True, drop=True)
		combined = combined.reindex(np.random.permutation(combined.index))
		combined.reset_index(inplace=True, drop=True)
		return combined

import matplotlib.pyplot as plt  # doctest: +SKIP
from sklearn import datasets, metrics, model_selection, svm

def random_forest_test(combined,model):
	if isinstance(combined, int) == False and len(combined) != 0: 
		y = combined['source_training'].values
		combined.drop('source_training',axis=1,inplace=True)
		x = combined.values
		lst = []
		for i in combined.columns:
		    score = cross_val_score(model,pd.DataFrame(combined[i]),y,cv=2,scoring='roc_auc')
		    if (np.mean(score) > 0.75):
		        lst.append(i)
		        print(i,np.mean(score))
		return lst
	else:
		print('empty dataframe')


def training_model(train_data_features, y, param_grid):
	if isinstance(train_data_features, pd.DataFrame) == True and len(train_data_features) != 0 and isinstance(y, pd.Series) == True and len(y) != 0 and isinstance(param_grid, dict) == True and len(param_grid) != 0:
		model = RandomForestClassifier(random_state=42)
		model = GridSearchCV(estimator=model, param_grid=param_grid, cv= 5)
		try:
			model = model.fit(train_data_features, y)
			print(model.best_params_)
			params = model.best_params_
			model = RandomForestClassifier(random_state=42, max_features=str(params.get('max_features')), n_estimators= int(params.get('n_estimators')), max_depth=int(params.get('max_depth')), criterion=str(params.get('criterion')))
			model.fit(train_data_features, y)
			return model
		except:
			print('failed to train model')
			pass
	else:
			print('mising dataframe')

def saving_model(model, filename):
	if isinstance(filename, str) == True and len(filename) != 0:
		try:
			pickle.dump(model, open(filename, 'wb'))
			print('saving model as: '+filename)
			return 'model saved'
		except:
			print('failed to save model')
			pass
	else:
		print('missing filename or model')


def scoring_model(model, train_data_features, y, scoring):
	if isinstance(train_data_features, pd.DataFrame) == True and len(train_data_features) != 0 and isinstance(y, pd.Series) == True and len(y) != 0 and isinstance(scoring, list) == True and len(scoring) != 0: 
		try:
			scores = cross_val_score(model, train_data_features, y, cv=5)
			print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
			scores = cross_validate(model, train_data_features, y, scoring=scoring)
			scores_list = (sorted(scores.keys()))
			for score in scores_list:
				print(score)
				print(scores[score])
			return 'scoring done'
		except:
			pass
	else:
		print('missing data or model')


def generate_sets(df, feature_cols):
	if isinstance(feature_cols, list) == True and len(feature_cols) != 0 and isinstance(df, pd.DataFrame) == True and len(df) > 0: 
		try:
			df = df[df.var_bollinger != -100]
			df = df[df.var_stoch != -100]
			df = df[df.RSI != -100]
			train_data_features = df[feature_cols]
			y = df.label 
			return (train_data_features, y)
		except:
			print('failed to exctract the features')
			pass
	else:
		print('missing dataframe or features')

def ema_trade_indicator(ema_12,ema_26,index,fft_20_close,x,y):
	i = 1
	if isinstance(ema_12, list) == True and len(ema_12) != 0 and isinstance(ema_26, list) == True and len(ema_26) > 0: 
		try:
			while i < len(fft_20_close):
				if ema_12[i-1] < ema_26[i-1] and ema_26[i] < ema_12[i]:
					x.append(index[i])
					y.append(fft_20_close[i])
				elif ema_26[i-1] < ema_12[i-1] and ema_12[i] < ema_26[i]:
					x.append(index[i])
					y.append(fft_20_close[i])
				else:
					pass
				i += 1
		except:
			pass


def bollinger_trade_indicator(bollinger,index,fft_20_close,x,y):
	i = 0
	while i < len(fft_20_close):
		if bollinger[i] == 1:
			x.append(index[i])
			y.append(fft_20_close[i])
		elif bollinger[i] == -1:
			x.append(index[i])
			y.append(fft_20_close[i])
		else:
			pass
		i += 1


def rsi_trade_indicator(index,rsi,fft_value,x,y):
	i = 0
	while i < len(rsi):
		if rsi[i] == 1:
			x.append(index[i])
			y.append(fft_value[i])
		elif rsi[i] == -1:
			x.append(index[i])
			y.append(fft_value[i])
		else:
			pass
		i += 1

def stoch_trade_indicator(index,stoch,fft_value,x,y):
	i = 0
	while i < len(stoch):
		if stoch[i] == 1:
			x.append(index[i])
			y.append(fft_value[i])
		elif stoch[i] == -1:
			x.append(index[i])
			y.append(fft_value[i])
		else:
			pass
		i += 1


def rsi_indicator(rsi_list):
	if len(rsi_list)> 0:
		rsi_indicator = []
		i = 0
		while i < len(rsi_list):
			if rsi_list[i] >= 80:
				rsi_indicator.append(1)
			elif rsi_list[i] <= 20:
				rsi_indicator.append(-1)
			else:
				rsi_indicator.append(0)
			i += 1
		return(rsi_indicator)
	else:
		print('empty list')



def compute_macd(var_macd_list,macd):
	i = 0
	while i < len(var_macd_list):
		if var_macd_list[i] > 0:
			macd.append(1)
		elif var_macd_list[i] < 1:
			macd.append(-1)
		else:
			macd.append(0)
		i += 1
	return(macd)    


def compute_mma(var_mma_list,mma):
	i = 0
	while i < len(var_mma_list):
		if var_mma_list[i] > 0:
			mma.append(1)
		elif var_mma_list[i] < 1:
			mma.append(-1)
		else:
			mma.append(0)
		i += 1
	return(mma)

def create_dataframe(MYDB, SQL, NAME_DICT, FEATURES_COLS):
	df = get_data(MYDB, SQL, NAME_DICT)
	if isinstance(df, int) == False and len(df) != 0:
		df = df[FEATURES_COLS]
		return df
	else:
		print('empty dataframe')


def labelCorrection(x):
	if isinstance(x, int) == True:
		if x == 100:
			x = 1
		elif x == 200:
			x = 2
		elif x == -100:
			x = -1
		elif x == -200:
			x = -2
		else:
			x = 0
		return x
	else:
		print('bad input data')
		pass


def check_distribution(size, df1, df2, mode, model, continuous_columns, categorical_columns):
	if isinstance(df1, pd.DataFrame) == True and len(df1) != 0 and isinstance(df2, pd.DataFrame) == True and len(df2) != 0 and isinstance(size, int) == True and size > 0 and isinstance(mode, str) == True and len(mode) > 0: 
		try:
			training_sample = df1.sample(size, random_state=49)
			testing_sample = df2.sample(size, random_state=48)
			if mode == 'lazy':
				ks_test(training_sample, testing_sample, continuous_columns)
				chi_test(training_sample, testing_sample, categorical_columns)
				return 'lazy done'
			elif mode == 'greedy':
				data = generate_dataset_test(training_sample, testing_sample)
				random_forest_test(data, model)
				return 'greedy done'

			else:
				print('cannot compute')
				pass
		except:
			print('empty dataframe')
			pass
	else:
		print('empty dataframe')
		pass

######################
######################
##unused functions kept for documentation ##
#######################
#######################



def format_dataset(stock):
	df = pd.read_csv(stock,delimiter=';')
	df = df.rename(index=str, columns={df.columns[0]:"name",df.columns[1]:"date",df.columns[2]:"open",df.columns[3]:"high",df.columns[4]:"low",df.columns[5]:"close",df.columns[6]:"volume"})
	df.open = list(map(format_number, df.open))
	df.high = list(map(format_number, df.high))
	df.low = list(map(format_number, df.low))
	df.close = list(map(format_number, df.close))
	df.date = list(map(date_corrector,df.date))
	return df


def get_movement(df,fft_100_close):
	i = 1
	close_value = df.fft_100_close.values.tolist()
	pct_close_mvt = [0]
	while i < len(close_value):
		pct_close_mvt.append((fft_100_close[i]-fft_100_close[i-1])/fft_100_close[i-1]*100.0)
	i += 1
	return pct_close_mvt
    
def insert_multiple_into_db(mydb, sql,val):
	#try:
	mycursor = mydb.cursor()
	mycursor.execute(sql, val)
	print(mycursor.rowcount, "record inserted.")
	#except:
	#	print('insertion failed')
	#	pass
	mydb.commit()
	return "1 record inserted."

def generate_momentum(fft,momentum):
	i = 0
	while i < len(fft):
		momentum.append(fft[i]-fft[i-1])
		i += 1
	i = 0
	while i < len(momentum):
		if momentum[i] > 0:
			momentum[i] = 1
		else:
			momentum[i] = 0
	i += 1
	return(momentum)


def get_index(sql,index_list,mydb):
	mycursor = mydb.cursor()
	mycursor.execute(sql)
	table_rows = mycursor.fetchall()
	try:
		index_list.append(table_rows[0][0])
	except:
		pass


def generate_graph(df,u,v,w,x,y,z,s,t):
	fig = plt.figure(figsize = (20, 5))
	plt.title('stochastich chart')
	df.plot(y=['fft_100_close'])
	df.plot(y=['%K', '%D'], figsize = (20, 5))
	plt.axhline(0, linestyle='--', alpha=0.1)
	plt.axhline(20, linestyle='--', alpha=0.5)
	plt.axhline(30, linestyle='--')
	plt.axhline(70, linestyle='--')
	plt.axhline(80, linestyle='--', alpha=0.5)
	plt.axhline(100, linestyle='--', alpha=0.1)
	plt.savefig('stoch.png')

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	plt.title('RSI chart')
	plt.plot(df['index'], df['RSI'])
	plt.axhline(0, linestyle='--', alpha=0.1)
	plt.axhline(20, linestyle='--', alpha=0.5)
	plt.axhline(30, linestyle='--')
	plt.axhline(70, linestyle='--')
	plt.axhline(80, linestyle='--', alpha=0.5)
	plt.axhline(100, linestyle='--', alpha=0.1)
	plt.savefig('rsi.png')
			
	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	plt.scatter(u,v, label='event', color='r', s=25, marker="o")
	#plt.scatter(y,z, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	#plt.plot(df['index'],df['ma20'],label='moving average 20')
	#plt.plot(df['index'],df['ma50'],label='moving average 50')
	#plt.plot(df['index'],df['26ema'],label='moving average 26')
	#plt.plot(df['index'],df['12ema'],label='moving average 12')
	#plt.plot(df['index'],df['lower_band'],label='lower')
	#plt.plot(df['index'],df['upper_band'],label='upper')
	plt.legend()
	plt.savefig('rsi_strat.png', dpi=fig.dpi)

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	plt.scatter(w,x, label='event', color='r', s=25, marker="o")
	#plt.scatter(y,z, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	#plt.plot(df['index'],df['ma20'],label='moving average 20')
	#plt.plot(df['index'],df['ma50'],label='moving average 50')
	#plt.plot(df['index'],df['26ema'],label='moving average 26')
	#plt.plot(df['index'],df['12ema'],label='moving average 12')
	#plt.plot(df['index'],df['lower_band'],label='lower')
	#plt.plot(df['index'],df['upper_band'],label='upper')
	plt.legend()
	plt.savefig('stoch_strat.png', dpi=fig.dpi)

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	#plt.scatter(w,x, label='event', color='r', s=25, marker="o")
	plt.scatter(y,z, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	#plt.plot(df['index'],df['ma20'],label='moving average 20')
	#plt.plot(df['index'],df['ma50'],label='moving average 50')
	plt.plot(df['index'],df['26ema'],label='moving average 26')
	plt.plot(df['index'],df['12ema'],label='moving average 12')
	#plt.plot(df['index'],df['lower_band'],label='lower')
	#plt.plot(df['index'],df['upper_band'],label='upper')
	plt.legend()
	plt.savefig('ema_strat.png', dpi=fig.dpi)

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	#plt.scatter(w,x, label='event', color='r', s=25, marker="o")
	plt.scatter(s,t, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	#plt.plot(df['index'],df['ma20'],label='moving average 20')
	#plt.plot(df['index'],df['ma50'],label='moving average 50')
	#plt.plot(df['index'],df['26ema'],label='moving average 26')
	#plt.plot(df['index'],df['12ema'],label='moving average 12')
	plt.plot(df['index'],df['lower_band'],label='lower')
	plt.plot(df['index'],df['upper_band'],label='upper')
	plt.legend()
	plt.savefig('bollinger_strat.png', dpi=fig.dpi)




	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	#plt.scatter(w,x, label='event', color='r', s=25, marker="o")
	#plt.scatter(y,z, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	plt.plot(df['index'],df['ma20'],label='moving average 20')
	plt.plot(df['index'],df['ma50'],label='moving average 50')
	plt.plot(df['index'],df['26ema'],label='moving average 26')
	plt.plot(df['index'],df['12ema'],label='moving average 12')
	plt.plot(df['index'],df['lower_band'],label='lower')
	plt.plot(df['index'],df['upper_band'],label='upper')
	plt.legend()
	plt.savefig('all.png', dpi=fig.dpi)

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	#plt.scatter(w,x, label='event', color='r', s=25, marker="o")
	#plt.scatter(y,z, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	plt.legend()
	plt.savefig('fourrier.png', dpi=fig.dpi)

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	#plt.scatter(w,x, label='event', color='r', s=25, marker="o")
	#plt.scatter(y,z, label='event', color='g', s=25, marker="o")
	#plt.scatter(u,v, label='event', color='b', s=25, marker="o")
	#plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	#plt.plot(df['index'],df['ma20'],label='moving average 20')
	#plt.plot(df['index'],df['ma50'],label='moving average 50')
	#plt.plot(df['index'],df['26ema'],label='moving average 26')
	#plt.plot(df['index'],df['12ema'],label='moving average 12')
	plt.plot(df['index'],df['lower_band'],label='lower')
	plt.plot(df['index'],df['upper_band'],label='upper')
	plt.legend()
	plt.savefig('bollinger.png', dpi=fig.dpi)

	fig = plt.figure(figsize = (20, 5))
	plt.figure(figsize=(20,5))
	#plt.scatter(y,z, label='event', color='k', s=25, marker="o")
	#plt.plot(df['index'],df['fft_100_close'],label='fft_100_close')
	plt.plot(df['index'],df['fft_20_close'],label='fft_20_close')
	plt.plot(df['index'],df['ma20'],label='moving average 20')
	plt.plot(df['index'],df['ma50'],label='moving average 50')
	plt.legend()
	plt.savefig('ma.png', dpi=fig.dpi)

	ohlc = df[['index', 'fft_100_open', 'fft_100_high', 'fft_100_low', 'fft_100_close']]
	fig = plt.figure(figsize=(20,5))
	fig, ax = plt.subplots()
	candlestick_ohlc(ax, ohlc.values, width=0.4,colorup='w', colordown='k');
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	plt.savefig("ohlc.png")

	fig = plt.figure(figsize=(20,5))
	fig, ax = plt.subplots()
	candlestick_ohlc(ax, ohlc.values[-5:len(df.index.values.tolist())], width=0.4,colorup='w', colordown='k');
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	plt.savefig("ohlc0.png")

	fig = plt.figure(figsize=(20,5))
	fig, ax = plt.subplots()
	candlestick_ohlc(ax, ohlc.values[-1:len(df.index.values.tolist())], width=0.4,colorup='w', colordown='k');
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	plt.savefig("ohlc1.png")

	fig = plt.figure(figsize=(20,5))
	fig, ax = plt.subplots()
	candlestick_ohlc(ax, ohlc.values[-2:len(df.index.values.tolist())], width=0.4,colorup='w', colordown='k');
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	plt.savefig("ohlc2.png")

	fig = plt.figure(figsize=(20,5))
	fig, ax = plt.subplots()
	candlestick_ohlc(ax, ohlc.values[-3:len(df.index.values.tolist())], width=0.4,colorup='w', colordown='k');
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	plt.savefig("ohlc3.png")
	
	plt.close('all')


def prediction_models(df,stock_prices,look_back, epochs, batch_size, model_name):
	stock_prices = df[stock_prices].values.astype('float32')
	stock_prices = stock_prices.reshape(len(stock_prices), 1)
	scaler = MinMaxScaler(feature_range=(0, 1))
	stock_prices = scaler.fit_transform(stock_prices)
	train_size = int(len(stock_prices) * 0.90)
	test_size = len(stock_prices) - train_size
	train, test = stock_prices[0:train_size,:], stock_prices[train_size:len(stock_prices),:]
	print('Split data into training set and test set... Number of training samples/ test samples:', len(train), len(test))
	# convert Apple's stock price data into time series dataset
	trainX, trainY = create_dataset(train, look_back)
	testX, testY = create_dataset(test, look_back)
	# reshape input of the LSTM to be format [samples, time steps, features]
	trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
	testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

	# create and fit the LSTM network
	model = Sequential()
	model.add(LSTM(4, input_shape=(look_back, 1)))
	model.add(Dense(1))
	model.compile(loss='mse', optimizer='adam')
	model.fit(trainX, trainY, nb_epoch=epochs, batch_size=batch_size)

	trainPredict = model.predict(trainX)
	testPredict = model.predict(testX)
	trainPredict = scaler.inverse_transform(trainPredict)
	trainY = scaler.inverse_transform([trainY])
	testPredict = scaler.inverse_transform(testPredict)
	testY = scaler.inverse_transform([testY])
	# calculate root mean squared error
	trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
	print('Train Score: %.2f RMSE' % (trainScore))
	testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
	print('Test Score: %.2f RMSE' % (testScore))

	predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
	# shift predictions of training data for plotting
	trainPredictPlot = np.empty_like(stock_prices)
	trainPredictPlot[:, :] = np.nan
	trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

	# shift predictions of test data for plotting
	testPredictPlot = np.empty_like(stock_prices)
	testPredictPlot[:, :] = np.nan
	testPredictPlot[len(trainPredict)+(look_back*2)+1:len(stock_prices)-1, :] = testPredict

	# plot baseline and predictions
	plt.plot(scaler.inverse_transform(stock_prices))
	plt.plot(trainPredictPlot)
	plt.plot(testPredictPlot)
	plt.show()
	model.save(model_name)
	return(testPredict)


