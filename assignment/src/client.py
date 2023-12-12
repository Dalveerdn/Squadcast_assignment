import main
import logging
from datetime import datetime


def step_1():
  print("Step 1: Running Function: upload_movies")
  main.upload_movies()


def step_2():
  print("Step 2: Running Function: upload_ratings")
  main.upload_ratings()


def step_3():
  print("Step 3: Running Function: Count_of_Movies_with_High_Ratings")
  main.Count_of_Movies_with_High_Ratings()


def step_4():
  print("Step 4: Running Function: Year_with_Second_Highest_Number_of_Action_Movies")
  main.Year_with_Second_Highest_Number_of_Action_Movies()


def step_5():
  print("Step 5: Running Function: Highest_Average_Rating_for_a_Movie_Genre_by_Rater_ID_1040")
  main.Highest_Average_Rating_for_a_Movie_Genre_by_Rater_ID_1040()


def step_6():
  print("Step 6: Running Function: Favorite_Movie_Genre_of_Rater_ID_1040")
  main.Favorite_Movie_Genre_of_Rater_ID_1040()


def step_7():
  print("Step 7: Running Function: top_Rated_Movie")
  main.top_Rated_Movie()


def step_8():
  print("Step 8: Running Function: Top_five_Rater_IDs")
  main.Top_five_Rater_IDs()


def step_9():
  print("Step 9: Running Function: Number_of_Unique_Raters")
  main.Number_of_Unique_Raters()


def step_10():
  print("Step 10: Running Function: Top_five_Movie_Titles")
  main.Top_five_Movie_Titles()


def parent():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("--step", help="step to be choosen for execution")

  args = parser.parse_args()

  eval(f"step_{args.step}()")

  logging.info({
      "last_executed": str(datetime.now()),
      "status": "Pipeline executed successfully",
  })


if __name__ == "__main__":
  parent()
