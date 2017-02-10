#Create an empty __init__.py file to specify that the current directory is a package
#All imports in __init__.py are made available when you import the package (directory) that contains it.
#from DataSetAnalyserMain import DataSetAnalyserMain
from tabulate import tabulate  #pretty print

def tabPrint(df):
    print tabulate(df, headers='keys', tablefmt='psql')