*** Settings ***

Library  OperatingSystem
Library  String
Library  DatabaseLibrary
Library  CSVLibrary
Library  JSONLibrary
Library  Collections


*** Variables ***
${dbName}  AdventureWorks2012
${dbUser}  
${dbPass}  
${dbHost}  
${dbPort}  1433

${csv_data_path}  TestData/TableNames.csv
${json_path}  TestData/ForDuplCheck.json