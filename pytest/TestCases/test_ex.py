import pymssql
import json


connect = pymssql.connect(host=r'host.docker.internal\SQLEXPRESS',
                          database='AdventureWorks2012',
                          user='sa',
                          password='1ExoticFruit2/')


jsonpath = '../Resources/Tables.json'
reportFile = open('../Report/report.txt', 'w+')

cursor = connect.cursor()


def test_check_null_values():
    json_file = open(jsonpath, 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['NullFieldsCheck']

    for i in range(len(json_attr)):
        query = "select count(*) from {0}.{1} where {2} is null or {3} is null"\
          .format(json_attr[i].get("SchemaName"),
                  json_attr[i].get("TableName"),
                  json_attr[i].get("NotNullField1"),
                  json_attr[i].get("NotNullField2"))

        cursor.execute(query)
        for result in cursor.fetchall():
            if result == (0,):
                reportFile.write("check_null_values test is PASSED\n")
            else:
                reportFile.write(json_attr[i].get("TableName") + " table has NULL values in field(s)\n")


def test_default_values():
    json_file = open(jsonpath, 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DefaultValuesCheck']

    for i in range(len(json_attr)):
        query = "select * from {0}.{1} where {2} not in ({3})"\
            .format(json_attr[i].get("SchemaName"),
                    json_attr[i].get("TableName"),
                    json_attr[i].get("CheckField"),
                    json_attr[i].get("DefaultValues"))

        cursor.execute(query)
        print(cursor.fetchall())

    invalid_val = []
    for r in cursor.fetchall():
        invalid_val.append(r)

    if len(invalid_val) == 0:
        reportFile.write("check_default_values test is PASSED\n")
    else:
        reportFile.write(json_attr[i].get("CheckField") + " field has incorrect value(s)\n")


def test_consistency():
    json_file = open(jsonpath, 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['ConsistencyCheck']

    for i in range(len(json_attr)):
        query = "select * from {0}.{1} t1 left join {0}.{2} t2 on t1.{4} = t2.{4} " \
                "where t2.{5} not in (select {5} from {0}.{3})" \
            .format(json_attr[i].get("SchemaName"),
                    json_attr[i].get("TableName1"),
                    json_attr[i].get("TableName2"),
                    json_attr[i].get("TableName3"),
                    json_attr[i].get("JoinField"),
                    json_attr[i].get("CheckField"))

        cursor.execute(query)

    invalid_val = []
    for r in cursor.fetchall():
        invalid_val.append(r)

    if len(invalid_val) == 0:
        reportFile.write("consistency test is PASSED\n")
    else:
        reportFile.write("Table has incorrect value(s)\n")


def test_duplicate_values():
    json_file = open(jsonpath, 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DBObjects']

    for i in range(len(json_attr)):
        query = "select {2}, count(*) from {0}.{1} group by {2} having count(*) > 1"\
          .format(json_attr[i].get("SchemaName"),
                  json_attr[i].get("TableName"),
                  json_attr[i].get("KeyField"))

        cursor.execute(query)

    duple_ids = []
    for r in cursor.fetchall():
        duple_ids.append(r)

    if len(duple_ids) == 0:
        reportFile.write("duplicate_values test is PASSED\n")
    else:
        reportFile.write(json_attr[i].get("TableName")+" table has duplicates\n")


def test_table_exist():
    json_file = open(jsonpath, 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DBObjects']

    for i in range(len(json_attr)):
        query = "select count(*) as cnt from AdventureWorks2012.INFORMATION_SCHEMA.TABLES " \
                "where TABLE_NAME = %(TableName)s"
        cursor.execute(query, {'TableName': json_attr[i].get("TableName")})

        for output in cursor.fetchall():
            if output == (1,):
                reportFile.write("table_exist test is PASSED\n")
            else:
                reportFile.write(json_attr[i].get("TableName") + " does not exist\n")


def test_metadata():
    query = "select COLUMN_NAME, DATA_TYPE from AdventureWorks2012.INFORMATION_SCHEMA.COLUMNS " \
            "where TABLE_NAME = 'UnitMeasure'"

    cursor.execute(query)
    result = cursor.fetchall()
    if result == [('UnitMeasureCode', 'nchar'), ('Name', 'nvarchar'), ('ModifiedDate', 'datetime')]:
        reportFile.write("Metadata test PASSED")
    else:
        reportFile.write("Metadata test FAILED")
