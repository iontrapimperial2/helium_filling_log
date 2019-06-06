# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:22:35 2019

@author: JohannesMHeinrich
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta, date
import numpy as np



class helium_filling:
    def __init__(self, data_file):
        ''' class gets initialized with with the parameter data_file = filename
            of the dataset in .txt format. file must be formated as described
            in function import_data(self)
        '''
        self.data_file = data_file       
        self.data = self.import_data()
        
        self.slope = 0.0
        self.y_value = 0.0
        self.fill_date = 0
        self.fill_date_str = 'blub'

    def import_data(self):
        ''' import data    
        '''
        data_file = open(self.data_file,'r')
        data_raw = data_file.readlines()        

        # parse data
        data = []
        for i in range(len(data_raw)):
            dd = data_raw[i]
            dd2 = dd.split(', ')         
            dd3 = [int(j) for j in dd2]
            data.append(dd3)
            
        return data
    
    
    def timestamp(self):
        ''' returns the dates in a format which can be used by pyplot 
        '''
        dates_01 = []
        for i in range(len(self.data)):
            date_format = str(self.data[i][0]) + ' ' + str(self.data[i][1]) + ' ' + str(self.data[i][2])
            datetime_object = datetime.strptime(date_format, '%d %m %Y')    
            dates_01.append(datetime_object)
        
        dates = mdates.date2num(dates_01)

        return dates
    
    
    def get_values(self):
        '''
        '''
        values = []
        for i in range(len(self.data)):
            values.append(self.data[i][3])
        
        return values
    
    
    def do_fit(self, dates, values, n, min_level):
        '''
        '''
        z4 = np.polyfit(dates[n:], values[n:], 1)
        p4 = np.poly1d(z4)
        
        self.slope = p4[1]
        self.y_value = p4[0]
        
        self.fill_date = (min_level - self.y_value)/self.slope
        fill_date_dt = datetime.fromordinal(int(self.fill_date))
        self.fill_date_str = str(fill_date_dt.day) + '/' + str(fill_date_dt.month) + '/' + str(fill_date_dt.year)
        
        xx = np.linspace(dates.min(), dates.max() + 14, 100)
        dd = mdates.num2date(xx)
        
        return xx, p4(xx), dd, self.slope
    
    
    def do_plot(self, dates, values, x_fit, y_fit, min_level, save_as):

        rule = mdates.rrulewrapper(mdates.WEEKLY)
        loc = mdates.RRuleLocator(rule)
        formatter = mdates.DateFormatter('%d/%m/%y')
        
        fig, ax = plt.subplots()
        plt.plot_date(dates, values)
        plt.plot(x_fit, y_fit, 'b-')
        plt.plot([x_fit[0],x_fit[-1]], [min_level,min_level], 'r-')        
                
        plt.ylim(300, 700) 
        
        plt.grid(True)
        
        plt.xticks(rotation=90)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(formatter)
        
        plt.title('Helium Fill Level')
        plt.text(dates.min() + 1, 425, 'by fit: ' + str("{:3.2f}".format(self.slope) + str(' units/day')), horizontalalignment='left', verticalalignment='center', fontsize=12)
        plt.text(dates.min() + 1, 375, 'est. date: ' + self.fill_date_str, horizontalalignment='left', verticalalignment='center', fontsize=12)
        #ax.xaxis.set_tick_params(rotation=30, labelsize=10)
        
#        now = datetime.now().date()
#        now_year = now.year
#        now_month = now.month
#        now_day = now.day
        
        
        fig.savefig(self.data_file[0:10] + '_' + save_as, bbox_inches='tight',dpi=400)        
    
    
