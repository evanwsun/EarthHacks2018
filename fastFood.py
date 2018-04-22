import pandas as pd
import matplotlib.pyplot as plt


class FastFood:
    def getCount(self, m,y):
        self.currentYear = self.xf[self.xf['Year'] == str(y)]
        self.currentMonth = self.currentYear[self.currentYear['Month'] == str(m)]
        return(len(self.currentMonth.index))

    def getSum(self, m,y):
        currentYear = self.xf[self.xf['Year'] == str(y)]
        currentMonth = currentYear[currentYear['Month'] == str(m)]
        self.xf['Sum'] = len(currentMonth.index)
        return(pd.to_numeric(currentMonth['Amount']).sum())

    def __init__(self, file):
        self.x = pd.read_csv(file)
        self.x = self.x.fillna(' ')
        #print(x)

        self.xf = self.x[self.x['Category'] == 'Fast Food']
        self.xf['Month'] = self.xf.Date.str[:2]
        self.xf['Year'] = self.xf.Date.str[-2:]
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                 'September', 'October', 'November', 'December']
        year = ['17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '18', '18', '18', '18', '18',
                '18', '18', '18', '18', '18', '18', '18']
        self.graph = pd.DataFrame(columns=['Month', 'Year', 'Count', 'Sum'])
        self.graph['Month'] = month
        self.graph['Year'] = year
        self.graph['Count'] = 0
        self.graph['Sum'] = 0.0

        for y in range(17, 19):
            for m in range(1, 13):
                if m < 10:
                    month = '0' + str(m)
                else:
                    month = str(m)
                if (y == 17):
                    self.graph.at[int(m) - 1, 'Count'] = self.getCount(month, y)
                    self.graph.at[int(m) - 1, 'Sum'] = self.getSum(month, y)
                if (y == 18):
                    self.graph.at[int(m) + 11, 'Count'] = self.getCount(month, y)
                    self.graph.at[int(m) + 11, 'Sum'] = self.getSum(month, y)







            #print('Month = '+str(m)+'   Year = '+str(y))
            #print('Count = '+ str(getCount(m,y)))
            #print('Sum = $'+ str(getSum(m,y))+ '\n')


    def printCountGraph(self, ax):
        self.graph.index= self.graph.Month+' '+self.graph.Year
        ax = self.graph[['Month','Count']].plot(kind='bar', color='c', title ="Frequency of Fast Food Consumption", figsize=(10, 5), legend=True, fontsize=12, ax = ax)
        ax.set_xlabel("Month", fontsize=8)
        ax.set_ylabel("# Times per Month", fontsize=12)
        return ax

    def printSumGraph(self, ax):
        self.graph.index = self.graph.Month + ' ' + self.graph.Year
        self.graph[['Month', 'Sum']].plot(kind='bar', color='c',title="Amount Spent on Fast Food", figsize=(10, 5), legend=True, fontsize=12, ax = ax)
        ax.set_xlabel("Month", fontsize=8)
        ax.set_ylabel("Amount Spent ($)", fontsize=12)
        return ax


if __name__ == '__main__':
    fastFoodObj = FastFood('transactions.csv')

