import streamlit as st
import requests

#Define the URL of the FastAPI endpoint
FASTAPI_URL = 'https://immo-eliza-deployment.onrender.com/predict'  # Update with your FastAPI endpoint URL

#Streamlit App Title
st.title('Price Prediction Web App')

#Image
#st.image('streamlit', caption='Streamlit Logo', use_column_width=True)

#Input features for price prediction
st.header('Enter Features for Prediction')
equipped_kitchen=st.radio("pick kitchen type",['USA_UNINSTALLED','USA_SEMI_EQUIPPED',
                                               'USA_INSTALLED', 'NOT_INSTALLED', 'USA_HYPER_EQUIPPED',
                                               'SEMI_EQUIPPED', 'HYPER_EQUIPPED', 'INSTALLED', 'MISSING'])
nbr_frontages = st.number_input('Number of Frontages:', min_value=0, max_value=10, value=1)
fl_terrace = st.number_input('Surface terrace (sqm):', min_value=0.0, step=100.0)

#Button to trigger prediction
if st.button('Predict Price'):
    # Prepare input data as JSON
    input_data = {
        'equipped_kitchen':equipped_kitchen,
        'nbr_frontages': nbr_frontages,
        'fl_terrace': fl_terrace,
        # Add more features as needed
    }
