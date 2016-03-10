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
from MySqlReader import MySqlReader 


r = MySqlReader()

r.load_db_tables(drop_if_exists=False, print_messages=True)
 
Reading file: orders.csv
CREATE TABLE orders (OrderId int64, PersonId int64, ProductId int64, Amount float64)
 
Reading file: persons.csv
CREATE TABLE persons (PersonID int64, PersonName object)
 
Reading file: products.csv
CREATE TABLE products (ProductID int64, Description object)

r.show_tables()
Out[225]: 
  TableName
0    orders
1   persons
2  products

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
r.run_query(q)

Out[227]: 
   PersonId  sum(amount)
0         1       100.37
1         2        50.04
2         4        30.50

r.delete_db_file()
```