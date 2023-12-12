import os
import dotenv
import logging
import psycopg2
import pandas as pd
from sqlalchemy import create_engine


if os.path.exists('.env'):
    dotenv.load_dotenv(".env")
if os.path.exists('.env.local'):
    dotenv.load_dotenv(".env.local")


host = os.getenv('HOST')
database = os.getenv('DATABASE')
passcode = os.getenv('PASSCODE')
username = os.getenv('USER')
port = os.getenv('PORT')
external_connection_string = os.getenv('CON_STRING')

logging.info('envirionment variables loaded successfully!')

connection = psycopg2.connect(external_connection_string)
cursor = connection.cursor()
logging.info('successfully connected to database!')

table_movies = "movies"
table_rating = "rating"


def upload_movies():
  # reading csv using pandas
  df_movie = pd.read_csv('movies.csv')

  # Create an SQLAlchemy engine using the connection string
  engine_movie = create_engine(external_connection_string)
  table_movies = "movies"

  # Upload the DataFrame to the PostgreSQL database
  df_movie.to_sql(table_movies, engine_movie, index=False, if_exists='replace')

  connection.commit()

  print("movies uploaded successfully")


def upload_ratings():
  # reading csv using pandas
  df_rating = pd.read_csv('ratings.csv')

  # Create an SQLAlchemy engine using the connection string
  engine_rating = create_engine(external_connection_string)
  table_rating = "rating"

  # Upload the DataFrame to the PostgreSQL database
  df_rating.to_sql(table_rating, engine_rating, index=False, if_exists='replace')

  connection.commit()

  print("ratings uploaded successfully")


def Count_of_Movies_with_High_Ratings():
  # the query will provide the count of unique movies that have received at least five ratings from the same rater, and the minimum rating given is 7 or higher.
  try:
    sql_query = """
        SELECT COUNT(DISTINCT movie_id) AS count_of_movies_with_high_ratings
    FROM rating
    GROUP BY rater_id
    HAVING COUNT(rating) >= 5 AND MIN(rating) >= 7;
    """
    # Create a cursor
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(sql_query)

    # Fetch all the rows
    result_rows = cursor.fetchall()
    result_rows = [i[0] for i in result_rows]
    print(f"Count of Movies with High Ratings: {len(result_rows)}")
  except Exception as e:
    logging.error("Not found or error encountered", e)


def Year_with_Second_Highest_Number_of_Action_Movies():
  try:
    sql_query = """
      WITH ActionMovies AS (
        SELECT
            movies.year,
            COUNT(*) AS num_action_movies
        FROM
            movies
        JOIN
            rating rating ON movies.id = rating.movie_id
        WHERE
            movies.genre LIKE '%Action%'
            AND movies.country = 'USA'
            AND rating.rating >= 6.5
            AND movies.minutes < 120
        GROUP BY
            movies.year
    )
    SELECT
        year
    FROM
        ActionMovies
    ORDER BY
        num_action_movies DESC
    LIMIT 1 OFFSET 1;
    """

    cursor = connection.cursor()
    cursor.execute(sql_query)
    result_rows = cursor.fetchall()

    print(f"The year with the second-highest number of action movies from the USA with an average rating of 6.5 or higher and a runtime of less than 120 minutes is: {result_rows[0][0]}")
  except Exception as e:
    logging.error("Not found or error encountered", e)


def Highest_Average_Rating_for_a_Movie_Genre_by_Rater_ID_1040():
  try:
    sql_query = """
    WITH GenreRatings AS (
        SELECT
            movies.genre,
            AVG(rating.rating) AS avg_rating,
            COUNT(*) AS num_ratings
        FROM
            rating rating
        JOIN
            movies ON rating.movie_id = movies.id
        WHERE
            rating.rater_id = 1040
        GROUP BY
            movies.genre
        HAVING
            COUNT(*) >= 5
    )
    SELECT
        genre,
        avg_rating
    FROM
        GenreRatings
    ORDER BY
        avg_rating DESC
    LIMIT 1;
    """
    # Create a cursor
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(sql_query)

    # Fetch all the rows
    result_rows = cursor.fetchall()
    print(f"The highest average rating for a movie genre given by rater with ID 1040 is in the genre '{result_rows[0][0]}' with an average rating of {result_rows[0][1]}.")

  except Exception as e:
    logging.error("Not found or error encountered", e)


def Favorite_Movie_Genre_of_Rater_ID_1040():
  # This query retrieves and prints the favorite movie genre for the rater with ID 1040 based on the genre of the movie the rater has rated most often

  try:
    df_movies = pd.read_sql_query(f"SELECT * FROM {table_movies};", connection)
    df_ratings = pd.read_sql_query(f"SELECT * FROM {table_rating};", connection)

    merged_df = pd.merge(df_movies, df_ratings, left_on='id', right_on='movie_id', how='inner')

    filtered_genre = merged_df[
        (merged_df['rater_id'] == 1040)
    ]

    # Count occurrences of each genre in the rater's ratings
    genre_counts = filtered_genre['genre'].value_counts()

    # Find the genre with the highest count
    favorite_genre = genre_counts.idxmax()

    print(f"Favorite_Movie_Genre_of_Rater_ID_1040 is: {favorite_genre}")
  except Exception as e:
    logging.error("Not found or error encountered", e)


def top_Rated_Movie():
  try:
    sql_query = """
    SELECT movies.title, rating.rating
  FROM rating
  JOIN movies ON rating.movie_id = movies.id
  WHERE movies.director LIKE 'Michael Bay'
    AND movies.genre LIKE '%Comedy%'
    AND movies.year = 2013
    AND movies.country LIKE 'India'
    AND rating.rating >= 5
  ORDER BY rating.rating DESC;
    """

    cursor = connection.cursor()
    cursor.execute(sql_query)
    result_rows = cursor.fetchall()

    if len(result_rows) != 0:
      print(f"top-rated Comedy movies of 2013 by 'Michael Bay' in India with minimum rating of 5 is {result_rows[0][0]}")
    else:
      print('Not found')

  except Exception as e:
    logging.error("Not found or error encountered", e)


def Top_five_Rater_IDs():
  # This function query identifies the top 5 rater IDs based on the most movies rated and the highest average rating (considering raters with a minimum of 5 ratings).

  try:
    sql_query = """WITH MoviesRatedCount AS (
    SELECT rater_id, COUNT(DISTINCT movie_id) AS num_movies_rated
    FROM rating
    GROUP BY rater_id
    ORDER BY num_movies_rated DESC
    LIMIT 5
    )

    SELECT mrc.rater_id, AVG(r.rating) AS average_rating
    FROM MoviesRatedCount mrc
    JOIN rating r ON mrc.rater_id = r.rater_id
    GROUP BY mrc.rater_id
    HAVING COUNT(r.rating) >= 5
    ORDER BY average_rating DESC
    LIMIT 5;"""

    cursor = connection.cursor()
    cursor.execute(sql_query)
    result_rows = cursor.fetchall()

    raters_id = [ratersid[0] for ratersid in result_rows]
    average_rating = [str(ratersid[1]).replace('Decimal()', '').replace(')', '') for ratersid in result_rows]

    # datframe
    df = pd.DataFrame(zip(raters_id, average_rating), columns=['raters_id', 'average_rating'])

    print(f"Top 5 raters ID's based on most movies rated are with their highest average rating are:{df}")
  except Exception as e:
    logging.error("Not found or error encountered", e)


def Number_of_Unique_Raters():
  # this function counting the number of unique raters and printing thair ID's.
  try:
    sql_query = """SELECT COUNT(DISTINCT rater_id) AS unique_rater_count
  FROM rating;"""

    cursor = connection.cursor()
    cursor.execute(sql_query)
    result_rows = cursor.fetchall()

    print(f"total count of unique rater IDs: {result_rows[0][0]}")
  except Exception as e:
    logging.error("Not found or error encountered", e)


def Top_five_Movie_Titles():
  # this funtion shorting following columns(minutes, year, rating) and printing their top five movies title based on duration, year of Release, number of ratings given, average rating (consider movies with minimum 5 ratings)

  # top five movies based on duration
  try:
    query_duration = """SELECT title
      FROM movies
      ORDER BY minutes DESC
      LIMIT 5;"""

    cursor = connection.cursor()
    cursor.execute(query_duration)
    result_rows_duration = cursor.fetchall()

    print("top five movies based on duration are:")
    rows_duration = [print(i[0]) for i in result_rows_duration]
  except Exception as e:
    logging.error("Not found or error encountered", e)

  # top five movies based on year of release
  try:
    query_year = """SELECT title
    FROM movies
    ORDER BY year DESC
    LIMIT 5;"""

    cursor = connection.cursor()
    cursor.execute(query_year)
    result_rows_year = cursor.fetchall()

    print("\n top five movies based on year of release are:")
    rows_year = [print(i[0]) for i in result_rows_year]
  except Exception as e:
    logging.error("Not found or error encountered", e)

  # top five movies based on average rating (with at least 5 ratings)
  try:
    query_rating = """SELECT title
    FROM movies
    JOIN (
      SELECT movie_id, AVG(rating) AS avg_rating
      FROM rating
      GROUP BY movie_id
      HAVING COUNT(rating) >= 5
    ) rating ON movies.id = rating.movie_id
    ORDER BY rating.avg_rating DESC
    LIMIT 5;"""

    cursor = connection.cursor()
    cursor.execute(query_rating)
    result_rows_rating = cursor.fetchall()

    print("\n top five movies based on year of release are:")
    rows_rating = [print(i[0]) for i in result_rows_rating]
  except Exception as e:
    logging.error("Not found or error encountered", e)

  # -- Top 5 movies based on number of ratings
  try:
    query_number_rating = """SELECT title
    FROM movies
    JOIN (
      SELECT movie_id, COUNT(rating) AS rating
      FROM rating
      GROUP BY movie_id
    ) rating ON movies.id = rating.movie_id
    ORDER BY rating.rating DESC
    LIMIT 5;"""

    cursor = connection.cursor()
    cursor.execute(query_number_rating)
    result_rows_number_rating = cursor.fetchall()

    print("\n top five movies based on year of release are:")
    number_rating = [print(i[0]) for i in result_rows_number_rating]
  except Exception as e:
    logging.error("Not found or error encountered", e)
