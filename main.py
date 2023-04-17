import sys
from PyQt5.QtWidgets import QApplication
from user import Ui_MainWindow
from ui_functions import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from count_time import Timeclass

from status_mqtt import *
from mqtt import *

class ui_windows(QMainWindow):
    def __init__(self):
        super(ui_windows, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #######SET WINDOWS ICOND AND TITLE########
        self.setWindowIcon(QIcon("images/logo.jpg"))
        self.setWindowTitle("Dostan")

        ##########INITIAL VARIABLES##########
        self.load = ""
        self.unload = ""
        self.save_load = []
        self.save_unload = []
        self.second_load = []
        self.second_unload = []
        self.final = []
        self.final_str = ""
        self.save_load_str = ""
        self.save_unload_str = ""
        self.second_load_str = ""
        self.second_unload_str = ""
        self.goal_list = []
        self.tour = False
        self.state = "false"

        ##########STYLESHEETS#################
        self.passive_style_header = """
        font: 63 24pt "Bahnschrift SemiBold";
        color: rgb(141, 141, 141);
        """ 

        self.passive_style = """
        font: 63 14pt "Bahnschrift SemiBold";
        color: rgb(141, 141, 141);
        """

        self.active_style_header = """
        font: 63 24pt "Bahnschrift SemiBold";
        color: #4286f4;
        """

        self.active_style = """
        font: 63 14pt "Bahnschrift SemiBold";
        color: #4286f4;
        """

        self.active_loading_style = """
        QPushButton{
            background-color:#4286f4;
            border: 0px;
            border-radius: 15px;
                font: 63 14pt "Bahnschrift SemiBold";
                color: rgb(209, 209, 209);
            }
            QPushButton:hover{
            background-color: rgb(208, 208, 208);
                color: rgb(66, 66, 66);
            }
        """
        self.passive_loading_style = """
        QPushButton{
            border: 2px solid #4286f4;
            border-radius: 15px;
                font: 63 14pt "Bahnschrift SemiBold";
                color: rgb(209, 209, 209);
            }
            QPushButton:hover{
            background-color: rgb(208, 208, 208);
                color: rgb(66, 66, 66);
            border:0px;
            }
        """

        ##########STATUS LABEL LIST AND INITIAL CONDITIONS############
        self.cnt = 0
        self.status_label_list = [self.ui.loading1, self.ui.unloading1, self.ui.loading2, self.ui.unloading2]
        for i in self.status_label_list:
            i.setStyleSheet(self.passive_style)

        self.status_header_list = [self.ui.step1_label, self.ui.step2_label]
        for i in self.status_header_list:
            i.setStyleSheet(self.passive_style_header)

        ##########START MQTT COMMUNICATION#####
        self.mqtt = MyThread()
        self.mqtt.value.connect(self.update_speed)
        self.mqtt.start()

        self.status_mqtt = MyThreadTerminal()
        # self.status_mqtt.start()
        self.status_mqtt.value.connect(self.update_status)

        self.count_time = Timeclass()
        self.count_time.value.connect(self.update_time)
        self.cnt = 0


        #########LOADING BUTTONS###############
        self.ui.load_u.clicked.connect(lambda: Ui_Functions.write_load(self, "U"))
        self.ui.load_d.clicked.connect(lambda: Ui_Functions.write_load(self, "D"))
        self.ui.load_l.clicked.connect(lambda: Ui_Functions.write_load(self, "L"))
        self.ui.load_r.clicked.connect(lambda: Ui_Functions.write_load(self, "R"))

        ########UNLOADING BUTTONS#############
        self.ui.unload_u.clicked.connect(lambda: Ui_Functions.write_unload(self, "U"))
        self.ui.unload_d.clicked.connect(lambda: Ui_Functions.write_unload(self, "D"))
        self.ui.unload_l.clicked.connect(lambda: Ui_Functions.write_unload(self, "L"))
        self.ui.unload_r.clicked.connect(lambda: Ui_Functions.write_unload(self, "R"))

        ########FIINSH BUTTONS##########
        self.ui.final_u.clicked.connect(lambda: Ui_Functions.write_final(self, "U"))
        self.ui.final_d.clicked.connect(lambda: Ui_Functions.write_final(self, "D"))
        self.ui.final_l.clicked.connect(lambda: Ui_Functions.write_final(self, "L"))
        self.ui.final_r.clicked.connect(lambda: Ui_Functions.write_final(self, "R"))

        ##########SELECT TOUR, SEND AND CLEAD BUTTONS
        self.ui.tur1_btn.clicked.connect(lambda: Ui_Functions.set_firttour(self))
        self.ui.tur2_btn.clicked.connect(lambda: Ui_Functions.set_secondtour(self))
        self.ui.clear_btn.clicked.connect(lambda: Ui_Functions.clear_tour(self))
        self.ui.start_btn.clicked.connect(lambda: Ui_Functions.send_goal(self))



        Ui_Functions.velocity_progress(self, 0.0)
        Ui_Functions.battery_percentage(self, 85)
    
    def update_speed(self, value):
        if float(value[1]) == 0.1:
            value[1] = 0.0
        speed_rotation = [round(float(value[1]), 3), round(float(value[2]), 3)]
        Ui_Functions.velocity_progress(self, speed_rotation[0])
    
    def update_status(self, value):
        if self.cnt < len(self.status_label_list):
            self.status_label_list[value].setStyleSheet(self.active_style)
            if self.cnt > 1:
                self.ui.step2_label.setStyleSheet(self.active_style_header)
            self.cnt += 1
    
    def update_time(self, value):
        self.cnt += value
        self.ui.time_label.setText(f"{int(self.cnt / 60)}dk {self.cnt % 60} s")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ui_windows()

    win.show()
    sys.exit(app.exec_())
