import streamlit as st
import requests

#Define the URL of the FastAPI endpoint
FASTAPI_URL = ' https://immo-eliza-deployment.onrender.com/predict'  # Update with your FastAPI endpoint URL

#Streamlit App Title
st.title('Price Prediction Web App')

#Image
#st.image('streamlit', caption='Streamlit Logo', use_column_width=True)

#Input features for price prediction
st.header('Enter Features for Prediction')
property_type=st.radio("pick property type",['House','appartement'])
region=st.radio("Pick region",["Flanders","Wallonia","Brussels-Capital"])
province = st.text_input('Province')
nbr_bedrooms = st.number_input('Number of Bedrooms:', min_value=0, max_value=10, value=1)
surface_area = st.number_input('Surface Area (sqm):', min_value=0.0, step=100.0)
locality = st.text_input('Locality:', 'Enter the locality name')

#Button to trigger prediction
if st.button('Predict Price'):
    # Prepare input data as JSON
    input_data = {
        'property_type':property_type,
        'region':region,
        'province':province,
        'num_bedrooms': nbr_bedrooms,
        'surface_area': surface_area,
        'locality': locality,
        # Add more features as needed
    }


    # Make POST request to FastAPI endpoint
    try:
        response = requests.post(FASTAPI_URL, json=input_data)
        if response.status_code == 200:
            predicted_price = response.json()['predicted_price']
            st.success(f'Predicted Price: £{predicted_price:.2f}')
        else:
            st.error('Failed to get prediction. Please try again.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
