# app/analytics.py
import matplotlib.pyplot as plt
import pandas as pd

class Analytics:
    def __init__(self, user_data_filepath):
        self.user_data = pd.read_excel(user_data_filepath)

    def plot_calorie_analysis(self):
        plt.figure()
        plt.plot(self.user_data['Calories Consumed'], label='Calories Consumed')
        plt.plot(self.user_data['Calories Burnt'], label='Calories Burnt')
        plt.legend()
        plt.show()

