# Description: Class file for the attendence logging part of the app.
import os 
from datetime import datetime

class AttendenceLogger:

    def __init__(self):
        self.__attendance_log_file = "attendance_logs/attendance.csv"
        os.makedirs("attendance_logs", exist_ok=True)
    
    def get_attendance_log_file(self):
        return self.__attendance_log_file
    
    def get_current_timestamp(self):
        """Generate current timestamp."""
        current_timestamp = datetime.now()
        date = current_timestamp.date()
        time = current_timestamp.strftime('%I:%M:%S %p')
        day_name = current_timestamp.strftime("%A")
        return {"Date": date, "Time": time, "Day": day_name}
