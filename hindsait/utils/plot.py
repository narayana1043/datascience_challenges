from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon, Patch
from utils.errors import print_error
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class USMaps:

    available_colours = ['blue', 'orange', 'green', 'olive', 'purple', 'cyan']

    def __init__(self, state_borders=True, county_borders=True, state_names=False, map_boundaries=None):
        """
        basic attributes to generate the map

        :param state_borders: Boolean if True draw state borders
        :param county_borders: Boolean if True draw county borders
        :param state_names: Boolean if True draw add state names to plot
        :param map_boundaries: list of border latitude and longitudes
        """
        self.state_borders = state_borders
        self.county_borders = county_borders
        self.state_names = state_names

        if map_boundaries is None:
            map_boundaries = [-119, -64, 22.0, 50.5]

        # Set the lower left and upper right limits of the bounding box & calculate a center point the projection:
        self.llcrnrlon, self.urcrnrlon, self.llcrnrlat, self.urcrnrlat = map_boundaries

    def _initialize_map(self, llcrnrlon=None, llcrnrlat=None, urcrnrlon=None, urcrnrlat=None):
        """
        private method to draw the outline of the map

        :param llcrnrlon: lower lon boundary
        :param llcrnrlat: lower lat boundary
        :param urcrnrlon: upper lon boundary
        :param urcrnrlat: upper lat boundary
        :return:
        """
        if not all(var is None for var in [llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat]):
            self.llcrnrlon, self.llcrnrlat, self.urcrnrlon, self.urcrnrlat = llcrnrlon, llcrnrlat, urcrnrlon, \
                                                                             urcrnrlat, lon_0, lat_0

        self.lon_0 = float(self.llcrnrlon + self.urcrnrlon) / 2.0
        self.lat_0 = float(self.llcrnrlat + self.urcrnrlat) / 2.0

        base_map = Basemap(llcrnrlon=self.llcrnrlon, llcrnrlat=self.llcrnrlat, urcrnrlon=self.urcrnrlon,
                           urcrnrlat=self.urcrnrlat, lon_0=self.lon_0, lat_0=self.lat_0,
                           projection='tmerc', resolution='i')

        # read basemap info files that are downloaded into the folder basemaps under the project root

        base_map.readshapefile('./basemaps/cb_2016_us_state_500k', 'states', drawbounds=self.state_borders, color="red",
                               linewidth=1)
        base_map.readshapefile('./basemaps/cb_2016_us_county_500k', 'counties', drawbounds=self.county_borders,
                               color="black", linewidth=0.4)

        if self.state_names:
            printed_names = []
            for state_info, state in zip(base_map.states_info, base_map.states):
                short_name = state_info['STUSPS']
                if short_name in printed_names:
                    continue
                # center of polygon : can be improved by giving exact locations
                x, y = np.array(state).mean(axis=0)
                # You have to align x,y manually to avoid overlapping for little states
                plt.text(x + .1, y, short_name, ha="center")
                printed_names.append(short_name)

        return base_map

    def colour_code_usa_country(self, data, title="Title", desc=None, level='county'):
        """
        add colours to the us map at a chosen level

        :param data: dict with category names as the keys
        :param title: tile of the plot
        :param desc: description to be added to the plot
        :param level: level at which we have to fill colors county or state
        :return:
        """
        base_map = self._initialize_map()
        categories = data.keys()
        assert len(categories) < 5, "Cannot handle more than 5 categories"
        category_colour = {category: colour for category, colour in
                           zip(categories, self.available_colours[:len(categories)])}

        # get current axes instance
        ax = plt.gca()

        # sets the colour of the county based on its category, if no category is given for a county then its colour is
        # white as white is the default colour assigned.
        if level == 'county':
            level_info = base_map.counties_info
            level_xy = base_map.counties
        elif level == 'state':
            level_info = base_map.states_info
            level_xy = base_map.states
        else:
            print_error(error='level')

        for level_index, level_info in enumerate(level_info):
            seg = level_xy[level_index]
            st_code = level_info['STATEFP']
            fp_code = level_info['COUNTYFP']
            for category in categories:
                if (st_code, fp_code) in data[category]:
                    poly = Polygon(seg, facecolor=category_colour[category])
                    ax.add_patch(poly)
                    break
                else:
                    poly = Polygon(seg, facecolor=self.available_colours[-1])
                    ax.add_patch(poly)

        patch_list = [Patch(color=category_colour[category], label=str(category)) for category in categories] + [
            Patch(color=self.available_colours[-1], label='Unlabelled')]

        legend = plt.legend(handles=patch_list)
        legend.get_frame().set_color('grey')

        title = plt.title(title)
        title.set_color('grey')

        if desc is not None:
            plt.figtext(x=0.5, y=0, s=desc, wrap=True, horizontalalignment='center', fontsize=8)

        plt.show()

    def colour_code_usa_state(self, data, state, title="Title", desc=None):
        """
        colour coding any state in us and plots the map

        :param data: a dictionary with categories as keys and their values as county fp codes
        :param state: the state [name/2 letter abbrev/fip code] of our interest
        :param title: the title for the plot of the map
        :param desc: decription of the plot of the map
        :return:
        """

        assert state, 'set one of the below equal to param state. ' \
                      '\n 1. state_name \n 2. state_abbrev \n 3. state_fip_code'

        state = state.lower()
        state_df = pd.read_csv('./csv_data/fips_state_codes.csv', dtype=str)
        base_map = self._initialize_map()

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

        categories = data.keys()
        assert len(categories) < 5, "Cannot handle more than 5 categories"
        category_colour = {category: colour for category, colour in
                           zip(categories, self.available_colours[:len(categories)])}

        # current axes instance
        ax = plt.gca()

        # get map boundaries
        geo_lines_dict_keys = ['llcrnrlon', 'urcrnrlon', 'llcrnrlat', 'urcrnrlat']
        geo_lines_dict_values = [180, -180, 90, -90]
        geo_lines_dict = {x: y for x, y in zip(geo_lines_dict_keys, geo_lines_dict_values)}

        states_info_list = [sn[key].lower() for sn in base_map.states_info]
        for states_info_index, _ in enumerate(states_info_list):
            if state == states_info_list[states_info_index]:
                state_boundary_values = [(base_map(xy[0], xy[1], True))
                                         for xy in base_map.states[states_info_index]]

                geo_lines_dict['llcrnrlat'] = min(geo_lines_dict['llcrnrlat'],
                                                  min(state_boundary_values, key=itemgetter(1))[1] - 0.5)
                geo_lines_dict['urcrnrlat'] = max(geo_lines_dict['urcrnrlat'],
                                                  max(state_boundary_values, key=itemgetter(1))[1] + 0.5)
                geo_lines_dict['urcrnrlon'] = max(geo_lines_dict['urcrnrlon'],
                                                  max(state_boundary_values, key=itemgetter(0))[0] + 0.5)
                geo_lines_dict['llcrnrlon'] = min(geo_lines_dict['llcrnrlon'],
                                                  min(state_boundary_values, key=itemgetter(0))[0] - 0.5)

        geo_lines_dict_values = [geo_lines_dict[key] for key in geo_lines_dict_keys]

        self.llcrnrlon, self.urcrnrlon, self.llcrnrlat, self.urcrnrlat = geo_lines_dict_values

        del base_map
        base_map = self._initialize_map()

        for county_index, county_info in enumerate(base_map.counties_info):
            seg = base_map.counties[county_index]
            county_fip = county_info['COUNTYFP']
            state_fip = county_info['STATEFP']
            for category in categories:
                if (state_fip, county_fip) in data[category] and state_fip == state_fip_given:
                    poly = Polygon(seg, facecolor=category_colour[category])
                    ax.add_patch(poly)
                    break
                elif state_fip == state_fip_given:
                    poly = Polygon(seg, facecolor=self.available_colours[-1])
                    ax.add_patch(poly)

        patch_list = [Patch(color=category_colour[category], label=str(category)) for category in categories] + [
            Patch(color=self.available_colours[-1], label='Unlabelled')]

        legend = plt.legend(handles=patch_list, loc='center left', bbox_to_anchor=(1, 0.5))
        legend.get_frame().set_color('grey')

        title = plt.title(title + ' - ' + state_name.upper())
        title.set_color('grey')

        if desc is not None:
            plt.figtext(x=0.5, y=0, s=desc, wrap=True, horizontalalignment='center', fontsize=8)

        plt.show()

        return None
