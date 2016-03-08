import os
import sqlite3 as sqlite

from os import listdir
from os.path import isfile, join
import pandas as pd

from pandas.io.sql import to_sql, read_sql

DB_NAME = 'foo.db'
DATA_FOLDER = 'files'

#sets the working directory as the directory the MySqlReader.py file is
os.chdir(os.path.dirname(os.path.realpath(__file__)))
#print os.getcwd()

def delete_db_file():
    os.remove(DB_NAME)
    
def load_db_tables():
    csvfiles = [f for f in listdir(DATA_FOLDER) if isfile(join(DATA_FOLDER, f))]
    
    for csvfile in csvfiles:
        tablename = os.path.splitext(os.path.basename(csvfile))[0]
        #print tablename
        
        DATA_FOLDER+'\\'+csvfile
        df = pd.read_csv(DATA_FOLDER+'\\'+csvfile,sep=',')
       
        coltypes = []
        for col in df.columns:
            coltypes.append(df[col].dtypes)
        
        try:
            conn = sqlite.connect(DB_NAME, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
            sql = "DROP TABLE IF EXISTS %s" % tablename
            conn.execute(sql)
                        
            sql = "CREATE TABLE %s (%s)" % (tablename,", ".join([ "%s %s" % (col, ct) for col, ct  in   zip(df.columns, coltypes) ]))
            print (sql)
            conn.execute(sql)
            df.to_sql(tablename, conn, if_exists='replace', index=False)
            
        except Exception:
            return 'error'
        finally:
            conn.close()            
        
def run_query(q):
    try:
        conn = sqlite.connect(DB_NAME, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
            
        return read_sql(q, conn, index_col=None)
        
    except Exception:
        raise
    finally:
        conn.close()  
    
#load_db_tables()
#
#q = """
#SELECT r.*, p.personnamea
#FROM orders r join persons p on r.personid = p.personid
#LIMIT 10;"""
#run_query(q)        
#
#
#
#dfresult = run_query(q)
#dfresult 
#
#delete_db_file()