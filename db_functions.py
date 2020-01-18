import pymysql
import pandas as pd
from sqlalchemy import create_engine
from configuration import config








def save_data_from_csv_format(df):
	try:
		engine = create_engine(config["sql_url"])
		df.to_sql('crawler_result', con=engine, index=False, if_exists='append')
	except:
		df.to_csv('cardata.csv', sep='\t', encoding='utf-8')
