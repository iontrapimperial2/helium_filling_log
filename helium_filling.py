# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:22:35 2019

@author: JohannesMHeinrich
"""

from class_helium_filling import helium_filling



### parameter ### the data list to read in
name_data_input = '2018_11_16_data.txt'
name_data_input_2 = '2019_03_05_data.txt'
name_data_input_3 = '2019_05_23_data.txt'

### how many initial datapoints not to use for the linear fit
n = 0
### the He fill level we don't want to be below
level = 333

### output name for the plot
name_plot_output = 'plot_helium_filling.png'




###############################################################################
### initiate the instance    
he_fill = helium_filling(name_data_input_3)

### parse time data into values matplotlib can plot
dates = he_fill.timestamp()
values = he_fill.get_values()

### fit the data, n gives the start datapoint for the fit
x_fit, y_fit, dates_2, slope = he_fill.do_fit(dates, values, n, level)

### plot the data and save the plot
he_fill.do_plot(dates, values, x_fit, y_fit, level, name_plot_output)
###############################################################################