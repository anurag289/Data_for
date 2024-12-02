# app/scheduler.py
import time
import pandas as pd

class WaterTracker:
    def __init__(self, working_hours):
        self.working_hours = working_hours
        self.water_consumed = 0

    def remind_to_drink_water(self):
        for hour in range(self.working_hours):
            time.sleep(3600)  # Wait for 1 hour
            print("Time to drink water!")

# Usage example
water_tracker = WaterTracker(8)
water_tracker.remind_to_drink_water()

# app/scheduler.py (continued)
class MedicationReminder:
    def __init__(self, schedule_filepath):
        self.schedule = pd.read_excel(schedule_filepath)

    def send_medication_reminders(self):
        # Logic to send reminders based on the schedule
        pass

# Sample Excel data for medication_schedule.xlsx
medication_data = {
    'Medication': ['Medicine A', 'Medicine B'],
    'Time': ['08:00', '14:00']
}
medication_df = pd.DataFrame(medication_data)
medication_df.to_excel('data/medication_schedule.xlsx', index=False)

# app/scheduler.py (continued)
class DietReminder:
    def __init__(self, meal_times):
        self.meal_times = meal_times

    def remind_meal_times(self):
        # Logic to remind meal times
        pass

# Example usage
meal_times = {'Breakfast': '08:00', 'Lunch': '13:00', 'Dinner': '19:00'}
diet_reminder = DietReminder(meal_times)
diet_reminder.remind_meal_times()

# app/scheduler.py (continued)
class ScreenTimeTracker:
    def __init__(self, break_interval=2):
        self.break_interval = break_interval

    def track_screen_time(self):
        time.sleep(self.break_interval * 3600)  # Wait for break_interval hours
        print("Time to take a break!")

# Example usage
screen_time_tracker = ScreenTimeTracker()
screen_time_tracker.track_screen_time()



