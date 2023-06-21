import json

print("reading")
with open("cities_dense.json", "r") as f:
    in_text = f.read()

print("loading")
data = json.loads(in_text)

states = set()
for c in data:
    state = c["admin1_code"]
    if not state or state in states:
        continue
    if state.isalpha():
        states.add(state)
    # print(json.dumps(countries, indent=2))
    # input()
states = [i for i in states]

print("dumping")
out_text = json.dumps(states, indent=2)

print("writing")
with open("states.json", "w") as f:
    f.write(out_text)

print("finished")





#   {
#     "geoname_id": "914959",
#     "name": "Kalulushi",
#     "ascii_name": "Kalulushi",
#     "alternate_names": [
#       "Kalulshi",
#       "Kalulushi"
#     ],
#     "feature_class": "P",
#     "feature_code": "PPL",
#     "country_code": "ZM",
#     "cou_name_en": "Zambia",
#     "country_code_2": null,
#     "admin1_code": "08",
#     "admin2_code": null,
#     "admin3_code": null,
#     "admin4_code": null,
#     "population": 66575,
#     "elevation": null,
#     "dem": 1304,
#     "timezone": "Africa/Lusaka",
#     "modification_date": "2012-06-20",
#     "label_en": "Zambia",
#     "coordinates": {
#       "lon": 28.09479,
#       "lat": -12.84151
#     }
#   },