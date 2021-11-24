import pymssql
import csv
import json


connect = pymssql.connect(host=r'',
                          database='AdventureWorks2012',
                          user='',
                          password='')

cursor = connect.cursor()


def read_data_from_json():
    json_file = open('Tables.json', 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DBObjects']




def test_duplicate_values():
    json_file = open('Tables.json', 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DBObjects']

    for i in range(len(json_attr)):
        query = f"select NationalIDNumber, count(*)" \
                    f"from %(SchemaName).(TableName)s" \
                    f"group by NationalIDNumber having count(*) > 1"

        cursor.execute(query, {'SchemaName': json_attr[i].get("SchemaName"), 'TableName': json_attr[i].get("TableName")})
        print(cursor.fetchall())

    #duple_ids = []
    #for r in cursor.fetchall():
    #   duple_ids.append(r)

    #assert len(duple_ids) == 0, f'Ids are not unique: {duple_ids}'


def test_table_exist():
    json_file = open('Tables.json', 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DBObjects']

    for i in range(len(json_attr)):
        query = f"select count(*) as cnt from AdventureWorks2012.INFORMATION_SCHEMA.TABLES " \
                f"where TABLE_NAME = %(TableName)s"
        cursor.execute(query, {'TableName': json_attr[i].get("TableName")})
        print(cursor.fetchall())


def test_metadata():
    json_file = open('Tables.json', 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    json_attr = obj['DBObjects']

    for i in range(len(json_attr)):
        query = f"select COLUMN_NAME, DATA_TYPE from AdventureWorks2012.INFORMATION_SCHEMA.COLUMNS " \
                f"where TABLE_NAME = %(TableName)s"
        cursor.execute(query, {'TableName': json_attr[i].get("TableName")})
        print(cursor.fetchall())
