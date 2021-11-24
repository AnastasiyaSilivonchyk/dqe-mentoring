*** Settings ***
Documentation    Suite description

#Library  DataDriver  ../TestData/TableNames.csv

Resource  ../Resources/variables.robot


Suite Setup  Connect DB
Suite Teardown  Disconnect From Database


*** Test Cases ***
Check NULL values in Employee table
   ${output}  query  select count(*) from Person.Person where FirstName is null or LastName is null
   should be true  '${output[0][0]}'=='0'

Check that there is no PersonType except required for the column
   check if not exists in database  select BusinessEntityID from Person.Person where PersonType not in ('SC', 'IN', 'SP', 'EM', 'VC', 'GC');

Check integrity between Employees and Departments
   row count is 0  select * from HumanResources.Employee e left join HumanResources.EmployeeDepartmentHistory edh on e.BusinessEntityID = edh.BusinessEntityID where edh.DepartmentID not in (select DepartmentID from [HumanResources].[Department]);

Check duplicated values
   row count is 0  select NationalIDNumber, count(*) from HumanResources.Employee group by NationalIDNumber having count(*) > 1

Verify table existance
   @{csv_data}=  read csv file to list    ${csv_data_path}
   FOR  ${TableName}  IN  @{csv_data}
     table must exist  ${TableName}
   END

Check metadata for UnitMeasure table
    ${metadata}  query  select COLUMN_NAME from ${dbName}.INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = 'UnitMeasure'
    should be true  ${metadata}==[('UnitMeasureCode',), ('Name',), ('ModifiedDate',)]


*** Keywords ***
Connect DB
    Connect To Database Using Custom Params  pymssql  database='${dbName}', user='${dbUser}', password='${dbPass}', host='${dbHost}', port=${dbPort}


