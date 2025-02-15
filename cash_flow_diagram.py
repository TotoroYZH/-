'''
Copyright (c) 2025 TotoroYZH, Interstellar Wanderers (Butian Gongcheng Club, Hangzhou No.2 High School of Zhejiang Province)

Access to the program is granted only to members of Interstellar Wanderers (Butian Gongcheng Club, Hangzhou No.2 High School of Zhejiang Province).

If there is a need for collaboration at GFSSM China Finals, the program may be considered for use by CD members of
Interstellar Wanderers (Butian Gongcheng Club, Hangzhou No.2 High School of Zhejiang Province) team's company in the 24 Hour
Extreme Design Challenge. However, such authorization is limited to the duration of the 24 Hour Design Challenge at GFSSM
China Finals, and non-Interstellar Wanderers (Butian Gongcheng Club, Hangzhou No.2 High School of Zhejiang Province) members
who are temporarily granted access to the program during this period are not authorized to use or distribute the program or
any part thereof outside of this period.
'''

import pandas as pd
import matplotlib.pyplot as plt

class Drawer:
    '''
    This class provides basic functionality for drawing cash flow diagram.

    Attributes:
        rd (str, optional): The path of the data file which needs to be a .xlsx file. Defaults to 'data.xlsx'.
        sheet_name (str, optional): The sheet containing the data. Defaults to 'Cash Flow Diagram'.
        min_time (int, optional): The beginning year of cash flow diagram. Defaults to 2064.
        max_time (int, optional): The ending year of cash flow diagram. Defaults to 2121.

    Example:
        >>> my_drawer = Drawer('C:/Users/Username/Documents/example.xlsx', 'example')
        >>> my_drawer.draw()
        [Then you will get a cash flow diagram.]
    '''
    def __init__(self,rd='data.xlsx',sheet_name='Cash Flow Diagram'):
        '''
        Initialize a new instance of Drawer.

        Args:
            rd (str, optional): The path of the data file which needs to be a .xlsx file. Defaults to 'data.xlsx'.
            sheet_name (str, optional): The sheet containing the data. Defaults to 'Cash Flow Diagram'.
            min_time (int, optional): The beginning year of cash flow diagram. Defaults to 2064.
            max_time (int, optional): The ending year of cash flow diagram. Defaults to 2121.
        '''
        self.colors = [(0,0,0.85),(0.9,0.2,0.2),(1,0.8,0.2),'green'] # blue, orange, yellow, green
        self.df = pd.read_excel('data.xlsx',sheet_name='Cash Flow Diagram') # recommended xlrd version: 1.2.0

        self.fig, self.ax1 = plt.subplots() # ax1: the left y-axis
        self.ax2 = self.ax1.twinx() # ax2: the right y-axis
        
        self.start = self.df.at[self.df.index[0],self.df.columns[0]]
        self.end = self.df.at[self.df.index[-1],self.df.columns[0]]
        plt.xlim(self.start-1,self.end+1)
        
        plt.rcParams['axes.unicode_minus'] = False # normally display minus
        
    def get_color(self):
        '''
        Get a color from colors, cycle processing.

        Returns:
            An element of colors.
        '''
        self.colors.append(self.colors.pop(0))
        return self.colors[-1]
    
    def get_xposr(self,val):
        '''
        Calculate the given year's relative position (a bit to the right) in the x-axis.

        Args:
            val (int): The year given.

        Returns:
            float: the given year's relative position (a bit to the right) in the x-axis.
        '''
        return (val-self.start+1)/(self.end-self.start+1)
    
    def get_xposl(self,val):
        '''
        Calculate the given year's relative position (a bit to the left) in the x-axis.

        Args:
            val (int): The year given.

        Returns:
            float: the given year's relative position (a bit to the left) in the x-axis.
        '''
        return (val-self.start)/(self.end-self.start+1)
    
    def ax1_zero(self,broken_ranges,color='black',ls1='-',ls2='--'):
        '''
        Draw the line y=0 in ax1.
        For ranges which data given include, draw them in the linestyle ls1.
        For ranges which data given does not include, draw them in the linestyle ls2. 

        Args:
            broken_ranges (list): The list store the ranges which data given does not include.
            color (Union[str, tuple], optional): The color in which the line will be drawn. Defaults to 'black'.
            ls1 (str, optional): Linestyle 1. Defaults to '-' which represents solid line.
            ls2 (str, optional): Linestyle 2. Defaults to '--' which represents dotted line.
        '''
        if broken_ranges:
            self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1, xmax=self.get_xposr(broken_ranges[0][0]))
            for i in range(len(broken_ranges)-1):
                self.ax1.axhline(y=0, color=color, linestyle=ls2, linewidth=1, xmin=self.get_xposl(broken_ranges[i][0]), xmax=self.get_xposr(broken_ranges[i][1]))
                self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1, xmin=self.get_xposl(broken_ranges[i][1]), xmax=self.get_xposr(broken_ranges[i+1][0]))
            self.ax1.axhline(y=0, color=color, linestyle=ls2, linewidth=1, xmin=self.get_xposl(broken_ranges[-1][0]), xmax=self.get_xposr(broken_ranges[-1][1]))
            self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1, xmin=self.get_xposl(broken_ranges[-1][1]))
        else:
            self.ax1.axhline(y=0, color=color, linestyle=ls1, linewidth=1)
    
    def draw(self):
        '''
        Draw the cash flow diagram you want.
        '''
        # set labels and axises
        self.ax1.set_xlabel(self.df.columns[0])
        self.ax1.set_ylabel('Income Per Year (Billion RMB)')
        self.ax1.tick_params(axis='both',direction='in') # set both axises' scale line direction of ax1 as 'in'
        self.ax2.set_ylabel('Total Profits (Billion RMB)')
        self.ax2.tick_params(axis='both',direction='in') # set both axises' scale line direction of ax2 as 'in'

        # find broken ranges
        broken_ranges = []
        for i in self.df.index[:-1]:
            if self.df.at[i+1,self.df.columns[0]]-self.df.at[i,self.df.columns[0]] > 1:
                broken_ranges.append([self.df.at[i,self.df.columns[0]],self.df.at[i+1,self.df.columns[0]]])

        # draw bars and plot
        for col in self.df.columns[1:-1]:
            self.ax1.bar(self.df[self.df.columns[0]],self.df[col],label=col,color=self.get_color())
        self.ax2.plot(self.df[self.df.columns[0]],self.df[self.df.columns[-1]],label=self.df.columns[-1],color=self.get_color())

        self.ax1_zero(broken_ranges) # draw y=0 in ax1
        self.ax2.axhline(y=0, color='black', linestyle='-', linewidth=1) # draw y=0 in ax2

        # set the legends' position and name the title
        self.ax1.legend(loc='lower right')
        self.ax2.legend(loc=(0.68,0.22))
        plt.title('Cash Flow Diagram')
        plt.show()

if __name__ == '__main__':      
    my_drawer = Drawer()
    my_drawer.draw()
