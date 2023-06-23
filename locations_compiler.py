import json

print("reading")
with open("countries.json", "r") as f:
    countries_text = f.read()
with open("cities_dense.json", "r") as f:
    cities_text = f.read()
with open("states.json", "r") as f:
    states_text = f.read()
with open("short_words.json", "r") as f:
    conflicts_text = f.read()

print("loading")
cities_data = json.loads(cities_text)
countries_data = json.loads(countries_text)
states_data = json.loads(states_text)
conflicts = json.loads(conflicts_text)

print("organization")

# CITY, COUNTY, STATE, STATE_ABBREVIATION, COUNTRY, ZIPCODE
cities = set()
# counties = set()
states = set()
state_abbr = set()
countries = set()
countries_abb = set()
#zipcodes

# i = 0
for c in cities_data:
    # print(json.dumps(c, indent=2))
    # input()
    # if c["population"] < 10**4:
    #     continue
    # i += 1

    # cities.add(c["name"])
    cities.add(c["ascii_name"])
    if c["alternate_names"]:
        for n in c["alternate_names"]:
            cities.add(n)
# print(i)
# input()

for abb, s in states_data.items():
    states.add(s)
    state_abbr.add(abb)

for c in countries_data:
    countries.add(c["name"])
    countries_abb.add(c["code"])

locations = set()
locations.update(cities)
locations.update(states)
locations.update(state_abbr)
locations.update(countries)
locations.update(countries_abb)

print("filtering for ascii")

def is_ascii(s):
    if not s:
        return False
    return all(ord(c) < 128 for c in s)

ascii_locations = []
for l in locations:
    if is_ascii(l):
        ascii_locations.append(l.lower())

        # Remove conflicts
        if ascii_locations[-1] in conflicts:
            ascii_locations.pop()





print("dumping")
out_text = json.dumps(ascii_locations, indent=2)

print("writing")
with open("locations.json", "w") as f:
    f.write(out_text)

print("finished")






#   {
#     "geoname_id": "5318313",
#     "name": "Tucson",
#     "ascii_name": "Tucson",
#     "alternate_names": [
#       "Fucson",
#       "Lucson",
#       "San Casme del Tucson",
#       "TUS",
#       "Takson",
#       "Teuson",
#       "Toison",
#       "Touson",
#       "Tucson"
#     ],
#     "feature_class": "P",
#     "feature_code": "PPLA2",
#     "country_code": "US",
#     "cou_name_en": "United States",
#     "country_code_2": null,
#     "admin1_code": "AZ",
#     "admin2_code": "019",
#     "admin3_code": null,
#     "admin4_code": null,
#     "population": 531641,
#     "elevation": "759",
#     "dem": 757,
#     "timezone": "America/Phoenix",
#     "modification_date": "2019-09-05",
#     "label_en": "United States",
#     "coordinates": {
#       "lon": -110.92648,
#       "lat": 32.22174
#     }
#   },