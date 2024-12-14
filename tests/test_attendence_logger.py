import os
import pytest
import pandas as pd
from datetime import datetime

@pytest.fixture
def setup_attendance_log():
    # Setup: Create necessary directories and a fresh attendance log file
    os.makedirs("attendance_logs", exist_ok=True)
    attendance_file = "attendance_logs/attendance.csv"
    if os.path.exists(attendance_file):
        os.remove(attendance_file)
    
    # Create a fresh attendance log file
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Day"])
    df.to_csv(attendance_file, index=False)

    yield attendance_file  # This is where the test will run

    # Teardown: Clean up the created attendance log file after the test
    if os.path.exists(attendance_file):
        os.remove(attendance_file)
    if not os.listdir("attendance_logs"):
        os.rmdir("attendance_logs")