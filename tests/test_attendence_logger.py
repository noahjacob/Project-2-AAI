import os
import pytest
import pandas as pd
from datetime import datetime
from AttendenceLogger import AttendenceLogger

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


@pytest.fixture
def setup_dataset():
    # Setup: Create necessary directories and a dummy dataset file
    os.makedirs("dataset", exist_ok=True)
    dummy_image_path = os.path.join("dataset", "John Doe_1.jpg")
    if os.path.exists(dummy_image_path):
        os.remove(dummy_image_path)
    
    # Create a dummy image file to simulate registration (content is dummy)
    with open(dummy_image_path, "w") as f:
        f.write("Dummy Image")

    yield dummy_image_path  # This is where the test will run

    # Teardown: Clean up the created dataset file after the test
    if os.path.exists(dummy_image_path):
        os.remove(dummy_image_path)
    if not os.listdir("dataset"):
        os.rmdir("dataset")