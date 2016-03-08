import MySqlReader as reader

reader.load_db_tables()

persondf = reader.run_query("select * from persons")

reader.delete_db_file()

persondf 