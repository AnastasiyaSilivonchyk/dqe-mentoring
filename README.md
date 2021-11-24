# DQE_Mentoring
To run tests in robot framework
		install robotframework via pip
		install robotframework-databaselibrary package
        install robotframework-csvlibrary-py3 (for python less than 3 use robotframework-csvlibrary)
		add runer as robotframework in Run Configuration from Templates
		put creds to establish connection
		
To run tests in pytest
		install pytest
		install pymssql for DB connection
		put creds to establish connection
		add runer as pytest in Run Configuration from Templates

Project structure
		Robot Framework:
		  Resources folder contains files with variables and common keywords
		  TestCases folder contains executed files with tests
		  TestData folder contains .csv, .json files with data need for tests (ex. input parameters for sql queries)
		
		PyTest:
		  Resources folder contains .json files with data need for tests (ex. input parameters for sql queries)
		  TestCases folder contains executed files with tests
	
Reporting
		Robot Framework:
		Has build-in report that can be opened in any browser by report.html file that is in root project folder
		
		PyTest:
		Test results are in report.txt file in pytest\Report\report.txt

		
