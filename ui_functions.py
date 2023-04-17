from main import *
from mqtt import *

class Ui_Functions(ui_windows):
    def velocity_progress(self, value):
        styleSheet = """
        QFrame#progress_frame{
            background-color: qconicalgradient(cx:0.5, cy:0.5, angle:270, stop:{STOP_1} rgba(255, 255, 255, 0), stop:{STOP_2} rgba(66, 134, 244, 255));
        border-radius: 125px;
        }

        """

        progress = (5-value*10) / 5

        stop_1 = str(progress - 0.01)
        stop_2 = str(progress)

        newStyleSheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}",stop_2)

        self.ui.progress_frame.setStyleSheet(newStyleSheet)
        self.ui.speed_label.setText(str(value))
    
    def battery_percentage(self, pct):
        x = 18 + pct
        w = 155 - pct

        self.ui.battery_pct.setGeometry(x, 31, w, 76)
    
    def write_load(self, x):
        if not self.tour:
            self.save_load.append(x)
            self.save_load_str = ",".join(self.save_load)
            self.ui.loading_lineedit.setText(self.save_load_str)
        
        else:
            self.second_load.append(x)
            self.second_load_str = ",".join(self.second_load)
            self.ui.loading_lineedit.setText(self.second_load_str)

    def write_unload(self, unload):
        if not self.tour:
            self.save_unload.append(unload)
            self.save_unload_str = ",".join(self.save_unload)
            self.ui.unloading_lineedit.setText(self.save_unload_str)
        
        else:
            self.second_unload.append(unload)
            self.second_unload_str = ",".join(self.second_unload)
            self.ui.unloading_lineedit.setText(self.second_unload_str)
    
    def write_final(self, final):
        self.final.append(final)
        self.final_str = ",".join(self.final)
        self.ui.final_lineedit.setText(self.final_str)

    def clear_tour(self):
        self.final.clear()
        self.ui.final_lineedit.clear()
        if not self.tour:
            if len(self.save_unload) > 0:
                self.save_unload.pop()
                self.save_unload_str = ",".join(self.save_unload)
                self.ui.unloading_lineedit.setText(self.save_unload_str)
            else:
                if len(self.save_load) > 0:
                    self.save_load.pop()
                    self.save_load_str = ",".join(self.save_load)
                    self.ui.loading_lineedit.setText(self.save_load_str)
        
        else:
            if len(self.second_unload) > 0:
                self.second_unload.pop()
                self.second_unload_str = ",".join(self.second_unload)
                self.ui.unloading_lineedit.setText(self.second_unload_str)
            else:
                if len(self.second_load) > 0:
                    self.second_load.pop()
                    self.second_load_str = ",".join(self.second_load)
                    self.ui.loading_lineedit.setText(self.second_load_str)
    
    def send_goal(self):
        self.count_time.start()
        self.ui.step1_label.setStyleSheet(self.active_style_header)
        if not self.ui.unloading_lineedit.text():
            self.final_str = ''
            self.state = "true"
        else:
            self.state = "false"
        connect_mqtt().publish(topic_2, f"{self.save_load_str};{self.save_unload_str};{self.second_load_str};{self.second_unload_str};{self.final_str};{self.state}")
        print(f"{self.save_load_str}; {self.save_unload_str}; {self.second_load_str}; {self.second_unload_str}; {self.final_str};{self.state}")
    
    def set_firttour(self):
        self.ui.loading_lineedit.setText(self.save_load_str)
        self.ui.unloading_lineedit.setText(self.save_unload_str)
        self.ui.tur1_btn.setStyleSheet(self.active_loading_style)
        self.ui.tur2_btn.setStyleSheet(self.passive_loading_style)
        self.tour = False
    
    def set_secondtour(self):
        self.ui.loading_lineedit.setText(self.second_load_str)
        self.ui.unloading_lineedit.setText(self.second_unload_str)
        self.ui.tur1_btn.setStyleSheet(self.passive_loading_style)
        self.ui.tur2_btn.setStyleSheet(self.active_loading_style)
        self.tour = True