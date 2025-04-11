import streamlit as st
from datetime import date

st.title(" BMR Calculator")

def reset_session_state():
    st.session_state["birth_date"] = date(2000, 1, 1)
    st.session_state["gender"] = "Male"
    st.session_state["weight"] = 30.0
    st.session_state["height"] = 100.0
    st.session_state["fitness_goal"] = "Maintain Weight"
    st.session_state["activity_level"] = "Little or no exercise"
    st.session_state["is_vegan"] = "No"
    st.session_state["has_allergy"] = "No"
    st.session_state["allergy_info"] = ""
    st.session_state["bmr"] = None
    st.session_state["calorie_needs"] = None
    st.session_state["calorie_target"] = None
    st.session_state["protein_target"] = None

if "birth_date" not in st.session_state:
    reset_session_state()

st.header("Enter Your Information")

birth_date = st.date_input(
    "Enter your date of birth",
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    value=st.session_state["birth_date"]
)
st.session_state["birth_date"] = birth_date

current_year = date.today().year
birth_year = birth_date.year
age = current_year - birth_year

gender = st.radio(
    "Select your gender", 
    ["Male", "Female"], 
    horizontal=True,
    index=["Male", "Female"].index(st.session_state["gender"])
)
st.session_state["gender"] = gender

weight = st.number_input(
    "Enter your weight (kg)",
    min_value=30.0,
    max_value=200.0,
    step=0.1,
    value=st.session_state["weight"]
)
st.session_state["weight"] = weight

height = st.number_input(
    "Enter your height (cm)",
    min_value=100.0,
    max_value=250.0,
    step=0.1,
    value=st.session_state["height"]
)
st.session_state["height"] = height

fitness_goal = st.selectbox(
    "Select your fitness goal",
    ["Weight Loss", "Maintain Weight", "Build Muscle"],
    index=["Weight Loss", "Maintain Weight", "Build Muscle"].index(st.session_state["fitness_goal"])
)
st.session_state["fitness_goal"] = fitness_goal

activity_options = [
    "Little or no exercise",
    "Light exercise/sports 1-3 days a week",
    "Moderate exercise/sports 3-5 days a week",
    "Hard exercise/sports 6-7 days a week",
    "Very hard exercise /sports & physical job"
]
activity_level = st.selectbox(
    "Select your activity level",
    activity_options,
    index=activity_options.index(st.session_state["activity_level"])
)
st.session_state["activity_level"] = activity_level

is_vegan = st.radio(
    "Are you a vegan?", 
    ["Yes", "No"], 
    horizontal=True,
    index=["Yes", "No"].index(st.session_state["is_vegan"])
)
st.session_state["is_vegan"] = is_vegan

has_allergy = st.radio(
    "Do you have any allergies?", 
    ["Yes", "No"], 
    horizontal=True,
    index=["Yes", "No"].index(st.session_state["has_allergy"])
)
st.session_state["has_allergy"] = has_allergy

allergy_info = st.session_state["allergy_info"]
if has_allergy == "Yes":
    allergy_info = st.text_area(
        "Please specify your allergies (e.g., nuts, dairy, gluten)", 
        st.session_state["allergy_info"]
    )
    st.session_state["allergy_info"] = allergy_info
else:
    st.session_state["allergy_info"] = ""

activity_multiplier = {
    "Little or no exercise": 1.2,
    "Light exercise/sports 1-3 days a week": 1.375,
    "Mmoderate exercise/sports 3-5 days a week": 1.55,
    "Hard exercise/sports 6-7 days a week": 1.725,
    "Very hard exercise/sports & physical job": 1.9
}

if st.button("Calculate BMR"):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    calorie_needs = bmr * activity_multiplier[activity_level]

    if fitness_goal == "Weight Loss":
        calorie_target = calorie_needs * 0.8
        protein_target = weight * 1.6
    elif fitness_goal == "Maintain Weight":
        calorie_target = calorie_needs
        protein_target = weight * 1.8
    else:  
        calorie_target = calorie_needs * 1.2
        protein_target = weight * 2.0

    st.subheader("Your Results")
    st.success(f"🧮 BMR: {bmr:.2f} kcal/day")
    st.info(f"🏋️‍♀️ Daily Calorie Needs: {calorie_needs:.2f} kcal")
    st.info(f"🎯 Daily Calorie Target: {calorie_target:.2f} kcal")
    st.info(f"🍗 Daily Protein Target: {protein_target:.2f} g")

    if is_vegan == "Yes":
        st.info("🌱 You follow a vegan diet.")
    if allergy_info:
        st.info(f"⚠️ Allergy: {allergy_info}")

    st.session_state["bmr"] = bmr
    st.session_state["calorie_needs"] = calorie_needs
    st.session_state["calorie_target"] = calorie_target
    st.session_state["protein_target"] = protein_target

if st.button("Clear Data"):
    reset_session_state()
    st.success("All input data has been cleared!")
