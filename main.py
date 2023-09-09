# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 19:03:58 2023

@author: AhmedOmar
"""

#fastapi uvicorn psycopg2

import scraper as my_scraper
import database as my_database
from threading import *
import threading
from fastapi import FastAPI
import json


#python -m uvicorn C:\Users\AhmedOmar\spyder_workspace\amazon_scraper\main.py:app --reload



app = FastAPI()

@app.get("/")
async def index():
   return {"message": "Hello World"}

########################################################################
########################################################################

@app.get("/list_all_items")
async def list_all_items():
    try:
        output = my_database.show_item_table("amazon_item")
        if output == "":
            return {"result": "failure"}
        else:
            return {"result": "success", "output":output}
        
    except Exception as error:
        return {"result": "Exception", "details":str(error)}
    
########################################################################
########################################################################


@app.get("/clear_all_database")
async def clear_all_database():
    try:
        my_database.clear_table("query_result")
        my_database.clear_table("scraper_query")
        my_database.clear_table("amazon_item")
        return {"result": "success"}
    except Exception as error:
        return {"result": "Exception", "details":str(error)}

########################################################################
########################################################################

@app.get("/list_all_item/{data_filter}")
async def list_all_item(data_filter):
    try:
        output = my_database.show_table_with_filter("amazon_item",data_filter)
        if output == None:
            return {"result": "failure"}
        else:
            return {"result": "success", "output":output}
    except Exception as error:
        return {"result": "Exception", "details":str(error)}
    
    
########################################################################
########################################################################

@app.get("/list_column/{data_filter}/{column_name}")
async def list_column(data_filter,column_name):
    try:
        output = my_database.show_table_with_filter("amazon_item",data_filter,column_name)
        if output == None:
            return {"result": "failure"}
        else:
            return {"result": "success", "output":output}
    except Exception as error:
        return {"result": "Exception", "details":str(error)}

########################################################################
########################################################################

@app.get("/list_all_item_of_scrap/{data_filter}")
async def list_all_item_of_scrap(data_filter):
    try:
        output = my_database.get_scrap_table_with_filter(data_filter)
        
        if output == None:
            return {"result": "failure"}
        else:
            return {"result": "success", "output":output}
    
    except Exception as error:
        return {"result": "Exception", "details":str(error)}

########################################################################
########################################################################

@app.get("/scrap_item/{item_name}")
async def scrap_item(item_name):
    
    try:
    
        t = threading.Timer(1, my_scraper.get_query,[item_name])
        t.daemon = True
        t.start() 
        
        return {"result": "success"}
    
    except Exception as error:
        return {"result": "Exception", "details":str(error)}


########################################################################
########################################################################
