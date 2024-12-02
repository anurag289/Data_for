import pandas as pd

food_data = { 'Food': ['Apple', 'Banana', 'Burger', 'Pizza'], 'Calories': [52, 89, 295, 266] }
food_df = pd.DataFrame(food_data)
food_df.to_excel('food_calories.xlsx', index=False)

exercise_data = { 'Exercise': ['Running', 'Cycling', 'Swimming'], 'CaloriesPerMin': [10, 8, 11] }
exercise_df = pd.DataFrame(exercise_data)
exercise_df.to_excel('exercise_calories.xlsx', index=False)

medication_data = { 'Medication': ['Medicine A', 'Medicine B'], 'Time': ['08:00', '14:00'] }
medication_df = pd.DataFrame(medication_data)
medication_df.to_excel('medication_schedule.xlsx', index=False)

user_data = { 'Name': ['John Doe'], 'Weight': [70], 'Calories Consumed': [1500], 'Calories Required': [2000], 'Calories Burnt': [500] }
user_df = pd.DataFrame(user_data)
user_df.to_excel('user_data.xlsx', index=False)