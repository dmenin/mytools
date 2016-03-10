import os
import sqlite3 as sqlite

from os import listdir
from os.path import isfile, join
import pandas as pd

from pandas.io.sql import read_sql #to_sql


class MySqlReader: 
    
    DB_NAME = ''
    DATA_FOLDER = ''
    
    
    #sets the working directory as the directory the MySqlReader.py file is
    os.chdir(os.path.dirname(os.path.realpath('__file__')))
    #print os.getcwd()
    
    def __init__(self):
       self.DB_NAME = 'foo.db'
       self.DATA_FOLDER = 'files'       
    
    def delete_db_file(self):
        os.remove(self.DB_NAME)
        
    def load_db_tables(self, drop_if_exists=True, print_messages=False):
        """
        loads the files into tables
    
        Parameters
        ----------
        drop_if_exists (default True):
            Whether drop the table if it exists. 
            Use when load_db_tables was called once, a new csv file is needed to be loaded and dont want to reload everything
            If False and table does  exists, ignores error
            
        print_messages: Boolean default False
            whether to print help messages or not  
    
        Returns
        -------
        None
        """
        
        conn = sqlite.connect(self.DB_NAME, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        
        csvfiles = [f for f in listdir(self.DATA_FOLDER) if isfile(join(self.DATA_FOLDER, f))]
        
        try: 
            for csvfile in csvfiles:
                tablename = os.path.splitext(os.path.basename(csvfile))[0]
                if print_messages:
                    print ' '
                    print 'Reading file:', csvfile
                
                self.DATA_FOLDER+'\\'+csvfile
                df = pd.read_csv(self.DATA_FOLDER+'\\'+csvfile,sep=',')
               
                coltypes = []
                for col in df.columns:
                    coltypes.append(df[col].dtypes)
                
                try:
                    if drop_if_exists:
                        sql = "DROP TABLE IF EXISTS %s" % tablename
                        conn.execute(sql)
                    
                    #I could use the "if_exists" and let the data frame create the table
                    #but if I want to load one "extra" table, the append method will reload the data
                    #also having control over the creation gives me more flexibility in case I want to change something in the future
                    sql = "CREATE TABLE %s (%s)" % (tablename,", ".join(
                                        [ "%s %s" % (col, ct) for col, ct in zip(df.columns, coltypes) ]))
                    if print_messages:
                        print (sql)                        
                    conn.execute(sql)
                    
                    #append: If table exists, insert data. Create if does not exist.
                    df.to_sql(tablename, conn, if_exists='append', index=False) 
                except Exception as e:
                    if "already exists" in e.message:
                        print e.message, ". drop_if_exists flag set to False ignores error"
                    else:
                        raise
        finally:
            conn.close()            
            
    def run_query(self,q):
        try:
            conn = sqlite.connect(self.DB_NAME, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
                
            return read_sql(q, conn, index_col=None)
            
        except Exception:
            raise
        finally:
            conn.close()  
            
    def show_tables(self):
        q = """SELECT name as TableName FROM sqlite_master WHERE type='table';"""
        return self.run_query(q)

        
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