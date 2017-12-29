from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon, Patch
from utils.errors import print_error
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def base_map_usa(state_borders=True, county_borders=True, state_names=False, map_boundaries=[-119, -64, 22.0, 50.5]):
    """
    Creates a basemap object with the given parameters as input. Generates the basemap for the country US but by
     varying the parameter map boundaries we can get states or regions of interest in US.
    :param state_borders: True draws boarders
    :param county_borders: True draws boarders
    :param state_names:True puts names(2 letter abbreviations) on the states
    :param map_boundaries: [ll_lon, ur_lon, ll_lat, ur_lat]
    :return: returns a basemap object
    """
    # Set the lower left and upper right limits of the bounding box:
    llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat = map_boundaries

    # and calculate a centerpoint, needed for the projection:
    center_lon = float(llcrnrlon + urcrnrlon) / 2.0
    center_lat = float(llcrnrlat + urcrnrlat) / 2.0

    m = Basemap(resolution='i', llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon, lon_0=center_lon, llcrnrlat=llcrnrlat,
                urcrnrlat=urcrnrlat, lat_0=center_lat, projection='tmerc')
    # Other configurations
    # m.drawmapboundary(fill_color='ivory')
    # m.fillcontinents(color='coral', lake_color='aqua')
    # m.drawcoastlines()
    # m.drawcountries()
    # m.drawstates()

    # draw state boundaries using the maps in base maps folder

    state_info = m.readshapefile('./basemaps/cb_2016_us_state_500k', 'states', drawbounds=state_borders, color="red",
                                 linewidth=1)

    # County data from Census Bureau
    county_info = m.readshapefile('./basemaps/cb_2016_us_county_500k', 'counties', drawbounds=county_borders,
                                  color='black', linewidth=0.4)

    # adding state name abbreviation to the map
    # TODO: check for outlying states and put them on the us map
    if state_names:
        printed_names = []
        for state_info, state in zip(m.states_info, m.states):
            short_name = state_info['STUSPS']
            if short_name in printed_names:
                continue
            # center of polygon
            x, y = np.array(state).mean(axis=0)
            # You have to align x,y manually to avoid overlapping for little states
            plt.text(x + .1, y, short_name, ha="center")
            printed_names.append(short_name)



    return m


def colour_code_usa_country(data, title="Title", desc=None, state_borders=True, county_borders=True, state_names=False,
                            level='county'):
    """
    color coding states/counties based on the level set on whole US map and plots it.
    :param data: should be a dict with each key containing the list of states or counties in it
    :param title: Title for the plot; default is "Title"
    :param desc: Description of the plot, will be added below the plot
    :param state_borders: Boolean if true draws the boarders
    :param county_borders: Boolean if true draws the boarders
    :param state_names: Boolean if true diplays the state names as 2 letter abbreviations "location of the name needs
    update"
    :param level: state / county what type of data ?
    :return: None
    """
    m = base_map_usa(state_borders, county_borders, state_names)
    available_colours = ['blue', 'orange', 'green', 'olive', 'purple', 'cyan']
    categories = data.keys()
    assert len(categories) < 5, "Cannot handle more than 5 categories"
    category_colour = {category: colour for category, colour in zip(categories, available_colours[:len(categories)])}

    # get current axes instance
    ax = plt.gca()

    # sets the colour of the county based on its category, if no category is given for a county then its colour is white
    #  as white is the default colour assigned.
    if level == 'county':
        level_info = m.counties_info
        level_xy = m.counties
    elif level == 'state':
        level_info = m.states_info
        level_xy = m.states
    else:
        print_error(error='level')

    for level_index, level_info in enumerate(level_info):
        seg = level_xy[level_index]
        fp_code = level_info['COUNTYFP']
        for category in categories:
            if fp_code in data[category]:
                poly = Polygon(seg, facecolor=category_colour[category])
                ax.add_patch(poly)
                break
            else:
                poly = Polygon(seg, facecolor=available_colours[-1])
                ax.add_patch(poly)

    patch_list = [Patch(color=category_colour[category], label=str(category)) for category in categories] + [
        Patch(color=available_colours[-1], label='Unlabelled')]

    legend = plt.legend(handles=patch_list, loc='best', bbox_to_anchor=(1, 0.5), ncol=len(categories) + 1)
    legend.get_frame().set_color('grey')

    title = plt.title(title)
    title.set_color('grey')

    if desc is not None:
        plt.figtext(x=0.5, y=0, s=desc, wrap=True, horizontalalignment='center', fontsize=8)

    plt.show()

    return None


def colour_code_usa_state(data, state, title="Title", desc=None):
    """
    colour coding any state in us and plots the map
    :param data: a dictionary with categories as keys and their values as county fp codes
    :param state_name: the state name of our interest
    :param state_abbrev: the state name abbrev of our interest
    :param state_fip: the state fip code of our interest
    :param title: the title for the plot of the map
    :param desc: decription of the plot of the map
    :return: None
    """

    assert state, 'set one of the below equal to param state. \n 1. state_name \n 2. state_abbrev \n 3. state_fip_code'

    state = state.lower()
    state_df = pd.read_csv('./csv_data/fips_state_codes.csv', dtype=str)

    if state in state_df['STATE_NAME'].str.lower().tolist():
        key = 'NAME'
        state_name = state
        state_fip_given = state_df[state_df['STATE_NAME'].str.lower() == state]['STATE'].str.lower().tolist()[0]
    elif state in state_df['STATE']:
        key = 'STATEFP'
        state_name = state_df[state_df['STATE'] == state]['STATE_NAME'].str.lower().tolist()[0]
        state_fip_given = state_df[state_df['STATE'] == state]['STATE'].str.lower().tolist()[0]
    elif state in state_df['STUSAB'].str.lower().tolist():
        key = 'STUSPS'
        state_name = state_df[state_df['STUSAB'] == state.upper()]['STATE_NAME'].str.lower().tolist()[0]
        state_fip_given = state_df[state_df['STUSAB'] == state.upper()]['STATE'].str.lower().tolist()[0]
    else:
        print('state not found')

    available_colours = ['blue', 'orange', 'green', 'olive', 'purple', 'cyan']
    categories = data.keys()
    assert len(categories) < 5, "Cannot handle more than 5 categories"
    category_colour = {category: colour for category, colour in zip(categories, available_colours[:len(categories)])}

    m = base_map_usa(state_borders=True, county_borders=True, state_names=False)

    # current axes instance
    ax = plt.gca()

    # get map boundaries
    geo_lines_dict_keys = ['llcrnrlon', 'urcrnrlon', 'llcrnrlat', 'urcrnrlat']
    geo_lines_dict_values = [180, -180, 90, -90]
    geo_lines_dict = {x: y for x, y in zip(geo_lines_dict_keys, geo_lines_dict_values)}

    states_info_list = [sn[key].lower() for sn in m.states_info]
    for states_info_index, _ in enumerate(states_info_list):
        if state == states_info_list[states_info_index]:
            state_boundary_values = [(m(xy[0], xy[1], True)) for xy in m.states[states_info_index]]

            geo_lines_dict['llcrnrlat'] = min(geo_lines_dict['llcrnrlat'],
                                              min(state_boundary_values, key=itemgetter(1))[1] - 0.2)
            geo_lines_dict['urcrnrlat'] = max(geo_lines_dict['urcrnrlat'],
                                              max(state_boundary_values, key=itemgetter(1))[1] + 0.2)
            geo_lines_dict['urcrnrlon'] = max(geo_lines_dict['urcrnrlon'],
                                              max(state_boundary_values, key=itemgetter(0))[0] + 0.2)
            geo_lines_dict['llcrnrlon'] = min(geo_lines_dict['llcrnrlon'],
                                              min(state_boundary_values, key=itemgetter(0))[0] - 0.2)

    geo_lines_dict_values = [geo_lines_dict[key] for key in geo_lines_dict_keys]

    del m
    m = base_map_usa(state_borders=True, county_borders=True, state_names=False, map_boundaries=geo_lines_dict_values)

    # for geo_line_key, geo_line_value in geo_lines_dict.items():
    #     m.__setattr__(geo_line_key, geo_line_value)
    #     print(m.__getattribute__(geo_line_key))
    # -119, -64, 22.0, 50.5

    # state_fip_df = pd.read_csv('./csv_data/fips_state_codes.csv', dtype=str)
    # if key == 'STATE':
    #     state_name = state_fip_df[state_fip_df['STATE'] == state]['STATE_NAME'].tolist()[0]
    # elif key == 'STATE_NAME':
    #     state_fip_code = state_fip_df[state_fip_df['STATE_NAME'].str.lower() == state.lower()]['STATE'].tolist()[0]
    # elif key == 'STUSAB':
    #     state_fip_code = state_fip_df[state_fip_df['STUSAB'].str.lower() == state.lower()]['STATE'].tolist()[0]
    #     state_name = state_fip_df[state_fip_df['STUSAB'].str.lower() == state.lower()]['STATE_NAME'].tolist()[0]

    for county_index, county_info in enumerate(m.counties_info):
        seg = m.counties[county_index]
        county_fip = county_info['COUNTYFP']
        state_fip = county_info['STATEFP']
        for category in categories:
            if county_fip in data[category] and state_fip == state_fip_given:
                poly = Polygon(seg, facecolor=category_colour[category])
                ax.add_patch(poly)
                break
            elif state_fip == state_fip_given:
                poly = Polygon(seg, facecolor=available_colours[-1])
                ax.add_patch(poly)

    patch_list = [Patch(color=category_colour[category], label=str(category)) for category in categories] + [
        Patch(color=available_colours[-1], label='Unlabelled')]

    legend = plt.legend(handles=patch_list, loc='center left', bbox_to_anchor=(1, 0.5))
    legend.get_frame().set_color('grey')

    title = plt.title(title + ' - ' + state_name.upper())
    title.set_color('grey')

    if desc is not None:
        plt.figtext(x=0.5, y=0, s=desc, wrap=True, horizontalalignment='center', fontsize=8)

    plt.show()

    return None
