import sys
import pandas as pd
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton
from geopy.distance import geodesic

# Load CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'data', 'worldcities.csv')
city_data = pd.read_csv(csv_path)

def find_city_distance(city1, city2):
    def get_city_info(city_name):
        city_info = city_data.loc[city_data['city_ascii'].str.lower() == city_name.lower()]
        return city_info.to_dict(orient='records')[0] if not city_info.empty else None

    city1_info = get_city_info(city1)
    city2_info = get_city_info(city2)

    if city1_info and city2_info:
        city1_coordinates = (city1_info["lat"], city1_info["lng"])
        city2_coordinates = (city2_info["lat"], city2_info["lng"])
        distance = geodesic(city1_coordinates, city2_coordinates).kilometers
        return distance
    return None

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

city1_entry = QLineEdit()
city2_entry = QLineEdit()
result_label = QLabel('Distance: ')
calculate_button = QPushButton('Calculate Distance')

def on_click():
    city1 = city1_entry.text()
    city2 = city2_entry.text()
    distance = find_city_distance(city1, city2)
    if distance:
        result_label.setText(f"Distance: {distance:.2f} km")
    else:
        result_label.setText("One or both cities not found.")

calculate_button.clicked.connect(on_click)

layout.addWidget(QLabel('Enter first city:'))
layout.addWidget(city1_entry)
layout.addWidget(QLabel('Enter second city:'))
layout.addWidget(city2_entry)
layout.addWidget(calculate_button)
layout.addWidget(result_label)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
