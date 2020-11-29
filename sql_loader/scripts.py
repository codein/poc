import os
import random
import datetime
import pandas as pd
import sqlite3

import sql_loader
from sql_loader import SQLite_Upsert_Loader_Class

SQL_LOADER_HOME = '~/temp/sql_loader_home'
DB_NAME = 'sql_loader_1.db'
db_path = os.path.expanduser('{0}/{1}'.format(SQL_LOADER_HOME, DB_NAME))


stocks_RHAT_sql_query = '''
SELECT * FROM stocks WHERE symbol=\'RHAT\'
'''

stocks_sql_query = '''
SELECT * FROM stocks
'''

update_sql_query = '''
update stocks set
[qty]='999', [price]='999.0'
where
[date]='2006-04-06' and [trans]='SELL' and [symbol]='RHAT'
'''

def get_db_connection():
    return sql_loader.get_db_connection()

def create_db():

    if os.path.exists(db_path):
      os.remove(db_path)
    with open(db_path, 'w') as fp:
        pass

    conn = get_db_connection()
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE stocks
                 (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()


    symbol = 'RHAT'
    c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

    # Do this instead
    t = ('RHAT',)
    c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    print(c.fetchone())

    # Larger example that inserts many records at a time
    purchases = [
        ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
        ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
        ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
        ('2006-03-28', 'BUY', 'RHAT', 1000, 45.00),
        ('2006-04-05', 'BUY', 'RHAT', 1000, 72.00),
        ('2006-04-06', 'SELL', 'RHAT', 500, 53.00),
    ]
    c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.

    # Save (commit) the changes
    conn.commit()
    conn.close()

def get_all_stocks():
    conn = get_db_connection()
    c = conn.cursor()
    t = ('RHAT',)
    import ipdb; ipdb.set_trace()
    c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    for row in c:
        print(row)


def get_df(sql_query):
    conn = get_db_connection()
    df = pd.read_sql_query(sql_query, conn)
    print(df)
    return df

def to_excel(df, filename):
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer,index=False)
    writer.save()


def get_random_date():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return datetime.datetime.strftime(random_date, '%Y-%m-%d')

def get_random_record():

    trans_types = ['BUY', 'SELL']
    symbols = ['IBM', 'GE', 'TSLA', 'AMZN', 'GOOG', 'DATA', 'FBK', 'BRK', 'SPY', 'TECL']


    record = [
        random.choice(trans_types),
        random.choice(symbols),
        random.randrange(10,1000,10),
        random.uniform(10.5, 100.5),
    ]
    return record

def get_random_stocks_df():
    start_date = datetime.date(2005, 1, 1)
    records = []
    for day in range(2000):
        date = start_date + datetime.timedelta(days=day)
        date_str = datetime.datetime.strftime(date, '%Y-%m-%d')
        record = get_random_record()
        record = [date_str] + record
        records.append(record)
    df = pd.DataFrame(records,columns=['date', 'trans', 'symbol', 'qty', 'price'])
    return df

def export_stocks_table_to_excel():
    df = get_df(stocks_sql_query)
    excel_filename = os.path.expanduser('{0}/{1}'.format(SQL_LOADER_HOME, 'stocks.xlsx'))
    to_excel(df, excel_filename)

if __name__ == '__main__':
    # create_db()
    # get_all_stocks()



    #random 2000 days
    # df = get_random_stocks_df()
    # excel_filename = os.path.expanduser('{0}/{1}'.format(SQL_LOADER_HOME, 'stocks_2000.xlsx'))
    # to_excel(df, excel_filename)

    excel_filename = os.path.expanduser('{0}/{1}'.format(SQL_LOADER_HOME, 'stocks_update_2005_100.xlsx'))
    excel_filename = os.path.expanduser('{0}/{1}'.format(SQL_LOADER_HOME, 'stocks_original_6.xlsx'))
    df = pd.read_excel(excel_filename)
    kwargs = {
        'table_name': 'stocks',
        'primary_keys': ['date', 'trans', 'symbol'],
        'df': df,
        'dry_run': False,
    }
    stocks_loader = SQLite_Upsert_Loader_Class(**kwargs)
    stocks_loader.execute()