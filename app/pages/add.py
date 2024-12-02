import streamlit as st
from utils.database import *
from datetime import datetime
def add_note():
    st.title("New Note")

    # Initialize session state variables
    if "workouts" not in st.session_state:
        st.session_state["workouts"] = []
    if "show_form" not in st.session_state:
        st.session_state["show_form"] = False

    target = st.text_input("Target area")

    # Button to toggle the workout form
    if st.button('\+'):
        st.session_state["show_form"] = True

    # Show workout form only when toggled
    if st.session_state["show_form"]:
        with st.form("add_workout_form"):
            exercise = st.text_input("Exercise")
            weight = st.number_input("Weight", min_value=0.0, step=0.1)
            reps = st.number_input("Reps", min_value=1, step=1)
            sets = st.number_input("Sets", min_value=1, step=1)
            submitted = st.form_submit_button("Add Exercise")

            if submitted:
                st.session_state["workouts"].append({
                    "exercise": exercise,
                    "weight": weight,
                    "reps": reps,
                    "sets": sets,
                })
        
            
        if st.button("Save Routine"):
            if target and st.session_state["workouts"]:
                new_routine = {
                    "target": target,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "workouts": st.session_state["workouts"]
                }

                # Update database: Add routine to the user's document
                client = get_mongo_client()
                if client:
                    db = client['fitCore_user_data']

                    db.users.update_one(
                        {"username": st.session_state["username"]},
                        {"$push": {"routines": new_routine}},
                        upsert=True
                    )
                    st.success("Routine saved!")
                    # Clear session state after saving
                    st.session_state["workouts"] = []
                    st.session_state["target_input"] = ""
        else:
            st.error("Please specify a target area and add at least one workout.")
    # Display workouts in an expander
    with st.expander("Show added workouts"):
        if st.session_state["workouts"]:
            for idx, workout in enumerate(st.session_state["workouts"], start=1):
                st.write(f"**Workout {idx}:**")
                st.write(f"- Exercise: {workout['exercise']}")
                st.write(f"- Weight: {workout['weight']} kg")
                st.write(f"- Reps: {workout['reps']}")
                st.write(f"- Sets: {workout['sets']}")
                st.write("---")
        else:
            st.write("No workouts added yet.")



if __name__ == "__main__":
    if st.session_state["authenticated"] == True:
        add_note()
    else:
        st.text("Sign In or Create account to view notes")