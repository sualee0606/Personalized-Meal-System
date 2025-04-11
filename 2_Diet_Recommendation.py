import streamlit as st
import pandas as pd
import random
import io

st.title("Diet Recommendation")

keys = ["bmr", "calorie_needs", "protein_target", "calorie_target"]
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = None

if None in [st.session_state[k] for k in keys]:
    st.error("Please go back to BMR page and fill in your information.")
    st.stop()

st.write("BMR:", round(st.session_state["bmr"], 2), "kcal/day")
st.write("Calorie Needs:", round(st.session_state["calorie_needs"], 2), "kcal")
st.write("Protein Target:", round(st.session_state["protein_target"], 2), "g")
st.write("Calorie Target:", round(st.session_state["calorie_target"], 2), "kcal")

is_vegan = st.session_state.get("is_vegan", "No")
has_allergy = st.session_state.get("has_allergy", "No")
allergy_info = st.session_state.get("allergy_info", "")

if is_vegan == "Yes":
    food_df = pd.read_csv("FOOD-VEGAN.csv")
else:
    food_df = pd.read_csv("FOOD-DATA.csv")

if "raw" in food_df["food"].values:
    food_df = food_df[~food_df["food"].str.contains("raw", case=False)]

if has_allergy == "Yes" and allergy_info.strip() != "":
    allergy_list = [x.strip().lower() for x in allergy_info.split(",")]
    for allergen in allergy_list:
        food_df = food_df[~food_df["food"].str.lower().str.contains(allergen)]

high_protein_df = pd.read_csv("FOOD-HIGH-PROTEIN.csv")

meal_count = st.radio("How many meals today?", [1, 2, 3], index=2)

def create_meal_plan():
    plan = []
    total_cal = st.session_state["calorie_target"]
    each_meal_cal = total_cal / meal_count

    for i in range(meal_count):
        if is_vegan == "Yes":
            selected = food_df.sample(4)
        else:
            protein_part = high_protein_df.sample(1)
            rest_part = food_df.sample(3)
            selected = pd.concat([protein_part, rest_part])

        total_grams = 400
        cal_sum = selected["Caloric Value"].sum()

        foods = []
        meal_cal = 0
        meal_protein = 0

        for _, row in selected.iterrows():
            percent = row["Caloric Value"] / cal_sum if cal_sum > 0 else 0.25
            grams = total_grams * percent
            cal = row["Caloric Value"] * (grams / 100)
            protein = row["Protein"] * (grams / 100)
            foods.append({
                "food": row["food"],
                "grams": round(grams),
                "calories": round(cal),
                "protein": round(protein, 1)
            })
            meal_cal += cal
            meal_protein += protein

        plan.append({
            "meal_number": f"Meal {i+1}",
            "foods": foods,
            "total_calories": round(meal_cal),
            "total_protein": round(meal_protein, 1)
        })

    return plan

if "meal_plan" not in st.session_state or st.session_state.get("meal_count") != meal_count:
    st.session_state["meal_plan"] = create_meal_plan()
    st.session_state["meal_count"] = meal_count

today_plan = st.session_state["meal_plan"]

st.subheader("Today's Meal Plan")
total_day_cal = 0
total_day_protein = 0

for meal in today_plan:
    st.write(meal["meal_number"])
    df = pd.DataFrame(meal["foods"])
    st.table(df)
    st.write("Total Calories:", meal["total_calories"])
    st.write("Total Protein:", meal["total_protein"])
    total_day_cal += meal["total_calories"]
    total_day_protein += meal["total_protein"]
    st.write("---")

st.write("Total Calories Today:", total_day_cal)
st.write("Total Protein Today:", total_day_protein)

def save_to_csv(plan):
    output = io.StringIO()
    for meal in plan:
        output.write(meal["meal_number"] + "\n")
        output.write("food,grams,calories,protein\n")
        for food in meal["foods"]:
            output.write(f"{food['food']},{food['grams']},{food['calories']},{food['protein']}\n")
        output.write("\n")
    return output.getvalue()

csv_data = save_to_csv(today_plan)

st.download_button("Download CSV", csv_data.encode("utf-8"), file_name="meal_plan.csv", mime="text/csv")

if st.button("Generate New Meal Plan"):
    st.session_state["meal_plan"] = create_meal_plan()
    st.success("New plan created.")
