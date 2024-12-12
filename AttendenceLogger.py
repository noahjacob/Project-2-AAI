# Description: Class file for the attendence logging part of the app.
import os 

class AttendenceLogger:

    def __init__(self):
        self.__attendance_log_file = "attendance_logs/attendance.csv"
        os.makedirs("attendance_logs", exist_ok=True)
    
    def get_attendance_log_file(self):
        return self.__attendance_log_file
