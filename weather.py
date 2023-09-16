import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("search.ui", self)

        self.search.clicked.connect(self.main)
    
    # Getting Data
    def get_data(self):
        self.city = self.city_name.text()
        base_url = 'http://api.weatherstack.com/current?'
        api = 'your api key'
        url = f'{base_url}access_key={api}&query={self.city}'
        self.response = requests.get(url).json()
        self.cur = self.response['current']

        # Saving Image
        image_url = self.cur['weather_icons'][0]
        image_data = requests.get(image_url).content
        with open('img.jpg', 'wb') as file:
            file.write(image_data)

    def main(self):
        try:
            self.get_data()
            loadUi('data.ui', self)

            # Inserting datas
            self.temp.setText(f"{str(self.cur['temperature'])} degree")
            self.pressure.setText(str(self.cur['pressure']))
            self.desc.setText(self.cur['weather_descriptions'][0])
            self.w_speed.setText(str(self.cur['wind_speed']))
            self.w_dir.setText(self.cur['wind_dir'])
            self.place.setText(self.response['location']['name'])
            self.uv.setText(str(self.cur['uv_index']))
            self.obv_time.setText(self.cur['observation_time'])
            self.humidity.setText(str(self.cur['humidity']))
            self.l_time.setText(self.response['location']['localtime'])

            # Insert Image from 'img.jpg'
            pixmap = QPixmap('img.jpg')
            self.Image.setPixmap(pixmap)
            self.Image.setScaledContents(True)  # Scale image to fit label

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            QMessageBox.warning(self, 'Error', error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
