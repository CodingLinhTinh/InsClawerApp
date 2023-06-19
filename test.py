from geopy.geocoders import Nominatim

def get_country_name(location):
    geolocator = Nominatim(user_agent="my_app")
    location_data = geolocator.geocode(location, exactly_one=True)
    if location_data:
        is_germany = location_data.raw['display_name'].split(",")[-1].strip()
        if is_germany == "Deutschland":
            return True
    return False

country = get_country_name("München")
print(country)