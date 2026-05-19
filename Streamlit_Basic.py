import streamlit as st
st.title("Hello")
st.header("This is header")
st.subheader("This is subheader")
st.text("This is our project")
st.markdown("### This is a markdown")

#Checkbox
if st.checkbox("Show/Hide"):
    st.text("Showing the widge")

#Radion Button
# Create a radion button to select gender
status = st.radio("Select Gender:", ["Male", "Female"])

#Display the selected option using success message
if status == 'Male':
    st.success("Male")
else:
    st.success("Female")

#Selection Box
# Create a radion button to select gender
Hobby = st.selectbox("Select your Hobby:", ["Dancing", "Reading", "Sports"])

#Display the selected hobby
st.write("Your hobby is: ", Hobby)

#Multi-Selectbox
# Create a multi select box for choosing hobbies
hobbies = st.multiselect("Select your Hobbies:", ['Dancing', 'Reading','Sports'])

#Display the number of selected hobbies
st.write("You Selected", len(hobbies), "hobbies")

#Button
st.button("Click")

if st.button("About"):
    st.text("Welcome to streamlit")

#Text Input
name = st.text_input("Enter your name:")

if st.button("Submit"):
    result = name.title()
    st.success(result)


#Slider
level = st.slider("Choose a level", min_value=1, max_value=5)

st.write(f"Selected Level: {level}")

