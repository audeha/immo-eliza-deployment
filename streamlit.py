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
equipped_kitchen=st.selectbox("Pick kitchen type",['HYPER_EQUIPPED', 'INSTALLED', 'MISSING', 
                                                   'NOT_INSTALLED', 'SEMI_EQUIPPED', 'USA_HYPER_EQUIPPED', 
                                                   'USA_INSTALLED', 'USA_SEMI_EQUIPPED', 'USA_UNINSTALLED']
)
nbr_frontages = st.number_input('Number of Frontages:', min_value=0, max_value=10, value=1)
fl_terrace = st.selectbox('Terrace ?:',  [0, 1])
fl_garden = st.selectbox('Garden ?:',  [0, 1])
fl_swimming_pool = st.selectbox('Swimming pool ?:',  [0, 1])
property_type=st.selectbox("Pick property type",['Apartment','House'])
longitude = st.slider("Longitude", min_value=5.479947, max_value=6.385048, step=0.000001)
latitude = st.slider("Latitude", min_value=48.824985, max_value=50.351432, step=0.000001)

region=st.selectbox("Pick region",['Brussels-Capital', 'Flanders', 'Wallonia'])
province = st.selectbox('Province', ['Antwerp', 'Brussels', 'East Flanders', 
                                     'Flemish Brabant', 'Hainaut', 'Liège', 'Limburg', 'Luxembourg', 'MISSING', 
                                     'Namur', 'Walloon Brabant', 'West Flanders']
)
heating_type = st.selectbox('Type of heating:', ['CARBON', 'ELECTRIC', 'FUELOIL', 'GAS', 
                                                 'MISSING', 'PELLET', 'SOLAR', 'WOOD']
)
state_building = st.selectbox('State of building:', ['AS_NEW', 'GOOD', 'JUST_RENOVATED', 
                                                     'MISSING', 'TO_BE_DONE_UP', 'TO_RENOVATE', 
                                                     'TO_RESTORE']
)

epc = st.selectbox('EPC:', ['A', 'A+', 'A++', 'B', 
                            'C', 'D', 'E', 'F', 'G', 'MISSING']
)
subproperty_type = st.selectbox('Select type of subproperty:',['APARTMENT', 'APARTMENT_BLOCK', 'BUNGALOW', 'CASTLE', 
                                                               'CHALET', 'COUNTRY_COTTAGE', 'DUPLEX', 'EXCEPTIONAL_PROPERTY', 
                                                               'FARMHOUSE', 'FLAT_STUDIO', 'GROUND_FLOOR', 'HOUSE', 'KOT', 'LOFT', 
                                                               'MANSION', 'MANOR_HOUSE', 'MIXED_USE_BUILDING', 'OTHER_PROPERTY', 
                                                               'PENTHOUSE', 'SERVICE_FLAT', 'TOWN_HOUSE', 'TRIPLEX', 'VILLA']
)
nbr_bedrooms = st.number_input('Number of Bedrooms:', min_value=0, max_value=10, value=1)
surface_area = st.number_input('Surface Area (sqm):', min_value=0.0, step=10.0)
garden_sqm = st.number_input('Garden Area (sqm):', min_value=0.0, step=10.0)
total_area_sqm = st.number_input('Living Area (sqm):', min_value=0.0, step=10.0)
surface_land_sqm = st.number_input('Plot Area (sqm):', min_value=0.0, step=10.0)
terrace_sqm = st.number_input('Terrace Area (sqm):', min_value=0.0, step=2.0)


locality = st.selectbox('Locality:', ['Aalst', 'Antwerp', 'Arlon', 'Ath', 'Bastogne', 
                                      'Brugge', 'Brussels', 'Charleroi', 'Dendermonde', 
                                      'Diksmuide', 'Dinant', 'Eeklo', 'Gent', 'Halle-Vilvoorde', 
                                      'Hasselt', 'Huy', 'Ieper', 'Kortrijk', 'Leuven', 'Liège', 
                                      'Maaseik', 'Marche-en'])




#Button to trigger prediction
if st.button('Predict Price'):
    # Prepare input data as JSON
    input_data = {
  "nbr_frontages": nbr_frontages,
  "equipped_kitchen": equipped_kitchen,
  "nbr_bedrooms": nbr_bedrooms,
  "latitude": latitude,
  "longitude": longitude,
  "total_area_sqm": total_area_sqm,
  "surface_land_sqm": surface_land_sqm,
  "terrace_sqm": terrace_sqm,
  "garden_sqm": garden_sqm,
  "province": province,
  "heating_type": heating_type,
  "state_building": state_building,
  "property_type": property_type,
  "epc": epc,
  "locality": locality,
  "subproperty_type": subproperty_type,
  "region": region,
  "fl_terrace": fl_terrace,
  "fl_garden": fl_garden,
  "fl_swimming_pool": fl_swimming_pool
}




    # Make POST request to FastAPI endpoint
    try:
        response = requests.post(FASTAPI_URL, json=input_data)
        if response.status_code == 200:
            predicted_price = response.json()[0]
            st.success(f'Predicted Price: €{predicted_price:.2f}')
        else:
            st.error('Failed to get prediction. Please try again.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
