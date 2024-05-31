import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QFileDialog, QInputDialog
from PyQt5.QtGui import QFont
import json


class CalorieCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.food_items = {}

        self.setWindowTitle("Calorie Counter")
        self.setGeometry(100, 100, 400, 400)

        self.food_label = QLabel("Food Item:", self)
        self.food_label.move(20, 20)
        self.calorie_label = QLabel("Calories:", self)
        self.calorie_label.move(20, 50)
        self.total_calories_label = QLabel("Total Calories: 0", self)
        self.total_calories_label.move(20, 200)
        
        self.total_calories_label.setFont(QFont("Arial", 12))
        self.total_calories_label.setFixedWidth(200)

        self.food_entry = QLineEdit(self)
        self.food_entry.setGeometry(120, 20, 200, 25)
        self.calorie_entry = QLineEdit(self)
        self.calorie_entry.setGeometry(120, 50, 200, 25)

        self.add_button = QPushButton("Add", self)
        self.add_button.setGeometry(20, 80, 100, 30)
        self.add_button.clicked.connect(self.add_food_item)

        self.food_listbox = QListWidget(self)
        self.food_listbox.setGeometry(20, 120, 300, 70)
        self.food_listbox.itemDoubleClicked.connect(self.edit_food_item)

        self.remove_button = QPushButton("Remove Selected", self)
        self.remove_button.setGeometry(20, 250, 150, 30)
        self.remove_button.clicked.connect(self.remove_selected_item)
        self.save_button = QPushButton("Save", self)
        self.save_button.setGeometry(180, 250, 100, 30)
        self.save_button.clicked.connect(self.save_data)
        self.load_button = QPushButton("Load", self)
        self.load_button.setGeometry(290, 250, 100, 30)
        self.load_button.clicked.connect(self.load_data)

        self.show()

    def add_food_item(self):
        food = self.food_entry.text().strip()
        calories = self.calorie_entry.text().strip()

        if not food or not calories:
            QMessageBox.warning(self, "Input Error", "Please enter both food item and calorie value.")
            return

        try:
            calories = int(calories)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Calories must be a number.")
            return

        self.food_items[food] = calories

        self.update_food_list()
        self.update_total_calories()

        self.food_entry.clear()
        self.calorie_entry.clear()

    def update_food_list(self):
        self.food_listbox.clear()
        for food, calories in self.food_items.items():
            self.food_listbox.addItem(f"{food}: {calories} calories")

    def update_total_calories(self):
        total_calories = sum(self.food_items.values())
        self.total_calories_label.setText(f"Total Calories: {total_calories}")

    def remove_selected_item(self):
        selected = self.food_listbox.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Selection Error", "No item selected to remove.")
            return
        food = self.food_listbox.item(selected).text().split(':')[0].strip()
        del self.food_items[food]
        self.update_food_list()
        self.update_total_calories()

    def edit_food_item(self, item):
        food, ok_pressed = QInputDialog.getText(self, "Edit Food Item", "Food Item:", text=item.text().split(':')[0].strip())
        if ok_pressed and food:
            calories, ok_pressed = QInputDialog.getInt(self, "Edit Calories", "Calories:", value=int(item.text().split(':')[1].strip().split()[0]))
            if ok_pressed:
                del self.food_items[item.text().split(':')[0].strip()]
                self.food_items[food] = calories
                self.update_food_list()
                self.update_total_calories()

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON files (*.json)")
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.food_items, file)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JSON files (*.json)")
        if file_path:
            with open(file_path, 'r') as file:
                self.food_items = json.load(file)
            self.update_food_list()
            self.update_total_calories()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalorieCounterApp()
    sys.exit(app.exec_())
