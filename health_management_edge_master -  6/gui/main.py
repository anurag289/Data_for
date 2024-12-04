# gui/main.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from app.models import HealthManager
from threading import Thread
import time
from tkinter import messagebox
from datetime import datetime
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import win32api


class BreakManager:
    def __init__(self):
        self.active_time = 0
        self.check_interval = 60  # Check every minute
        self.break_interval = 0.3 * 60  # Suggest a break every 30 minutes
        self.break_duration = 2 * 60  # 2 minutes break
        self.break_notifications = True
        self.break_popup_active = False  # Track break popup state

    def toggle_break_notifications(self):
        self.break_notifications = not self.break_notifications

    def track_activity(self):
        while True:
            if self.is_user_active():
                self.active_time += self.check_interval
                if self.active_time >= self.break_interval and not self.break_popup_active:
                    self.show_break_reminder()
                    self.active_time = 0  # Reset active time after showing reminder
            else:
                self.active_time = 0  # Reset active time if user is inactive
            time.sleep(self.check_interval)

    def toggle_break_notifications(self):
        self.break_notifications = not self.break_notifications

    def is_user_active(self):
        # Check if the system is idle or locked
        idle_time = win32api.GetTickCount() - win32api.GetLastInputInfo()
        if idle_time > (self.check_interval * 1000):
            return False
        return True

    def show_break_reminder(self):
        self.break_popup_active = True
        def close_popup():
            self.break_popup_active = False
        messagebox.showinfo("Break Time", f"Time to take a break! Stand up and stretch for {self.break_duration // 60} minutes.")
        close_popup()

    def suggest_break(self):
        messagebox.showinfo("Break Time", f"Time to take a break! Stand up and stretch for {self.break_duration // 60} minutes.")


class HealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Management App")
        self.root.geometry("950x600")

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=6)
        self.style.configure('TEntry', font=('Helvetica', 12))

        self.manager = None
        self.create_initial_setup()

    def create_initial_setup(self):
        self.setup_frame = ttk.Frame(self.root)
        self.setup_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.setup_frame, text="Enter your details", font=('Helvetica', 14, 'bold')).pack(pady=10)

        ttk.Label(self.setup_frame, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.setup_frame)
        self.name_entry.pack()

        ttk.Label(self.setup_frame, text="Age:").pack(pady=5)
        self.age_entry = ttk.Entry(self.setup_frame)
        self.age_entry.pack()

        ttk.Label(self.setup_frame, text="Height (cm):").pack(pady=5)
        self.height_entry = ttk.Entry(self.setup_frame)
        self.height_entry.pack()

        ttk.Label(self.setup_frame, text="Weight (kg):").pack(pady=5)
        self.weight_entry = ttk.Entry(self.setup_frame)
        self.weight_entry.pack()

        ttk.Label(self.setup_frame, text="Activity Level:").pack(pady=5)
        self.activity_level_var = tk.StringVar(self.setup_frame)
        self.activity_level_var.set("Select Activity Level")
        activity_levels = [
            "Little to no exercise",
            "Light exercise 1-3 days/week",
            "Moderate exercise 3-5 days/week",
            "Hard exercise 6-7 days/week",
            "Physically demanding job or challenging exercise routine"
        ]
        ttk.OptionMenu(self.setup_frame, self.activity_level_var, *activity_levels).pack(pady=5)

        ttk.Button(self.setup_frame, text="Submit", command=self.submit_user_details).pack(pady=20)

    def submit_user_details(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        height = int(self.height_entry.get())
        weight = int(self.weight_entry.get())
        activity_level = self.activity_level_var.get()

        self.manager = HealthManager(name, age, height, weight, activity_level)
        self.manager.save_user_data()

        self.setup_frame.destroy()
        self.create_main_dashboard()

    def create_main_dashboard(self):
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
        ttk.Button(self.nav_frame, text="User Information", command=self.show_user_info_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Calories Consumed", command=self.show_calories_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Calories Burned", command=self.show_calories_burned_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Water Tracker", command=self.show_water_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Medication Reminder", command=self.show_medication_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Analytics", command=self.show_analytics_section).pack(side=tk.LEFT, padx=5)

        self.create_user_info_section()
        self.create_calories_section()
        self.create_calories_burned_section()
        self.create_water_section()
        self.create_medication_section()
        self.create_analytics_section()

        self.show_user_info_section()  # Show user info section by default

        # Start medication reminder thread
        self.manager.start_medication_reminders()
        # Start water reminder thread
        self.manager.start_water_reminders()
        # Start break manager thread
        start_break_manager()

    def toggle_medication_notifications(self):
        self.manager.toggle_medication_notifications()

    def toggle_water_notifications(self):
        self.manager.toggle_water_notifications()

    def toggle_break_notifications(self):
        break_manager.toggle_break_notifications()

    def create_user_info_section(self):
        self.user_info_frame = ttk.Frame(self.root)
        self.user_info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        calories_to_burn = self.manager.calculate_calories_to_burn()

        user_info = f"Name: {self.manager.name}\n" \
                    f"Water to be taken: {self.manager.calculate_daily_water_intake():.2f} liters\n" \
                    f"Calories to be consumed: {self.manager.calculate_daily_calorie_intake():.2f} kcal\n" \
                    f"Calories consumed: {self.manager.calories_consumed} kcal\n" \
                    f"Calories burnt: {self.manager.calories_burned} kcal\n" \
                    f"Calories to be burnt: {calories_to_burn:.2f} kcal\n" \
                    f"Water consumed: {self.manager.water_consumed:.2f} liters"
        ttk.Label(self.user_info_frame, text="User Information", font=('Helvetica', 14, 'bold')).pack(pady=10)
        self.user_info_label = ttk.Label(self.user_info_frame, text=user_info, font=('Helvetica', 12))
        self.user_info_label.pack(pady=10)

    def create_calories_section(self):
        self.calories_frame = ttk.Frame(self.root)
        self.calories_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.calories_frame.forget()  # Hide initially

        ttk.Label(self.calories_frame, text="Enter calories consumed:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.calories_entry = ttk.Entry(self.calories_frame)
        self.calories_entry.pack(pady=5)
        ttk.Button(self.calories_frame, text="Add Manually", command=self.add_calories).pack(pady=5)

        ttk.Label(self.calories_frame, text="Select food item:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.food_var = tk.StringVar(self.calories_frame)
        self.food_var.set(self.manager.food_library['Food'].iloc[0])
        ttk.OptionMenu(self.calories_frame, self.food_var, *self.manager.food_library['Food']).pack(pady=5)
        ttk.Button(self.calories_frame, text="Add from Library", command=self.add_calories_from_library).pack(pady=5)

    def create_calories_burned_section(self):
        self.calories_burned_frame = ttk.Frame(self.root)
        self.calories_burned_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.calories_burned_frame.forget()  # Hide initially

        ttk.Label(self.calories_burned_frame, text="Enter calories burned manually:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.calories_burned_entry = ttk.Entry(self.calories_burned_frame)
        self.calories_burned_entry.pack(pady=5)
        ttk.Button(self.calories_burned_frame, text="Add Manually", command=self.add_calories_burned).pack(pady=5)

        ttk.Label(self.calories_burned_frame, text="Select exercise:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.exercise_var = tk.StringVar(self.calories_burned_frame)
        self.exercise_var.set(self.manager.exercise_library['Exercise'].iloc[0])
        ttk.OptionMenu(self.calories_burned_frame, self.exercise_var, *self.manager.exercise_library['Exercise']).pack(pady=5)

        ttk.Label(self.calories_burned_frame, text="Duration (minutes):", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.duration_entry = ttk.Entry(self.calories_burned_frame)
        self.duration_entry.pack(pady=5)
        ttk.Button(self.calories_burned_frame, text="Add from Library", command=self.add_calories_burned_from_library).pack(pady=5)

    def create_water_section(self):
        self.water_frame = ttk.Frame(self.root)
        self.water_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.water_frame.forget()  # Hide initially

        ttk.Label(self.water_frame, text="Track your water intake", font=('Helvetica', 12, 'bold')).pack(pady=10)
        ttk.Button(self.water_frame, text="250 ML per click", command=self.log_water).pack(pady=5)

    def create_medication_section(self):
        self.medication_frame = ttk.Frame(self.root)
        self.medication_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.medication_frame.forget()  # Hide initially

        ttk.Label(self.medication_frame, text="Add Medication", font=('Helvetica', 12, 'bold')).pack(pady=10)
        ttk.Label(self.medication_frame, text="Medication Name:").pack(pady=5)
        self.med_name_entry = ttk.Entry(self.medication_frame)
        self.med_name_entry.pack(pady=5)

        ttk.Label(self.medication_frame, text="Time (HH:MM AM/PM):").pack(pady=5)
        self.med_time_entry = ttk.Entry(self.medication_frame)
        self.med_time_entry.pack(pady=5)

        ttk.Button(self.medication_frame, text="Add", command=self.add_medication).pack(pady=10)

        ttk.Label(self.medication_frame, text="Medication Schedule", font=('Helvetica', 12, 'bold')).pack(pady=10)
        self.medication_listbox = tk.Listbox(self.medication_frame, font=('Helvetica', 12))
        self.medication_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        self.update_medication_list()

    def create_analytics_section(self):
        self.analytics_frame = ttk.Frame(self.root)
        self.analytics_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.analytics_frame.forget()  # Hide initially

        ttk.Label(self.analytics_frame, text="Analytics Dashboard", font=('Helvetica', 14, 'bold')).pack(pady=10)

        self.figure, self.ax = plt.subplots(2, 2, figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.analytics_frame)
        self.canvas.get_tk_widget().pack()

        self.update_analytics_dashboard()

    def show_analytics_section(self):
        self.update_analytics_dashboard()
        self.analytics_frame.pack(fill=tk.BOTH, expand=True)
        self.user_info_frame.forget()
        self.calories_frame.forget()
        self.calories_burned_frame.forget()
        self.water_frame.forget()
        self.medication_frame.forget()

    def update_analytics_dashboard(self):
        daily_data = self.manager.get_daily_data()

        self.ax[0, 0].clear()
        self.ax[0, 0].bar(['Consumed', 'Required'],
                          [daily_data['Calories Consumed'].sum(), daily_data['Calories Required'].sum()],
                          color=['blue', 'green'])
        self.ax[0, 0].set_title('Calories')

        calories_burned = daily_data['Calories Burnt'].sum()
        calories_to_burn = self.manager.calculate_calories_to_burn()
        self.ax[0, 1].clear()
        self.ax[0, 1].bar(['Burned', 'To Burn'], [calories_burned, calories_to_burn], color=['orange', 'red'])
        self.ax[0, 1].set_title('Calories Burned vs To Burn')

        self.ax[1, 0].clear()
        self.ax[1, 0].bar(['Consumed', 'Required'],
                          [daily_data['Water Consumed'].sum(), daily_data['Weight'].iloc[0] * 0.033],
                          color=['blue', 'green'])
        self.ax[1, 0].set_title('Water')

        bmi, status = self.manager.calculate_bmi()
        self.ax[1, 1].clear()
        self.ax[1, 1].bar(['BMI'], [bmi], color=['purple'])
        self.ax[1, 1].text(0, bmi + 1, f"{status}", ha='center')

        # Adding BMI categories
        self.ax[1, 1].set_ylim(0, 40)  # Set y-axis limit for better visualization
        self.ax[1, 1].axhspan(0, 18.5, facecolor='blue', alpha=0.5, label='Underweight')
        self.ax[1, 1].axhspan(18.5, 24.9, facecolor='green', alpha=0.5, label='Normal')
        self.ax[1, 1].axhspan(25, 29.9, facecolor='orange', alpha=0.5, label='Overweight')
        self.ax[1, 1].axhspan(30, 40, facecolor='red', alpha=0.5, label='Obese')
        self.ax[1, 1].legend(loc='upper right')

        self.ax[1, 1].set_title('BMI Categories')

        self.figure.tight_layout()
        self.canvas.draw()

    def show_user_info_section(self):
        self.update_user_info_label()
        self.user_info_frame.pack(fill=tk.BOTH, expand=True)
        self.calories_frame.forget()
        self.calories_burned_frame.forget()
        self.water_frame.forget()
        self.medication_frame.forget()
        self.analytics_frame.forget()

    def show_calories_section(self):
        self.calories_frame.pack(fill=tk.BOTH, expand=True)
        self.user_info_frame.forget()
        self.calories_burned_frame.forget()
        self.water_frame.forget()
        self.medication_frame.forget()
        self.analytics_frame.forget()

    def show_calories_burned_section(self):
        self.calories_burned_frame.pack(fill=tk.BOTH, expand=True)
        self.user_info_frame.forget()
        self.calories_frame.forget()
        self.water_frame.forget()
        self.medication_frame.forget()
        self.analytics_frame.forget()

    def show_water_section(self):
        self.water_frame.pack(fill=tk.BOTH, expand=True)
        self.user_info_frame.forget()
        self.calories_frame.forget()
        self.calories_burned_frame.forget()
        self.medication_frame.forget()
        self.analytics_frame.forget()

    def show_medication_section(self):
        self.medication_frame.pack(fill=tk.BOTH, expand=True)
        self.user_info_frame.forget()
        self.calories_frame.forget()
        self.calories_burned_frame.forget()
        self.water_frame.forget()
        self.analytics_frame.forget()

    def update_user_info_label(self):
        calories_to_burn = self.manager.calculate_calories_to_burn()
        user_info = f"Name: {self.manager.name}\n" \
                    f"Water to be taken: {self.manager.calculate_daily_water_intake():.2f} liters\n" \
                    f"Calories to be consumed: {self.manager.calculate_daily_calorie_intake():.2f} kcal\n" \
                    f"Calories consumed: {self.manager.calories_consumed} kcal\n" \
                    f"Calories burnt: {self.manager.calories_burned} kcal\n" \
                    f"Calories to be burnt: {calories_to_burn:.2f} kcal\n" \
                    f"Water consumed: {self.manager.water_consumed:.2f} liters"
        self.user_info_label.config(text=user_info)

    def add_calories(self):
        calories = int(self.calories_entry.get())
        self.manager.add_manual_calories(calories)
        self.manager.save_user_data()
        self.update_user_info_label()

    def add_calories_from_library(self):
        food = self.food_var.get()
        self.manager.select_food_from_library(food)
        self.manager.save_user_data()
        self.update_user_info_label()

    def add_calories_burned(self):
        calories = int(self.calories_burned_entry.get())
        self.manager.add_manual_burned_calories(calories)
        self.manager.save_user_data()
        self.update_user_info_label()

    def add_calories_burned_from_library(self):
        exercise = self.exercise_var.get()
        duration = int(self.duration_entry.get())
        self.manager.select_exercise_from_library(exercise, duration)
        self.manager.save_user_data()
        self.update_user_info_label()

    def log_water(self):
        self.manager.water_consumed += 0.25  # Assuming each log is 250ml
        self.manager.save_user_data()
        self.update_user_info_label()

    def add_medication(self):
        med_name = self.med_name_entry.get()
        med_time = self.med_time_entry.get()
        self.manager.add_medication(med_name, med_time)
        self.update_medication_list()

    def update_medication_list(self):
        self.medication_listbox.delete(0, tk.END)
        for med in self.manager.medication_schedule:
            time_12hr = datetime.strptime(med['Time'], "%H:%M").strftime("%I:%M %p")
            self.medication_listbox.insert(tk.END, f"{med['Medication']} at {time_12hr}")

    def start_medication_reminders(self):
        def reminder_loop():
            while True:
                now = datetime.now().strftime("%H:%M")
                for med in self.manager.medication_schedule:
                    if med['Time'] == now:
                        messagebox.showinfo("Medication Reminder", f"Time to take {med['Medication']}")
                time.sleep(60)  # Check every minute

        reminder_thread = Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()


def start_break_manager():
    global break_manager
    break_manager = BreakManager()
    break_thread = Thread(target=break_manager.track_activity, daemon=True)
    break_thread.start()

if __name__ == "__main__":
    root = ThemedTk(theme="clam")
    app = HealthApp(root)
    start_break_manager()
    root.mainloop()
