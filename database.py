# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:06:25 2023

@author: AhmedOmar
"""


import psycopg2
from configparser import ConfigParser
import json


conn = None
scrapper_conn = None
DATABASE_URL = 'postgres://scraper_postgresql_user:6c8QKNK5p3eXuOI42MSR6GwhCk1x6hTj@dpg-cjtndm1gdgss738f4t60-a/scraper_postgresql'


def init_database():
    global conn
    
    try:
        if conn == None:
            conn = psycopg2.connect(DATABASE_URL)
            connect()
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("init_database "+str(error))
    print("pass -- init_database")


########################################################################
########################################################################
########################################################################


def init_scrapper_database():
    global scrapper_conn
    
    try:
        if scrapper_conn == None:
            scrapper_conn = psycopg2.connect(DATABASE_URL)
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("init_database "+str(error))
    print("pass -- init_database")


########################################################################
########################################################################
########################################################################

def connect():
    global conn
    
    
		
    commands = (
        """
        CREATE TABLE IF NOT EXISTS scraper_query (
        query_id SERIAL PRIMARY KEY,
        query_data VARCHAR(255) NOT NULL,
        created_at TIME DEFAULT CURRENT_TIME,
        created_on DATE DEFAULT CURRENT_DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS amazon_item (
        id SERIAL PRIMARY KEY,
        amazon_id VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        price NUMERIC(5,2),
        rating VARCHAR(255),
        reviews VARCHAR(255),
        availability VARCHAR(255),
        url TEXT NOT NULL
        )""",
        """
        CREATE TABLE IF NOT EXISTS query_result (
        query_result_id SERIAL PRIMARY KEY,
        query_id INTEGER NOT NULL,
        amazon_item_id INTEGER NOT NULL,
        
        CONSTRAINT fk_customer_1
        FOREIGN KEY(query_id) 
    	REFERENCES scraper_query(query_id)
    	ON DELETE CASCADE,
        
        CONSTRAINT fk_customer_2
        FOREIGN KEY(amazon_item_id) 
    	REFERENCES amazon_item(id)
    	ON DELETE CASCADE
        )
        """)  #,"""DROP TABLE amazon_item;"""
        
    
    try:
        
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("connect "+str(error))
    
    print("pass -- connect")

########################################################################
########################################################################
########################################################################

def insert_query(query):
    
    sql = "select query_id from scraper_query WHERE query_data = \'"+query+"\';"
    
    query_id = None
    try:
        
        # create a new cursor
        cur = scrapper_conn.cursor()
        cur.execute(sql)
        
        
        result = cur.fetchone()
        
        if result:
        
            
            # commit the changes to the database
            scrapper_conn.commit()
            
            # close communication with the database
            cur.close()
            
            return None
        else:
            
            sql = """INSERT INTO scraper_query(query_data) VALUES(%s) RETURNING query_id;"""
            
            # execute the INSERT statement
            cur.execute(sql, (query,))
            # get the generated id back
            query_id = cur.fetchone()[0]
            # commit the changes to the database
            scrapper_conn.commit()
            # close communication with the database
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("insert_query  "+str(error))

    return query_id


########################################################################
########################################################################
########################################################################


def insert_amazon_item(amazon_id, title, price, rating, reviews, availability, url):
    
    
    sql = "select id from amazon_item WHERE amazon_id = \'"+amazon_id+"\';"
    id= None
    
    
    try:
        
        # create a new cursor
        cur = scrapper_conn.cursor()
        cur.execute(sql)
        
        
        result = cur.fetchone()
        
        if result:
        
            
            # commit the changes to the database
            scrapper_conn.commit()
            
            # close communication with the database
            cur.close()
            
            return result[0]
            
        else:
            
            sql = """INSERT INTO amazon_item(amazon_id,title,price,rating,reviews,availability,url)
                     VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            id = None
        
            # execute the INSERT statement
            cur.execute(sql, (amazon_id, title, price, rating, reviews, availability, url,))
            
            # get the generated id back
            id = cur.fetchone()[0]
             
            # commit the changes to the database
            scrapper_conn.commit()
            
             
            # close communication with the database
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("insert_amazon_item "+str(error))

    return id


########################################################################
########################################################################
########################################################################


def insert_query_result(query_id, amazon_item_id):
    
    
    sql = """INSERT INTO query_result(query_id,amazon_item_id)
             VALUES(%s,%s) RETURNING query_result_id;"""
    query_result_id = None
    try:
        
        # create a new cursor
        cur = scrapper_conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (query_id,amazon_item_id,))
        # get the generated id back
        query_result_id = cur.fetchone()[0]
        # commit the changes to the database
        scrapper_conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("insert_query_result "+str(error))
 
    return query_result_id


########################################################################
########################################################################
########################################################################


def clear_table(table_name):
    
    #sql = "TRUNCATE TABLE "+table_name+" RESTART IDENTITY;"
    sql = "DELETE FROM "+table_name+";"
    try:
        if conn == None:
            init_database()
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("clear_table "+str(error))
    finally:
        close_connection()
        
        
        
########################################################################
########################################################################
########################################################################


def show_item_table(table_name):
    
    #sql = "TRUNCATE TABLE "+table_name+" RESTART IDENTITY;"
    sql = "select * from "+table_name+";"
    
    my_dict = []
    
    jsondict =None
    
    try:
        
        if conn == None:
            init_database()
        
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        
        
        for item in cur.fetchall():
            json_item = row_to_json(item)
            if json_item != "":
                my_dict.append(json_item)
        
        # close communication with the database
        cur.close()
        
        jsondict = json.dumps(my_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print("show_table "+str(error))
    finally:
        close_connection()
        
    return jsondict
 


        
########################################################################
########################################################################
########################################################################


def show_table_with_filter(table_name, data_filter, column_name = ""):
    
    #sql = "TRUNCATE TABLE "+table_name+" RESTART IDENTITY;"
    print("show_table_with_filter  1")
    sql = ""
    if column_name == "":
        print("show_table_with_filter  2")
        sql = "select * from "+table_name+" WHERE title LIKE '%"+str(data_filter)+"%';"
    else:
        print("show_table_with_filter  3")
        sql = "select "+column_name+" from "+table_name+" WHERE title LIKE '%"+str(data_filter)+"%';"
    
    my_dict = []
    
    jsondict =None
    
    try:
        
        if conn == None:
            init_database()
            
        print("show_table_with_filter  4")
        
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
            
        print("show_table_with_filter  5")
        
        if column_name == "":
                
            print("show_table_with_filter  6")
        
            for item in cur.fetchall():
                
                print("show_table_with_filter  6  1")
                json_item = row_to_json(item)
                
                print("show_table_with_filter  6  2")
                if json_item != "":
                    print("show_table_with_filter  6  3")
                    my_dict.append(json_item)
        else:    
            print("show_table_with_filter  7")
            my_dict = cur.fetchall()
        
        # close communication with the database
        cur.close()
        
        jsondict = json.dumps(my_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print("show_table_with_filter "+str(error))
    finally:
        close_connection()
        
    return jsondict


########################################################################
########################################################################
########################################################################


def get_scrap_table_with_filter(data_filter):
    
    sql = "select * from amazon_item WHERE id IN (select amazon_item_id from query_result WHERE query_id IN (select query_id from scraper_query WHERE query_data = \'"+str(data_filter)+"\'));"
    
    my_dict = []
    
    jsondict =None
    
    try:
        
        if conn == None:
            init_database()
        
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        
        
        for item in cur.fetchall():
            json_item = row_to_json(item)
            if json_item != "":
                my_dict.append(json_item)
        
        # close communication with the database
        cur.close()
        
        jsondict = json.dumps(my_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print("get_scrap_table_with_filter "+str(error))
    finally:
        close_connection()
        
    return jsondict


########################################################################
########################################################################
########################################################################

def row_to_json(split_data):
    
    try:
        
        #new_data = data[1:-1]
        #new_data = data
        
        
        #split_data = new_data.split(", ")
        
        price = str(split_data[3])#.replace("Decimal(").replace(")")
        
        
    
        
        json_result = {"amazon_id":split_data[1],"title":split_data[2],"price":price,"rating":split_data[4],
                       "reviews":split_data[5],"availability":split_data[6],"url":split_data[7]}
        
            
    except (Exception, psycopg2.DatabaseError) as error:
        print("row_to_json "+str(error) +"    ---    "+str(split_data))
        json_result = ""
        
    return json_result
      
########################################################################
########################################################################
########################################################################


def show_table(table_name):
    
    #sql = "TRUNCATE TABLE "+table_name+" RESTART IDENTITY;"
    sql = "select * from "+table_name+";"
    
    my_dict = []
    
    jsondict =""
    
    try:
        
        if conn == None:
            init_database()
        
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        
        
        for item in cur.fetchall():
            print("-- "+str(item))
        
        # close communication with the database
        cur.close()
        
        jsondict = json.dumps(my_dict)
    except (Exception, psycopg2.DatabaseError) as error:
        print("show_table "+str(error))
    finally:
        close_connection()
        
    return jsondict
 
########################################################################
########################################################################
########################################################################

def close_connection():
    global conn
    
    try:
        if conn != None:
            conn.close()
            conn = None
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
       
########################################################################
########################################################################
########################################################################

def close_scrapper_connection():
    global scrapper_conn
    
    try:
        if scrapper_conn != None:
            scrapper_conn.close()
            scrapper_conn = None
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 
        
