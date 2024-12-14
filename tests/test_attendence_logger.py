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

def test_get_current_timestamp(setup_attendance_log):
    logger = AttendenceLogger()
    timestamp = logger.get_current_timestamp()

    # Ensure the timestamp contains Date, Time, and Day
    assert "Date" in timestamp
    assert "Time" in timestamp
    assert "Day" in timestamp
    
    
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    correct_format = f"{year}-{month}-{day}"

    # Ensure the date is in the correct format
    assert isinstance(timestamp["Date"], str)
    assert timestamp["Date"] == correct_format

    assert isinstance(timestamp["Time"], str)
    assert isinstance(timestamp["Day"], str)