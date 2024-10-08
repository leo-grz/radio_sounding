from src import *
import sys
from time import perf_counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def main():

    start_time = perf_counter()

    config = load_json_data()
    config['sounding_file'] = 'data/windy_sounding4.json'

    # try:

    windy_sounding = load_json_data(config['sounding_file'])

    attributes = ['pressure', 'temp', 'dewpoint', 'gpheight', 'wind_u', 'wind_v']
    extracted_data = extract_data(windy_sounding, attributes) # extract data from raw json format
    extracted_data = clean_extracted_data(extracted_data, config) # clean data from outliers
    extracted_data = add_units(extracted_data) # add units to data for displaying and further calculations

    plot_extracted_data(extracted_data, config) # plot pressure, temperature, dewpoint, height and windspeeds for better data inspection
    params = calc_params(extracted_data) # calculate indices, temperatures, points like lcl, lfc, el, lcc, cape, cin...

    fig = plt.figure(figsize=tuple(config['figsize']))
    gs = gridspec.GridSpec(10, 15)
    gs_skewt = gs[:, 0:10] # location where to show skew-t
    ax_hodograph = fig.add_subplot(gs[0:5, 10:15]) # ax to plot hodograph on
    display_skewt_plot(extracted_data, config, params, fig, gs_skewt)
    display_hodograph_plot(extracted_data, config, ax_hodograph)

    sounding_properties = windy_sounding.get('properties', 1)
    display_parameters(config, params, fig, sounding_properties)

    print(f'Execution time: {perf_counter() - start_time:.4f} seconds')

    lon, lat = [sounding_properties.get(x, 1) for x in ['lon', 'lat']]
    open_google_maps(lat, lon)

    plt.title(config['sounding_file'])
    plt.show()

    # except FileNotFoundError as e: # if config- or data file are missing
    #     print(e.with_traceback) 
    #     sys.exit(1) 
    # except ValueError as e: # if there exist less than 5 data points
    #     print(e.with_traceback)
    #     sys.exit(1)
   
if __name__ == '__main__':
    main()