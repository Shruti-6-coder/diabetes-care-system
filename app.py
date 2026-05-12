import streamlit as st
import pandas as pd
from datetime import datetime
import os

file_path = "data.csv"

st.title("Smart Diabetes Care System")

st.sidebar.title("Navigation")

option = st.sidebar.selectbox(
    "Choose an option",
    ["Home", "Add Sugar Level", "View Data", "Diet Suggestion", "Reminder", "Prediction"]
)

# Create file if not exists
if not os.path.exists("data.csv"):
    df = pd.DataFrame(columns=["Time", "Sugar"])
    df.to_csv("data.csv", index=False)

# HOME
if option == "Home":
    st.write("Welcome to your Diabetes Dashboard")

# ADD SUGAR LEVEL
elif option == "Add Sugar Level":
    st.subheader("Enter Blood Sugar Level")

    sugar = st.number_input("Enter value (mg/dL)", min_value=0)

    if st.button("Save Data"):
        new_data = pd.DataFrame({
            "Time": [datetime.now()],
            "Sugar": [sugar]
        })

        new_data.to_csv(file_path, mode='a', header=False, index=False)

        st.success("✅ Data Saved Successfully!")

        # 🚨 SMART ALERT SYSTEM
        if sugar > 180:
            st.error("⚠ High Sugar Level! Consider insulin or consult a doctor.")
        elif sugar < 70:
            st.warning("⚠ Low Sugar Level! Take glucose immediately.")
        else:
            st.success("✅ Sugar level is normal.")
# VIEW DATA
elif option == "View Data":
    st.subheader("Your Sugar Records")

    df = pd.read_csv(file_path)
    
    st.subheader("Statistics")

    st.write("Average Sugar:", df["Sugar"].mean())
    st.write("Max Sugar:", df["Sugar"].max())
    st.write("Min Sugar:", df["Sugar"].min())

    # Show table
    st.write(df)

    # Convert Time column to datetime
    df["Time"] = pd.to_datetime(df["Time"])

    # Set Time as index
    df.set_index("Time", inplace=True)

    # Show line chart
    st.subheader("Sugar Level Trend 📈")
    st.line_chart(df["Sugar"])

# DIET SUGGESTION
elif option == "Diet Suggestion":
    st.subheader("Personalized Diet Suggestion 🥗")

    sugar = st.number_input("Enter your current sugar level (mg/dL)", min_value=0)

    if sugar > 0:
        if sugar < 70:
            st.error("⚠ Low Sugar (Hypoglycemia)")
            st.write("👉 Take quick sugar foods:")
            st.write("- Fruit juice")
            st.write("- Glucose tablets")
            st.write("- Banana")
            st.write("- Honey")

        elif 70 <= sugar <= 140:
            st.success("✅ Normal Sugar Level")
            st.write("👉 Maintain balanced diet:")
            st.write("- Roti / Brown rice")
            st.write("- Dal, vegetables")
            st.write("- Fruits in moderation")
            st.write("- Plenty of water")

        elif 140 < sugar <= 180:
            st.warning("⚠ Slightly High Sugar")
            st.write("👉 Control carbs:")
            st.write("- Avoid white rice")
            st.write("- Eat more vegetables")
            st.write("- Include protein (dal, paneer, eggs)")
            st.write("- Walk after meals")

        else:
            st.error("🚨 High Sugar Level")
            st.write("👉 Strict diet control needed:")
            st.write("- No sugar / sweets")
            st.write("- Avoid rice & fried food")
            st.write("- Eat leafy vegetables")
            st.write("- High protein diet")
            st.write("- Drink water & exercise")

        st.info("💡 Tip: Always consult a doctor for medical advice.")
        
# ADD REMINDER

elif option == "Reminder":
    st.subheader("Medicine & Insulin Reminder ⏰")

    reminder_time = st.time_input("Set Reminder Time")

    if st.button("Set Reminder"):
        st.session_state["reminder_time"] = reminder_time
        st.success(f"Reminder set for {reminder_time}")

    # Check reminder
    if "reminder_time" in st.session_state:
        current_time = datetime.now().time()

        # Convert to same format (ignore seconds)
        if current_time.hour == st.session_state["reminder_time"].hour and \
           current_time.minute == st.session_state["reminder_time"].minute:

            st.error("💊 Time to take your medicine / insulin!")

        else:
            st.info(f"Next reminder at {st.session_state['reminder_time']}")
                    
#PREDICTION

elif option == "Prediction":
    st.subheader("AI-Based Sugar Prediction 🤖")

    df = pd.read_csv(file_path)

    if len(df) < 2:
        st.warning("Not enough data to predict. Add more sugar records.")
    else:
        import numpy as np
        from sklearn.linear_model import LinearRegression

        # Prepare data
        df["Index"] = range(len(df))

        X = df[["Index"]]
        y = df["Sugar"]

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next value
        next_index = [[len(df)]]
        prediction = model.predict(next_index)

        st.success(f"📈 Predicted Next Sugar Level: {prediction[0]:.2f} mg/dL")