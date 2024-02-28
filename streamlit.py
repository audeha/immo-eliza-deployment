import streamlit as st
import requests
import folium 
from streamlit_folium import folium_static, st_folium
from folium.plugins import Draw
from folium import plugins

headers = {
    "authorization": st.secrets['url'],
    "content-type": "application/json"
}

#Define the URL of the FastAPI endpoint
FASTAPI_URL = 'url'

loc_coordinates = {
    "Brussels": (50.8503, 4.3517),
    "Antwerp": (51.2194, 4.4025),
    "Liège": (50.8503, 5.6889),
    "Brugge": (51.2094, 3.2247),
    "Halle-Vilvoorde": (50.8333, 4.3),
    "Gent": (51.0543, 3.7174),
    "Turnhout": (51.3223, 4.9483),
    "Leuven": (50.8792, 4.7009),
    "Nivelles": (50.5974, 4.3279),
    "Oostend": (51.2093, 2.9296),
    "Aalst": (50.9364, 4.0355),
    "Charleroi": (50.4101, 4.4447),
    "Kortrijk": (50.8284, 3.2653),
    "Hasselt": (50.9311, 5.3375),
    "Namur": (50.4669, 4.8675),
    "Mechelen": (51.0259, 4.4773),
    "Sint-Niklaas": (51.1585, 4.1437),
    "Mons": (50.4541, 3.9561),
    "Veurne": (51.0749, 2.6564),
    "Dendermonde": (51.0259, 4.1059),
    "Verviers": (50.5891, 5.8667),
    "Tournai": (50.6052, 3.3879),
    "Oudenaarde": (50.8466, 3.611),
    "Soignies": (50.5796, 4.0714),
    "Thuin": (50.3397, 4.2859),
    "Mouscron": (50.7399, 3.2069),
    "Dinant": (50.2606, 4.9125),
    "Tongeren": (50.7805, 5.4645),
    "Maaseik": (51.0984, 5.7886),
    "Ath": (50.6303, 3.7806),
    "Huy": (50.5201, 5.2394),
    "Marche-en-Famenne": (50.2232, 5.3485),
    "Waremme": (50.6986, 5.256),
    "Neufchâteau": (49.8412, 5.4429),
    "Arlon": (49.6837, 5.8149),
    "Diksmuide": (51.0339, 2.8614),
    "Virton": (49.5665, 5.5232),
    "Bastogne": (50.0039, 5.7215),
    "Philippeville": (50.1669, 4.5475),
    "Roeselare": (50.9489, 3.121),
    "Eeklo": (51.1871, 3.5492),
    "Tielt": (50.999, 3.3396),
    "Ieper": (50.8503, 2.8833),
    "MISSING": (50.8503, 4.3517)  
}

#Streamlit App Title
st.title('Price Prediction Web App')

#Image
#st.image('streamlit', caption='Streamlit Logo', use_column_width=True)

#Input features for price prediction
st.header('Please Enter House Specifications for Prediction')

nbr_bedrooms = st.number_input('Number of Bedrooms:', min_value=0, max_value=10, value=1)
nbr_frontages = st.number_input('Number of Frontages:', min_value=0, max_value=10, value=1)
total_area_sqm = st.number_input('Living Area (sqm):', min_value=0.0, step=10.0)
surface_land_sqm = st.number_input('Plot Area (sqm):', min_value=0.0, step=10.0)
fl_terrace = st.selectbox('Terrace ?:',  [0, 1])
terrace_sqm = st.number_input('Terrace Area (sqm):', min_value=0.0, step=2.0)
fl_garden = st.selectbox('Garden ?:',  [0, 1])
garden_sqm = st.number_input('Garden Area (sqm):', min_value=0.0, step=10.0)
property_type=st.selectbox("Pick property type",['House','appartement'])
subproperty_type = st.selectbox('Select type of subproperty:',['HOUSE', 'APARTMENT', 'APARTMENT_BLOCK', 'BUNGALOW', 'CASTLE', 'CHALET', 'COUNTRY_COTTAGE', 'DUPLEX', 'EXCEPTIONAL_PROPERTY', 'FARMHOUSE', 'FLAT_STUDIO', 'GROUND_FLOOR', 'KOT', 'LOFT', 'MANOR_HOUSE', 'MANSION', 'MIXED_USE_BUILDING', 'OTHER_PROPERTY', 'PENTHOUSE', 'SERVICE_FLAT', 'TOWN_HOUSE', 'TRIPLEX', 'VILLA' ])


state_building = st.selectbox('State of building:', ["AS_NEW","JUST_RENOVATED","GOOD","TO_BE_DONE_UP","TO_RENOVATE","TO_RESTORE","MISSING"])


epc = st.selectbox('EPC:', ["A++","A+","A","B","C","D","E","F","G","MISSING",])

heating_type = st.selectbox('Type of heating:', ["GAS","ELECTRIC","PELLET","FUELOIL","WOOD","SOLAR","CARBON","MISSING"])

equipped_kitchen=st.selectbox("Pick kitchen type",['HYPER_EQUIPPED', 'INSTALLED', 'MISSING', 'NOT_INSTALLED', 'SEMI_EQUIPPED', 'USA_HYPER_EQUIPPED', 'USA_INSTALLED', 'USA_SEMI_EQUIPPED', 'USA_UNINSTALLED' ])

fl_swimming_pool = st.selectbox('Swimming pool ?:',  [0, 1])
# List of regions and their corresponding provinces
region_province_mapping = {
    "Flanders": ["West Flanders", "East Flanders", "Antwerp", "Limburg", "Flemish Brabant","MISSING"],
    "Wallonia": ["Hainaut", "Liège", "Walloon Brabant", "Namur", "Luxembourg","MISSING"],
    "Brussels-Capital": ["Brussels","MISSING"]
}

# List of localities for each province
province_locality_mapping = {
    "Antwerp": ["Antwerp", "Turnhout", "Mechelen"],
    "East Flanders": ["Gent", "Aalst", "Sint-Niklaas", "Dendermonde", "Oudenaarde", "Eeklo"],
    "Brussels": ["Brussels"],
    "Walloon Brabant": ["Nivelles"],
    "Flemish Brabant": ["Halle-Vilvoorde", "Leuven"],
    "Liège": ["Liège", "Verviers", "Huy", "Waremme"],
    "West Flanders": ["Brugge", "Oostend", "Kortrijk", "Veurne", "Diksmuide", "Roeselare", "Tielt", "Ieper"],
    "Hainaut": ["Charleroi", "Mons", "Tournai", "Soignies", "Thuin", "Mouscron", "Ath"],
    "Luxembourg": ["Marche-en-Famenne", "Neufchâteau", "Arlon", "Virton", "Bastogne"],
    "Limburg": ["Hasselt", "Tongeren", "Maaseik"],
    "Namur": ["Namur", "Dinant", "Philippeville"],
    "MISSING": ["MISSING"]
}


# User selects the region
region = st.selectbox("Pick region", list(region_province_mapping.keys()))

# Based on the selected region, dynamically update the options for the province
provinces_for_region = region_province_mapping.get(region, [])
province = st.selectbox('Province', provinces_for_region)

# Based on the selected province, dynamically update the options for the locality
localities_for_province = province_locality_mapping.get(province, [])
locality = st.selectbox('Locality:', localities_for_province)

for p,c in loc_coordinates.items():
    if p == locality:
        latitude = c[0]
        longitude = c[1]        
  
# Initial coordinates for Brussels
st.title("Property Location")

#belgium_coords = [50.8503, 4.3517]  # Latitude and Longitude for Brussels, Belgium
m = folium.Map(location=[latitude,longitude], zoom_start=12)
Draw(export=True).add_to(m)


# Call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

if st_data is not None and st_data.get("last_active_drawing") is not None:
    # Accessing coordinates from the last_active_drawing
    coordinates = st_data["last_active_drawing"].get("geometry", {}).get("coordinates")

    if coordinates is not None and len(coordinates) == 2:
        # Extract latitude and longitude
        latitude, longitude = coordinates
        st.write(f"Last Clicked Latitude: {latitude}")
        st.write(f"Last Clicked Longitude: {longitude}")
else:
    st.warning("Please select the marker and click on the map to retrieve coordinates")




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
