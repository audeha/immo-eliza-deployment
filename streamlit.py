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
equipped_kitchen=st.selectbox("Pick kitchen type",['USA_UNINSTALLED','USA_SEMI_EQUIPPED',
                                               'USA_INSTALLED', 'NOT_INSTALLED', 'USA_HYPER_EQUIPPED',
                                               'SEMI_EQUIPPED', 'HYPER_EQUIPPED', 'INSTALLED', 'MISSING'])
nbr_frontages = st.number_input('Number of Frontages:', min_value=0, max_value=10, value=1)
fl_terrace = st.number_input('Terrace ?:',  [0, 1])
fl_garden = st.number_input('Garden ?:',  [0, 1])
fl_swimming_pool = st.number_input('Swimming pool ?:',  [0, 1])
property_type=st.selectbox("Pick property type",['House','appartement'])
longitude = st.slider("Longitude", min_value=5.479947, max_value=6.385048, step=0.000001)
latitude = st.slider("Latitude", min_value=48.824985, max_value=50.351432, step=0.000001)

region=st.selectbox("Pick region",["Flanders","Wallonia","Brussels-Capital"])
province = st.selectbox('Province', [
    "West Flanders",
    "Antwerp",
    "East Flanders",
    "Hainaut",
    "Brussels",
    "Liège",
    "Flemish Brabant",
    "Limburg",
    "Walloon Brabant",
    "Namur",
    "Luxembourg",
    "MISSING"
])
heating_type = st.selectbox('Type of heating:', [
    "GAS",
    "MISSING",
    "FUELOIL",
    "ELECTRIC",
    "PELLET",
    "WOOD",
    "SOLAR",
    "CARBON"
])
state_building = st.selectbox('State of building:', [
    "MISSING",
    "GOOD",
    "AS_NEW",
    "TO_RENOVATE",
    "TO_BE_DONE_UP",
    "JUST_RENOVATED",
    "TO_RESTORE"
])

epc = st.selectbox('EPC:', [
    "MISSING",
    "B",
    "C",
    "D",
    "A",
    "F",
    "E",
    "G",
    "A+",
    "A++"
])
subproperty_type = st.selectbox('Select type of subproperty:',[
    "HOUSE",
    "APARTMENT",
    "VILLA",
    "GROUND_FLOOR",
    "APARTMENT_BLOCK",
    "MIXED_USE_BUILDING",
    "PENTHOUSE",
    "DUPLEX",
    "FLAT_STUDIO",
    "EXCEPTIONAL_PROPERTY",
    "TOWN_HOUSE",
    "SERVICE_FLAT",
    "MANSION",
    "BUNGALOW",
    "KOT",
    "LOFT",
    "FARMHOUSE",
    "COUNTRY_COTTAGE",
    "MANOR_HOUSE",
    "TRIPLEX",
    "OTHER_PROPERTY",
    "CHALET",
    "CASTLE"
])
nbr_bedrooms = st.number_input('Number of Bedrooms:', min_value=0, max_value=10, value=1)
surface_area = st.number_input('Surface Area (sqm):', min_value=0.0, step=10.0, value=1)
garden_sqm = st.number_input('Garden Area (sqm):', min_value=0.0, step=10.0, value=1)
total_area_sqm = st.number_input('Living Area (sqm):', min_value=0.0, step=10.0, value=1)
surface_land_sqm = st.number_input('Plot Area (sqm):', min_value=0.0, step=10.0, value=1)
terrace_sqm = st.number_input('Terrace Area (sqm):', min_value=0.0, step=2.0, value=1)


locality = st.selectbox('Locality:', [
    "Brussels",
    "Antwerp",
    "Liège",
    "Brugge",
    "Halle-Vilvoorde",
    "Gent",
    "Turnhout",
    "Leuven",
    "Nivelles",
    "Oostend",
    "Aalst",
    "Charleroi",
    "Kortrijk",
    "Hasselt",
    "Namur",
    "Mechelen",
    "Sint-Niklaas",
    "Mons",
    "Veurne",
    "Dendermonde",
    "Verviers",
    "Tournai",
    "Oudenaarde",
    "Soignies",
    "Thuin",
    "Mouscron",
    "Dinant",
    "Tongeren",
    "Maaseik",
    "Ath",
    "Huy",
    "Marche-en-Famenne",
    "Waremme",
    "Neufchâteau",
    "Arlon",
    "Diksmuide",
    "Virton",
    "Bastogne",
    "Philippeville",
    "Roeselare",
    "Eeklo",
    "Tielt",
    "Ieper",
    "MISSING"
])




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
            predicted_price = response.json()[0]
            st.success(f'Predicted Price: €{predicted_price:.2f}')
        else:
            st.error('Failed to get prediction. Please try again.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
