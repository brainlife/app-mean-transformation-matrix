#!/usr/local/bin/python3

import mne
import numpy as np
import json

# Generate a json.product to display messages on Brainlife UI
dict_json_product = {'brainlife': []}

# Load inputs from config.json
with open('config.json') as config_json:
    config = json.load(config_json)

# Read all raw files and store them in a list
keys = list(config.keys())
list_raw = []
for i in range(len(keys)):
    data_file = str(config.pop(keys[i]))
    raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)
    list_raw.append(raw)

# Create an empty 3D matrix that will contain for each file its transposition matrix
pos = np.zeros((len(keys), 4, 4))

# Loop to store the transposition matrix of each file
for raw, i in zip(list_raw, range(len(keys))):
    pos[i] = raw.info["dev_head_t"]["trans"]

# Create info object of an empty .fif file from info of the first run
ch_names = list_raw[0].info["ch_names"]
sfreq = list_raw[0].info["sfreq"]
mean_tm_info = mne.create_info(ch_names, sfreq=sfreq)

# Compute the mean of all matrices across the files and store it in mean_tm_info
mean_tm_info["dev_head_t"]["trans"] = np.mean(pos, axis=0)

# Add dig info to the empty .fif too
mean_tm_info['dig'] = list_raw[0].info['dig']

# Create raw object
data = np.ones([len(ch_names), 1])

# Link false data and info to create the .fif
mean_tm_raw = mne.io.RawArray(data, mean_tm_info)
mean_tm_raw.save('out_dir/mean_tm-raw.fif', overwrite=True)

# Success message in product.json
dict_json_product['brainlife'].append({'type': 'success',
                                       'msg': 'Mean transformation matrix was computed successfully.'})

# Save the dict_json_product in a json file
with open('product.json', 'w') as outfile:
    json.dump(dict_json_product, outfile)
