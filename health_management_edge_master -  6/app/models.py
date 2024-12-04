# app/models.py
import os
import pandas as pd
from datetime import datetime
from threading import Thread
from tkinter import messagebox
import time

class HealthManager:
    def __init__(self, name, age, height, weight, activity_level):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.calories_consumed = 0
        self.calories_burned = 0
        self.water_consumed = 0  # Initialize water consumption
        self.medication_schedule = []  # Initialize medication schedule
        self.medication_notifications = True
        self.water_notifications = True
        self.water_popup_active = False  # Track water popup state

        # Use absolute paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, '..', 'data')
        food_file_path = os.path.join(self.data_dir, 'food_calories.xlsx')
        exercise_file_path = os.path.join(self.data_dir, 'exercise_calories.xlsx')
        medication_file_path = os.path.join(self.data_dir, 'medication_schedule.xlsx')
        user_data_file_path = os.path.join(self.data_dir, 'user_data.xlsx')

        self.food_library = pd.read_excel(food_file_path)
        self.exercise_library = pd.read_excel(exercise_file_path)

        # Load medication schedule if it exists
        if os.path.exists(medication_file_path):
            self.medication_schedule = pd.read_excel(medication_file_path).to_dict('records')
        else:
            self.medication_schedule = []

        # Load user data if it exists
        if os.path.exists(user_data_file_path):
            self.user_data = pd.read_excel(user_data_file_path)
        else:
            self.user_data = pd.DataFrame(columns=['Name', 'Weight', 'Calories Consumed', 'Calories Required', 'Calories Burnt', 'Water Consumed'])

    def calculate_bmr(self):
        height_m = self.height / 100  # Convert height to meters
        bmr = (9.65 * self.weight) + (573 * height_m) - (5.08 * self.age) + 260
        return bmr

    def calculate_bmi(self):
        height_m = self.height / 100  # Convert height to meters
        bmi = self.weight / (height_m ** 2)
        if bmi < 18.5:
            status = "Underweight"
        elif 18.5 <= bmi < 24.9:
            status = "Normal"
        elif 25 <= bmi < 29.9:
            status = "Overweight"
        else:
            status = "Obese"
        return bmi, status

    def toggle_medication_notifications(self):
        self.medication_notifications = not self.medication_notifications

    def toggle_water_notifications(self):
        self.water_notifications = not self.water_notifications

    def start_medication_reminders(self):
        def reminder_loop():
            while True:
                now = datetime.now().strftime("%H:%M")
                for med in self.medication_schedule:
                    if med['Time'] == now and self.medication_notifications:
                        messagebox.showinfo("Medication Reminder", f"Time to take {med['Medication']}")
                time.sleep(60)  # Check every minute

        reminder_thread = Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()

    def start_water_reminders(self, interval_minutes=0.3):
        def reminder_loop():
            while True:
                time.sleep(interval_minutes * 60)  # Interval in minutes
                if self.water_notifications and not self.water_popup_active:
                    self.show_water_reminder()
        reminder_thread = Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()

    def show_water_reminder(self):
        self.water_popup_active = True
        messagebox.showinfo("Water Reminder", "Time to log your water intake!")
        self.water_popup_active = False

    def calculate_calories_to_burn(self):
        activity_multipliers = {
            "Little to no exercise": 1.2,
            "Light exercise 1-3 days/week": 1.37,
            "Moderate exercise 3-5 days/week": 1.55,
            "Hard exercise 6-7 days/week": 1.725,
            "Physically demanding job or challenging exercise routine": 1.9
        }
        bmr = self.calculate_bmr()
        daily_calorie_goal = bmr * activity_multipliers[self.activity_level]
        calories_to_burn = max(daily_calorie_goal - self.calories_consumed,
                               0)  # Ensure it doesn't return a negative value
        return calories_to_burn

    def calculate_daily_calorie_intake(self):
        activity_multipliers = {
            "Little to no exercise": 1.2,
            "Light exercise 1-3 days/week": 1.37,
            "Moderate exercise 3-5 days/week": 1.55,
            "Hard exercise 6-7 days/week": 1.725,
            "Physically demanding job or challenging exercise routine": 1.9
        }
        return self.calculate_bmr() * activity_multipliers[self.activity_level]

    def calculate_daily_water_intake(self):
        return self.weight * 0.033

    def calculate_daily_calorie_intake(self):
        return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5

    def calculate_bmi(self):
        height_m = self.height / 100  # Convert height to meters
        bmi = self.weight / (height_m ** 2)
        if bmi < 18.5:
            status = "Underweight"
        elif 18.5 <= bmi < 24.9:
            status = "Normal"
        elif 25 <= bmi < 29.9:
            status = "Overweight"
        else:
            status = "Obese"
        return bmi, status

    def recommended_sleep_time(self):
        return 7

    def add_manual_calories(self, calories):
        self.calories_consumed += calories

    def select_food_from_library(self, food_name):
        food = self.food_library[self.food_library['Food'] == food_name]
        self.calories_consumed += food['Calories'].values[0]

    def add_manual_burned_calories(self, calories):
        self.calories_burned += calories

    def select_exercise_from_library(self, exercise_name, duration):
        exercise = self.exercise_library[self.exercise_library['Exercise'] == exercise_name]
        calories_per_min = exercise['CaloriesPerMin'].values[0]
        self.calories_burned += calories_per_min * duration

    def add_medication(self, name, time):
        time_24hr = datetime.strptime(time, "%I:%M %p").strftime("%H:%M")
        self.medication_schedule.append({'Medication': name, 'Time': time_24hr})
        self.save_medication_schedule()

    def save_medication_schedule(self):
        medication_file_path = os.path.join(self.data_dir, 'medication_schedule.xlsx')
        medication_df = pd.DataFrame(self.medication_schedule)
        medication_df.to_excel(medication_file_path, index=False)

    def save_user_data(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        user_data = {
            'Name': [self.name],
            'Weight': [self.weight],
            'Calories Consumed': [self.calories_consumed],
            'Calories Required': [self.calculate_daily_calorie_intake()],
            'Calories Burnt': [self.calories_burned],
            'Water Consumed': [self.water_consumed]
        }
        user_file_path = os.path.join(self.data_dir, 'user_data.xlsx')
        user_df = pd.DataFrame(user_data)
        user_df.to_excel(user_file_path, index=False)
        self.user_data = pd.read_excel(user_file_path)

    def get_daily_data(self):
        return self.user_data
