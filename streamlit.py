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
fl_terrace = st.radio('Surface terrace (sqm):', [0, 1])

#Button to trigger prediction
if st.button('Predict Price'):
    # Prepare input data as JSON
    input_data = {
        'equipped_kitchen':equipped_kitchen,
        'nbr_frontages': nbr_frontages,
        'fl_terrace': fl_terrace,
        # Add more features as needed
    }

    # Make POST request to FastAPI endpoint
    try:
        response = requests.post(FASTAPI_URL, json=input_data)
        if response.status_code == 200:
            predicted_price = response.json()[predicted_price]
            st.success(f'Predicted Price: £{predicted_price:.2f}')
        else:
            st.error('Failed to get prediction. Please try again.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')


