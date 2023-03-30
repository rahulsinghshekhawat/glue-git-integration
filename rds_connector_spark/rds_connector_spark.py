from awsglue.utils import getResolvedOptions
import sys
import os
import psycopg2 as ps
import boto3
import datetime
import time 
import random 
import sqlalchemy
import psycopg2 as ps
from pyspark.sql import SparkSession

print(sqlalchemy.__version__)
print(ps.__version__)

print(os.listdir())







import psycopg2
import pandas as pd
from pyspark.sql import SparkSession
from sqlalchemy import create_engine

appName = "PySpark PostgreSQL Example - via psycopg2"
master = "local"

spark = SparkSession.builder.master(master).appName(appName).getOrCreate()

engine_poc1 = create_engine(
    "postgresql+psycopg2://postgres:76417890@database-poc1.cj9l648dhie1.ap-south-1.rds.amazonaws.com/postgres?client_encoding=utf8")

engine_poc2 = create_engine(
    "postgresql+psycopg2://postgres:76417890@database-poc2.cj9l648dhie1.ap-south-1.rds.amazonaws.com/postgres?client_encoding=utf8")

pd_dept = pd.read_sql('select * from employee limit 100000', engine_poc1)
print(type(pd_dept))
print(pd_dept.columns)

# pd_employee = pd.read_sql()

# Convert Pandas dataframe to spark DataFrame
df = spark.createDataFrame(pd_dept)
print(df.schema)
df.show()
df.write.csv("spark_output_employee.csv")
print(os.listdir())

with open("/tmp/spark_output_employee.csv", "rb") as f:
            self.s3.put_object(
                Bucket=self.bucket,
                Body=f,
                Key=f'rds-query-results/spark_outputs/file1.csv'
            )














class rds:
    def __init__(self):
        self.poc1_endpoint = 'database-poc1.cj9l648dhie1.ap-south-1.rds.amazonaws.com'
        self.poc2_endpoint = 'database-poc2.cj9l648dhie1.ap-south-1.rds.amazonaws.com'
        self.poc1_port = '5432'
        self.poc2_port = '5432'
        self.poc1_uname = 'postgres'
        self.poc2_uname = 'postgres'
        self.poc1_password = '76417890'
        self.poc2_password = '76417890'
        self.poc1_database = 'postgres'
        self.poc2_database = 'postgres'

        self.s3 = boto3.client('s3',region_name='ap-south-1')
        self.bucket = 'dummyweb321'
    
    def rds_poc1_connector(self):
        conn = ps.connect(host=self.poc1_endpoint,
                  database=self.poc1_database,
                  user=self.poc1_uname,
                  password=self.poc1_password,
                  port=self.poc1_port)
        conn.autocommit = True
        cur = conn.cursor()
        return cur

    def rds_poc2_connector(self):
        conn = ps.connect(host=self.poc2_endpoint,
                  database=self.poc2_database,
                  user=self.poc2_uname,
                  password=self.poc2_password,
                  port=self.poc2_port)
        conn.autocommit = True
        cur = conn.cursor()
        return cur


    def get_dept_ids(self, sql_query, cur):
        # cur = self.rds_poc2_connector()
        cur.execute(sql_query)
        lst = cur.fetchall()

        dept_ids = []
        for i in range(len(lst)):
            dept_ids.append(lst[i][0])
        return tuple(dept_ids)
    
    def save_query_results_to_3(self, sql_query, glue_dir, p_filename):
        cur = self.rds_poc1_connector()
        print(os.listdir())
        cur.execute(sql_query)
        print(cur.fetchall())
        sql = f"COPY ({sql_query}) TO STDOUT WITH CSV DELIMITER ','"
        with open(f"{glue_dir}/{p_filename}", "w") as file:
            cur.copy_expert(sql, file)
        print(os.listdir())
        with open(f"{glue_dir}/{p_filename}", "rb") as f:
            self.s3.put_object(
                Bucket=self.bucket,
                Body=f,
                Key=f'rds-query-results/{p_filename}'
            )
    
    

# if __name__ == '__main__':
#     rds1 = rds()
#     cur1 = rds1.rds_poc1_connector()
#     cur2 = rds1.rds_poc2_connector()
#     q = 'select dept_id from dept limit 20;'
#     dept_ids = rds1.get_dept_ids(q,cur2)
#     sql_query = f'select * from employee where dept_id in {dept_ids} limit 20000'
#     print(sql_query)
    
#     file_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d - %H-%M-%S')
#     glue_dir = '/tmp'
#     p_filename = f'{file_date}'+'_table.csv'
#     rds1.save_query_results_to_3(sql_query,glue_dir,p_filename)
