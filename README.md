# amazon_web_scraper_postgresql_fastapi_on_render
Amazon a web scraper saves data using remote PostgreSQL (on render.com) and you can get the scraped date through fast-API python

# Scaper
  - A web scraper for Amazon items you add the search query (not the link) and it starts collecting the data and navigates through pages automatically

# Database diagram
![diagram](https://github.com/ahmedbfci/amazon_web_scraper_postgresql_fastapi_on_render/assets/13260414/8728270a-61de-40c6-b830-e40c87234ffc)


# Fast-API

  - scrap_item/{item_name}  ->  the scraper start search for {item_name} on Amazon and save the results on remote PostgreSQL. Ex(scrap_item/ipad)
    
  - list_all_items  ->  return all the content of (amazon_item) table in JSON format
  - clear_all_database  ->  clear all the tables (query_result, scraper_query, amazon_item)
    
  - list_all_item_of_scrap/{item_name}  ->  return all the scraped items for previously scrap query
  - list_column/{data_filter}/{column_name}  ->  return only selected column {column_name} of the scraped items for previously scrap query

  - list_all_item/{filter}  ->  return all the with title (LIKE) the {filter} parameter

# Debloyment 

  - How to create a PostgreSQL database (on render.com) [medium](https://medium.com/geekculture/how-to-create-and-connect-to-a-postgresql-database-with-render-and-pgadmin-577b326fd19d)
  - How to deploy the API  watch [this video](https://www.youtube.com/watch?v=JiA-8oVgPIM)

# important 
  - Part of the scraper was inspired by [darshilparmar](https://github.com/darshilparmar) work link to his [repo](https://github.com/darshilparmar/amazon-web-scraping-python-project)
    




