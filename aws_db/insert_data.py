from sqlalchemy import create_engine 
import pandas as pd

def create_db(config):
    
    # setting up the db
    user = config['user'] 
    password = config['password'] 
    host = config['host'] 
    port = config['port'] 
    db_name = config['db_name']
    db_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}" 

    # create engine
    db = create_engine(db_string) 
    return db


def insert_data(csv_fpath, table_name, sep=',', index_col=None):
    
    db = create_db()
    df = pd.read_csv(csv_fpath, sep=sep)
    if index_col:
        df.set_index(index_col, inplace=True)
    df.to_sql(table_name, db)