from MySqlReader import MySqlReader 

r = MySqlReader()
r.load_db_tables(drop_if_exists=False, print_messages=True)
r.show_tables()

q = """
SELECT r.*, p.personname
FROM orders r join persons p on r.personid = p.personid
LIMIT 10;"""

persondf = r.run_query(q)
print persondf 

q = """
select Personid, sum(amount)
from orders
group by PersonId
"""
r.run_query(q)

r.delete_db_file()