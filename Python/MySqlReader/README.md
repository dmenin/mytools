MySQLReader
===================
Developed with:
Python 2.7.11 |Anaconda 2.5.0 (64-bit)| (default, Jan 29 2016, 14:26:21) [MSC v.1500 64 bit (AMD64)]
Depends on: sqlite3, pandas.io.sql 

Interface to read files into DB table and run queries on it


* Place csv Files into the "files" folder
* call load_db_tables() to load the files into tables
* run query reader.run_query("select * from persons")
* delete DB file if dont want to use it again: delete_db_file()


Output:

```
from MySqlReader import MySqlReader 

r = MySqlReader()

r.load_db_tables(drop_if_exists=True, index_first_column=True, print_messages=True)
 
Reading file: orders.csv
CREATE TABLE orders (OrderId int64, PersonId int64, ProductId int64, Amount float64)
CREATE INDEX idxordersOrderId on orders (OrderId)
 
Reading file: persons.csv
CREATE TABLE persons (PersonID int64, PersonName object)
CREATE INDEX idxpersonsPersonID on persons (PersonID)
 
Reading file: products.csv
CREATE TABLE products (ProductID int64, Description object)
CREATE INDEX idxproductsProductID on products (ProductID)

r.show_tables(include_indexes=True)
Out[300]: 
             ObjectName ObjectType TableName
0                orders      table    orders
1      idxordersOrderId      index    orders
2               persons      table   persons
3    idxpersonsPersonID      index   persons
4              products      table  products
5  idxproductsProductID      index  products

q = """
SELECT r.*, p.personname
FROM orders r join persons p on r.personid = p.personid
LIMIT 10;"""

persondf = r.run_query(q)
print persondf 

   OrderId  PersonId  ProductId  Amount PersonName
0        1         1         10  100.37       John
1        2         2         30   50.04       Paul
2        3         4         20   30.50       karl

q = """
select Personid, sum(amount)
from orders
group by PersonId
"""
print r.run_query(q)
   PersonId  sum(amount)
0         1       100.37
1         2        50.04
2         4        30.50

r.delete_db_file()

```