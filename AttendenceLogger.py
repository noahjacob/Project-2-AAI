# Description: Class file for the attendence logging part of the app.
import os 
from datetime import datetime
import pandas as pd
import streamlit as st
import glob

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
    
    def check_if_marked(self, name, df):
        """Check if the student is already marked for the day."""
        today_date = datetime.now().date()
        
        if len(df[(df["Name"] == name) & (df["Date"] == str(today_date))]):
            return True
        return False
    
    def log_attendance(self, name):
        """Log attendance to a CSV file."""
        timestamp = self.get_current_timestamp()
        log = {"Name": name}
        log.update(timestamp)

        if not os.path.exists(self.get_attendance_log_file()):
            df = pd.DataFrame()
            df = df._append(log, ignore_index=True)
            df.to_csv(self.get_attendance_log_file(), index=False)
            st.write(f"Attendance marked for {name}.")
        else:
            df = pd.read_csv(self.get_attendance_log_file())
            if not self.check_if_marked(name, df):
                df = df._append(log, ignore_index=True)
                df.to_csv(self.get_attendance_log_file(), index=False)
                st.write(f"Attendance marked for {name}.")
            else:
                st.write(f"{name} has already been marked present today.")

    def get_attendance_log(self):
        """Return the attendance log DataFrame."""
        if os.path.exists(self.get_attendance_log_file()):
            return pd.read_csv(self.get_attendance_log_file())
        return None
    
    def check_if_registered(self, name):
        """Check if the person is registered in the dataset."""
        # Check if the person's face is already registered in the dataset
        pattern = os.path.join("dataset", f"{name}_*.jpg")
        matches = glob.glob(pattern)
        return len(matches) > 0
