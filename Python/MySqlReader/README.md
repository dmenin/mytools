MySQLReader
===================

Interface to read files into DB table and run queries on it


Place csv Files into the "files" folder
call load_db_tables() to load the files into tables (very few formats supported)
run query reader.run_query("select * from persons")
delete DB file if not necessary: delete_db_file()