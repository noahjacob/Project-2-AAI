# Description: Main app file that will run the GUI using streamlit.
from AttendenceLogger import AttendenceLogger
from FaceRecognition import FaceRecognition
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters

if __name__ == "__main__":
    st.title("Facial Recognition Attendance System")

    # Initialize FaceRecognition and AttendenceLogger classes
    face_recognition_model = FaceRecognition()
    attendance_logger = AttendenceLogger()
    
    with st.sidebar:
        selected = option_menu("Main Menu", ["Log Attendance", 'View Attendance Log', 'Train Model'], 
                               icons=['box-arrow-right', 'table'], menu_icon="list", default_index=0)

    if selected == "Log Attendance":
        st.title("Log In")
        mark = st.button("Mark Attendance")

        if mark:
            try:
                # Run the face recognition pipeline
                name = face_recognition_model.pipeline()
                
                # Log the attendance of the recognized face
                attendance_logger.log_attendance(name)

            except Exception as e:
                st.error(f"Error: {e}. Please make sure the model is trained or faces are registered.")
            
    elif selected == "View Attendance Log":
        st.title("Attendance Log")
        df = attendance_logger.get_attendance_log()

        if isinstance(df, pd.DataFrame):
            df.reset_index(drop=True, inplace=True)
            df.index = df.index + 1
            dynamic_filters = DynamicFilters(df, filters=["Name", "Date", "Day"])
            with st.sidebar:
                dynamic_filters.display_filters()
            dynamic_filters.display_df(use_container_width=True)
        else:
            st.write("There are no logs currently. Please start logging in.")
            
    else:  # Registration of new faces
        st.title("Registration")
        name = st.text_input("Please enter your full name", "")

        if name:
            if not face_recognition_model.check_if_registered(name):
                face_recognition_model.generate_dataset(name)
                face_recognition_model.update_model_and_train()
                st.write(f"Hi {name}! Your face has been successfully registered.")
            else:
                st.write(f"Hi {name}. Your face has already been registered.")