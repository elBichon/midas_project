#! /usr/bin/env python3
# coding: utf-8
import mysql.connector
import db_credentials
import pandas as pd
import talib, re  
import numpy as np
import utils


def main():
    pass

if __name__ == "__main__":
	
	MYDB = mysql.connector.connect(
	  host=db_credentials.host,
	  user=db_credentials.user,
	  passwd=db_credentials.passwd,
	  database=db_credentials.database
	) 

	SQL = "SELECT * FROM fourier_processed_stock"
	name_dict = {0:'index',1:'date_of_day', 2:'hour', 3:'numberOfTrades', 4:'name', 5:'volume', 6:'fft_20_close', 7:'fft_20_open', 8:'fft_20_low', 9:'fft_20_high', 10:'fft_100_close', 11:'fft_100_open', 12:'fft_100_low', 13:'fft_100_high'}
	df = utils.get_data(MYDB, SQL, name_dict)
	if isinstance(df, int) == False and len(df) != 0:
		index = df.index.values.tolist()
		ohlc = df[['fft_100_open', 'fft_100_high', 'fft_100_low', 'fft_100_close']]
		O  = np.array(ohlc.fft_100_open,dtype='f8')
		H  = np.array(ohlc.fft_100_high,dtype='f8')
		L   = np.array(ohlc.fft_100_low,dtype='f8')
		C = np.array(ohlc.fft_100_close,dtype='f8')
		  
		cdls = re.findall('(CDL\w*)', ' '.join(dir(talib)))
		for cdl in cdls:  
			toExec = getattr(talib, cdl)  
			out = toExec(np.array(O), np.array(H), np.array(L), np.array(C))  
			df[str(cdl)] = out
			df[str(cdl)] = df[str(cdl)].apply(utils.labelCorrection)

		if isinstance(df, int) == False and len(df) != 0:
			CDL2CROWS = df.CDL2CROWS.values.tolist()
			CDL3BLACKCROWS = df.CDL3BLACKCROWS.values.tolist()
			CDL3INSIDE = df.CDL3INSIDE.values.tolist()
			CDL3LINESTRIKE = df.CDL3LINESTRIKE.values.tolist()
			CDL3OUTSIDE = df.CDL3OUTSIDE.values.tolist()
			CDL3STARSINSOUTH = df.CDL3STARSINSOUTH.values.tolist()
			CDL3WHITESOLDIERS = df.CDL3WHITESOLDIERS.values.tolist()
			CDLABANDONEDBABY = df.CDLABANDONEDBABY.values.tolist()
			CDLADVANCEBLOCK = df.CDLADVANCEBLOCK.values.tolist()
			CDLBELTHOLD = df.CDLBELTHOLD.values.tolist()
			CDLBREAKAWAY = df.CDLBREAKAWAY.values.tolist()
			CDLCLOSINGMARUBOZU = df.CDLCLOSINGMARUBOZU.values.tolist()
			CDLCONCEALBABYSWALL = df.CDLCONCEALBABYSWALL.values.tolist()
			CDLCOUNTERATTACK = df.CDLCOUNTERATTACK.values.tolist()
			CDLDARKCLOUDCOVER = df.CDLDARKCLOUDCOVER.values.tolist()
			CDLDOJI = df.CDLDOJI.values.tolist()
			CDLDOJISTAR = df.CDLDOJISTAR.values.tolist()
			CDLDRAGONFLYDOJI = df.CDLDRAGONFLYDOJI.values.tolist()
			CDLENGULFING = df.CDLENGULFING.values.tolist()
			CDLEVENINGDOJISTAR = df.CDLEVENINGDOJISTAR.values.tolist()
			CDLEVENINGSTAR = df.CDLEVENINGSTAR.values.tolist()
			CDLGAPSIDESIDEWHITE = df.CDLGAPSIDESIDEWHITE.values.tolist()
			CDLGRAVESTONEDOJI = df.CDLGRAVESTONEDOJI.values.tolist()
			CDLHAMMER = df.CDLHAMMER.values.tolist()
			CDLHANGINGMAN = df.CDLHANGINGMAN.values.tolist()
			CDLHARAMI = df.CDLHARAMI.values.tolist()
			CDLHARAMICROSS = df.CDLHARAMICROSS.values.tolist()
			CDLHIGHWAVE = df.CDLHIGHWAVE.values.tolist()
			CDLHIKKAKE = df.CDLHIKKAKE.values.tolist()
			CDLHIKKAKEMOD = df.CDLHIKKAKEMOD.values.tolist()
			CDLHOMINGPIGEON = df.CDLHOMINGPIGEON.values.tolist()
			CDLIDENTICAL3CROWS = df.CDLIDENTICAL3CROWS.values.tolist()
			CDLINNECK = df.CDLINNECK.values.tolist()
			CDLINVERTEDHAMMER = df.CDLINVERTEDHAMMER.values.tolist()
			CDLKICKING = df.CDLKICKING.values.tolist()
			CDLKICKINGBYLENGTH = df.CDLKICKINGBYLENGTH.values.tolist()
			CDLLADDERBOTTOM = df.CDLLADDERBOTTOM.values.tolist()
			CDLLONGLEGGEDDOJI = df.CDLLONGLEGGEDDOJI.values.tolist()
			CDLLONGLINE = df.CDLLONGLINE.values.tolist()
			CDLMARUBOZU = df.CDLMARUBOZU.values.tolist()
			CDLMATCHINGLOW = df.CDLMATCHINGLOW.values.tolist()
			CDLMATHOLD = df.CDLMATHOLD.values.tolist()
			CDLMORNINGDOJISTAR = df.CDLMORNINGDOJISTAR.values.tolist()
			CDLMORNINGSTAR = df.CDLMORNINGSTAR.values.tolist()
			CDLONNECK = df.CDLONNECK.values.tolist()
			CDLPIERCING = df.CDLPIERCING.values.tolist()
			CDLRICKSHAWMAN = df.CDLRICKSHAWMAN.values.tolist()
			CDLRISEFALL3METHODS = df.CDLRISEFALL3METHODS.values.tolist()
			CDLSEPARATINGLINES = df.CDLSEPARATINGLINES.values.tolist()
			CDLSHOOTINGSTAR = df.CDLSHOOTINGSTAR.values.tolist()
			CDLSHORTLINE = df.CDLSHORTLINE.values.tolist()
			CDLSPINNINGTOP = df.CDLSPINNINGTOP.values.tolist()
			CDLSTALLEDPATTERN = df.CDLSTALLEDPATTERN.values.tolist()
			CDLSTICKSANDWICH = df.CDLSTICKSANDWICH.values.tolist()
			CDLTAKURI = df.CDLTAKURI.values.tolist()
			CDLTASUKIGAP = df.CDLTASUKIGAP.values.tolist()
			CDLTHRUSTING = df.CDLTHRUSTING.values.tolist()
			CDLTRISTAR = df.CDLTRISTAR.values.tolist()
			CDLUNIQUE3RIVER = df.CDLUNIQUE3RIVER.values.tolist()
			CDLUPSIDEGAP2CROWS = df.CDLUPSIDEGAP2CROWS.values.tolist()
			CDLXSIDEGAP3METHODS = df.CDLXSIDEGAP3METHODS.values.tolist()

			DF_DICT = {'CDL2CROWS':CDL2CROWS,'CDL3BLACKCROWS':CDL3BLACKCROWS,'CDL3INSIDE':CDL3INSIDE,'CDL3LINESTRIKE':CDL3LINESTRIKE,
		'CDL3OUTSIDE':CDL3OUTSIDE,'CDL3STARSINSOUTH':CDL3STARSINSOUTH,'CDL3WHITESOLDIERS':CDL3WHITESOLDIERS,
		'CDLABANDONEDBABY':CDLABANDONEDBABY,'CDLADVANCEBLOCK':CDLADVANCEBLOCK,'CDLBELTHOLD':CDLBELTHOLD,'CDLBREAKAWAY':CDLBREAKAWAY,
		'CDLCLOSINGMARUBOZU':CDLCLOSINGMARUBOZU,'CDLCONCEALBABYSWALL':CDLCONCEALBABYSWALL,'CDLCOUNTERATTACK':CDLCOUNTERATTACK,
		'CDLDARKCLOUDCOVER':CDLDARKCLOUDCOVER,'CDLDOJI':CDLDOJI,'CDLDOJISTAR':CDLDOJISTAR,'CDLDRAGONFLYDOJI':CDLDRAGONFLYDOJI,
		'CDLENGULFING':CDLENGULFING,'CDLEVENINGDOJISTAR':CDLEVENINGDOJISTAR,'CDLEVENINGSTAR':CDLEVENINGSTAR,
		'CDLGAPSIDESIDEWHITE':CDLGAPSIDESIDEWHITE,'CDLGRAVESTONEDOJI':CDLGRAVESTONEDOJI,'CDLHAMMER':CDLHAMMER,
		'CDLHANGINGMAN':CDLHANGINGMAN,'CDLHARAMI':CDLHARAMI,'CDLHARAMICROSS':CDLHARAMICROSS,'CDLHIGHWAVE':CDLHIGHWAVE,
		'CDLHIKKAKE':CDLHIKKAKE,'CDLHIKKAKEMOD':CDLHIKKAKEMOD,'CDLHOMINGPIGEON':CDLHOMINGPIGEON,'CDLIDENTICAL3CROWS':CDLIDENTICAL3CROWS,
		'CDLINNECK':CDLINNECK,'CDLINVERTEDHAMMER':CDLINVERTEDHAMMER,'CDLKICKING':CDLKICKING,'CDLKICKINGBYLENGTH':CDLKICKINGBYLENGTH,
		'CDLLADDERBOTTOM':CDLLADDERBOTTOM,'CDLLONGLEGGEDDOJI':CDLLONGLEGGEDDOJI,'CDLLONGLINE':CDLLONGLINE,'CDLMARUBOZU':CDLMARUBOZU,
		'CDLMATCHINGLOW':CDLMATCHINGLOW,'CDLMATHOLD':CDLMATHOLD,'CDLMORNINGDOJISTAR':CDLMORNINGDOJISTAR,'CDLMORNINGSTAR':CDLMORNINGSTAR,
		'CDLONNECK':CDLONNECK,'CDLPIERCING':CDLPIERCING,'CDLRICKSHAWMAN':CDLRICKSHAWMAN,'CDLRISEFALL3METHODS':CDLRISEFALL3METHODS,
		'CDLSEPARATINGLINES':CDLSEPARATINGLINES,'CDLSHOOTINGSTAR':CDLSHOOTINGSTAR,'CDLSHORTLINE':CDLSHORTLINE,
		'CDLSPINNINGTOP':CDLSPINNINGTOP,'CDLSTALLEDPATTERN':CDLSTALLEDPATTERN,'CDLSTICKSANDWICH':CDLSTICKSANDWICH,'CDLTAKURI':CDLTAKURI,
		'CDLTASUKIGAP':CDLTASUKIGAP,'CDLTHRUSTING':CDLTHRUSTING,'CDLTRISTAR':CDLTRISTAR,'CDLUNIQUE3RIVER':CDLUNIQUE3RIVER,
		'CDLUPSIDEGAP2CROWS':CDLUPSIDEGAP2CROWS,'CDLXSIDEGAP3METHODS':CDLXSIDEGAP3METHODS}
			df = pd.DataFrame.from_dict(DF_DICT)
			if isinstance(df, int) == False and len(df) != 0:
				SQL = "INSERT INTO candlestick_indicator (CDL2CROWS, CDL3BLACKCROWS, CDL3INSIDE, CDL3LINESTRIKE, CDL3OUTSIDE, CDL3STARSINSOUTH, CDL3WHITESOLDIERS, CDLABANDONEDBABY, CDLADVANCEBLOCK, CDLBELTHOLD, CDLBREAKAWAY, CDLCLOSINGMARUBOZU, CDLCONCEALBABYSWALL, CDLCOUNTERATTACK, CDLDARKCLOUDCOVER, CDLDOJI, CDLDOJISTAR, CDLDRAGONFLYDOJI, CDLENGULFING, CDLEVENINGDOJISTAR, CDLEVENINGSTAR, CDLGAPSIDESIDEWHITE, CDLGRAVESTONEDOJI, CDLHAMMER, CDLHANGINGMAN, CDLHARAMI, CDLHARAMICROSS, CDLHIGHWAVE, CDLHIKKAKE, CDLHIKKAKEMOD, CDLHOMINGPIGEON, CDLIDENTICAL3CROWS, CDLINNECK, CDLINVERTEDHAMMER, CDLKICKING, CDLKICKINGBYLENGTH, CDLLADDERBOTTOM, CDLLONGLEGGEDDOJI, CDLLONGLINE, CDLMARUBOZU, CDLMATCHINGLOW, CDLMATHOLD, CDLMORNINGDOJISTAR, CDLMORNINGSTAR, CDLONNECK, CDLPIERCING, CDLRICKSHAWMAN, CDLRISEFALL3METHODS, CDLSEPARATINGLINES, CDLSHOOTINGSTAR, CDLSHORTLINE, CDLSPINNINGTOP, CDLSTALLEDPATTERN, CDLSTICKSANDWICH, CDLTAKURI, CDLTASUKIGAP, CDLTHRUSTING, CDLTRISTAR, CDLUNIQUE3RIVER, CDLUPSIDEGAP2CROWS, CDLXSIDEGAP3METHODS) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				VAL = [tuple(x) for x in df.values.tolist()]
				if len(VAL) > 0:
					utils.insert_data(MYDB,SQL,VAL)
				else:
					print('no data to insert')
			else:
				print('empty dataframe')
		else:
			print('empty dataframe')
	else:
		print('empty dataframe')



