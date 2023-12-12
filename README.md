# This assignment consist of 10 function:
1) first time i was dealing with **PostgreSQL** so few task i completed directly with pandas.
2) i used **logging** library for error handling( to print error it provides a flexible way to log different messages)
3) used render cloud based **PostgreSQL** database.
4) used **.env.local** file to load senstive data like password, host, port, database, connection string etc.
5) used **flake8** for coding style formatting.
6) code can load both **env** and **.env.local** both file i added **env** file.
7) **requirements.txt** i mentioned library in this file.
 
we can access any function using command "**python client.py --step 1**" if you want to run any function so, you have to change step as 1, 2, 3 etc. see below are the steps responsiable to run specific function.
  
  **step_1** to run **upload_movies()** this will upload the movies csv in movies table of database.
  
  **step_2** to run **upload_ratings()** this will upload the ratings csv in rating table of database.
  
  **step_3** to run **Count_of_Movies_with_High_Ratings()**
  
  **step_4** to run **Year_with_Second_Highest_Number_of_Action_Movies()**
  
  **step_5** to run **Highest_Average_Rating_for_a_Movie_Genre_by_Rater_ID_1040()**
  
  **step_6** to run **Favorite_Movie_Genre_of_Rater_ID_1040()**
  
  **step_7** to run **top_Rated_Movie()** In this function i applied filter to choose all records where 'Michael Bay' is in director columns, then to again to filter genre columns as 'Comedy', then to filter records of year 2013, then to filter country India (considered movies with a minimum of 5 ratings)....as result i was geting zero because 'Michael Bay' not directed any movie in india. but if have to print one by one for each condition so **step_10** following same logic.

  
  **step_8** to run **Top_five_Rater_IDs()**. this function following same filter logic as **step_7**
  
  **step_9** to run **Number_of_Unique_Raters()**. 
  
  **step_10** to run **Top_five_Movie_Titles()**.this will filter out top five movies title based on duration, then top five movies based on year of release, average rating (with at least 5 ratings), number of ratings.
