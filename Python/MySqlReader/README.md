MySQLReader
===================
Developed with:
Python 2.7.11 |Anaconda 2.5.0 (64-bit)| (default, Jan 29 2016, 14:26:21) [MSC v.1500 64 bit (AMD64)]


Interface to read files into DB table and run queries on it


* Place csv Files into the "files" folder
* call load_db_tables() to load the files into tables (very few formats supported)
* run query reader.run_query("select * from persons")
* delete DB file if not necessary: delete_db_file()


Output:

```
import MySqlReader as reader

reader.load_db_tables()
CREATE TABLE orders (OrderId int64, PersonId int64, ProductId int64, Amount float64)
CREATE TABLE persons (PersonID int64, PersonName object)
CREATE TABLE products (ProductID int64,  Description object)

persondf = reader.run_query("select * from persons")

reader.delete_db_file()

persondf 
Out[46]: 
   PersonID PersonName
0         1       John
1         2       Paul
2         3       Mary
3         4       karl
```