#!/usr/local/bin/python3

import mne
import numpy as np
import json
import os
import shutil


def mean_transformation_matrix(list_raw):
    """Compute the mean transformation matrix across all runs thanks to head position registered at the beginning
    of each run.

    Parameters
    ----------
    list_raw: list of instance of mne.io.Raw
        List of all the runs that we want to realign by computing the mean transformation matrix.
        At least two runs are required.

    Returns
    -------
    mean_tm_raw: instance of mne.io.Raw
        The mean transformation matrix across all runs saved in a .fif file. 
    """

    # Create an empty 3D matrix that will contain for each file its transposition matrix
    pos = np.zeros((len(list_raw), 4, 4))

    # Loop to store the transposition matrix of each file
    for raw, i in zip(list_raw, range(len(list_raw))):
        pos[i] = raw.info["dev_head_t"]["trans"]

    # Create info object of an empty .fif file from info of the first run
    ch_names = list_raw[0].info["ch_names"]
    sfreq = list_raw[0].info["sfreq"]
    mean_tm_info = mne.create_info(ch_names, sfreq=sfreq)

    # Compute the mean of all matrices across the files and store it in mean_tm_info
    mean_tm_info["dev_head_t"]["trans"] = np.mean(pos, axis=0)

    # Create data
    data = np.ones([len(ch_names), 1])

    # Create raw object
    mean_tm_raw = mne.io.RawArray(data, mean_tm_info)
    mean_tm_raw.save('out_dir/destination.fif', overwrite=True)

    return mean_tm_raw 


def main():

    # Generate a json.product to display messages on Brainlife UI
    dict_json_product = {'brainlife': []}

    # Load inputs from config.json
    with open('config.json') as config_json:
        config = json.load(config_json)

    # Read all raw files and store them in a list
    list_raw = []
    for data_file in config["fif_runs"]:
        raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)
        list_raw.append(raw)

    if len(config["fif_runs"]) < 2:
        value_error_message = f'Only one run was given. This App needs at least two runs to compute ' \
                              f'the mean transformation matrix.'
        raise ValueError(value_error_message)

    # Read and save the fif file to be preprocess
    data_file = (config.pop('fif'))
    raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)
    raw.save("out_dir/meg.fif", overwrite=True)

    # Read the crosstalk files
    cross_talk_file = config.pop('crosstalk')
    if os.path.exists(cross_talk_file) is True:
        shutil.copy2(cross_talk_file, 'out_dir/crosstalk_meg.fif')  # required to run a pipeline on BL

    # Read the calibration file
    calibration_file = config.pop('calibration')
    if os.path.exists(calibration_file) is True:
        shutil.copy2(calibration_file, 'out_dir/calibration_meg.dat')  # required to run a pipeline on BL

    # Get head pos file
    head_pos = config.pop('headshape')
    if os.path.exists(head_pos) is True:
        shutil.copy2(head_pos, 'out_dir/headshape.pos')  # required to run a pipeline on BL

    # Compute mean transformation matrix
    mean_transformation_matrix(list_raw)

    # Success message in product.json
    dict_json_product['brainlife'].append({'type': 'success',
                                           'msg': 'Mean transformation matrix was computed successfully.'})

    # Save the dict_json_product in a json file
    with open('product.json', 'w') as outfile:
        json.dump(dict_json_product, outfile)


if __name__ == '__main__':
    main()
