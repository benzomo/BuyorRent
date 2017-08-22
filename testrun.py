import make_plt
from numpy import sin
import numpy as np
import housingCalc

import pandas as pd


x = np.linspace(0,100,num=101)
k = np.random.normal()
y = sin((x/ k))
m = [x, y]
m = np.reshape(m, (2, 101)).T



'''
Declare Housing Variables----------------------------
'''
lev = 3
levI = 3
n_income = 50000
savings0 = 250000
m_term = 25
m_termI = 25
t_max = 30
p_price = 500000
p_priceI = 500000

isInv = 0
notRent = 0

savings = np.empty(t_max*12)
eq = np.empty(t_max*12)
nw = np.empty(t_max*12)

'''
-----------------------------------------------------
'''

p, ax = make_plt.line(m)
p.show()
ax.plot(m[:,1]+1)


a = housingCalc.update_v()




a.to_csv('test.csv', sep=',', encoding='utf-8')


'''
m_data, time, m_pmt, m_ipmt, m_ppmt = housingCalc.mort(lev, p_price, savings0, m_term, t_max)



for i in range(t_max*12):
    if time[i,0] == 0:
        dp = p_price/(lev + 1)
        savings[0] = savings0 - dp
        eq[0] = dp
        nw[0] = savings0
    else:
        savings[i] = savings[i-1] + n_income/12 - m_pmt[i]
        eq[i] = eq[i-1] + m_ppmt[i]
        nw[i] = eq[i] + savings[i]


n_varData = np.array((savings, eq, nw)).T

data1 = pd.DataFrame(n_varData, columns=['Savings', 'Equity', 'Net Wealth'])

b = data1.ix[:, 0:3]
b_np = np.asmatrix(b)
'''

data, n_data = housingCalc.simulate(lev, levI, n_income, savings0, m_term, t_max, p_price, m_termI, p_priceI, isInv, notRent)


#data = pd.concat([data, m_data], axis=1)









