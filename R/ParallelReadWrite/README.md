ReadMe
===================

* parallel_read:
	1) Given a list of uniqueIdentifiers "uniqueIdentifiers" and an ODBC connection "odbc_connection_name";
	2) Creates X tasks (30 on the code) to call Y insert procedures (50 on the code)

* parallel_read:
	1) Given a list of uniqueIdentifiers "uniqueIdentifiers" and an ODBC connection "odbc_connection_name";
	2) Creates X tasks (4 on the code) to execute Y queries (12 on the code)
	3) Each query selects a random uniqueIdentifier from a pre-defined list and uses it on the where clause (to avoid querying the same thing over and over)
	4) Goes back to step 2
