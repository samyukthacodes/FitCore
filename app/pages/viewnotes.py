import streamlit as st

def show_notes():
    """
    Retrieve and display all routines for a given username.

    Args:
        username (str): The username to look up in the database.
        db (pymongo.database.Database): The MongoDB database object.
    """
    st.title("Your Routines")
    username = st.session_state["username"]
    db = st.session_state["db"]
    # Retrieve user data from the database
    user_data = db.users.find_one({"username": username})

    if user_data and "routines" in user_data:
        routines = user_data["routines"]
        
        if routines:
            for idx, routine in enumerate(routines, start=1):
                with st.expander(f"Routine {idx}: {routine['target']} ({routine['date']})"):
                    st.write(f"**Target Area:** {routine['target']}")
                    st.write(f"**Date:** {routine['date']}")
                    st.write("**Workouts:**")
                    for workout_idx, workout in enumerate(routine["workouts"], start=1):
                        st.write(f"  **Workout {workout_idx}:**")
                        st.write(f"    - Exercise: {workout['exercise']}")
                        st.write(f"    - Weight: {workout['weight']} kg")
                        st.write(f"    - Reps: {workout['reps']}")
                        st.write(f"    - Sets: {workout['sets']}")
        else:
            st.info("No routines found. Add a new routine to get started!")
    else:
        st.error("No user data found. Please ensure you are logged in.")



if __name__ == "__main__":
    if st.session_state["authenticated"] == True:
        show_notes()
    else:
        st.text("Sign In or Create account to view notes")