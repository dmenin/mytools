import MySqlReader as reader

reader.load_db_tables()

q = """
SELECT r.*, p.personname
FROM orders r join persons p on r.personid = p.personid
LIMIT 10;"""
  

persondf = reader.run_query(q)

reader.delete_db_file()

print persondf 
