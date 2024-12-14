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

def test_check_if_marked(setup_attendance_log):
    data = {
        "Name": ["John Doe", "Jane Smith"],
        "Date": [str(datetime.now().date()), str(datetime.now().date())],
        "Time": ["10:00:00 AM", "10:05:00 AM"],
        "Day": ["Monday", "Monday"]
    }
    df = pd.DataFrame(data)

    logger = AttendenceLogger()
    
    # Test that "John Doe" is marked as present for today
    assert logger.check_if_marked("John Doe", df) == True
    
    # Test that a name not in the DataFrame is not marked as present
    assert logger.check_if_marked("Non Registered Name", df) == False

def test_log_attendance(setup_attendance_log):
    logger = AttendenceLogger()
    name = "John Doe"
    
    # Log attendance for the first time
    logger.log_attendance(name)
    
    # Check if the attendance file is created
    assert os.path.exists(setup_attendance_log) == True
    
    # Check if name is logged.
    df = pd.read_csv(setup_attendance_log)
    assert name in df["Name"].values
    assert len(df) == 1  # Ensure only one attendance entry
    
    # Checking if duplicate names get logged for the same day.
    logger.log_attendance(name)
    
    df = pd.read_csv(setup_attendance_log)
    assert len(df) == 1  # Attendance should not be logged twice for the same person

def test_get_attendance_log(setup_attendance_log):
    logger = AttendenceLogger()
    name = "John Doe"

    # Logs the attendance.
    logger.log_attendance(name)

    # Get the attendance log
    df = logger.get_attendance_log()
    
    # Check if the attendance log is returned as a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Ensure the file has at least one record (from the earlier log) and checks if all columns exist.
    assert len(df) > 0
    assert "Name" in df.columns
    assert "Date" in df.columns
    assert "Time" in df.columns
    assert "Day" in df.columns

def test_check_if_registered(setup_dataset):
    logger = AttendenceLogger()
    
    # Test with a name that is "registered" (the file was created during setup)
    name = "John Doe"
    
    # Check if the user is "registered"
    assert logger.check_if_registered(name) == True