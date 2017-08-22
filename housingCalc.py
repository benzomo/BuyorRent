# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 19:20:50 2017

@author: benmo
"""
import numpy as np
import pandas as pd


def get_v():
    global infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap      
    
    infl = [0.02, 0.02, 0.02, 'infl']
    mterm_res = [10, 25, 30, 'mterm_res']
    mterm_inc = [10, 15, 25, 'mterm_inc']
    rate_m = [0.03, 0.04, 0.05, 'rate_m']
    rate_mkt = [0.04, 0.06, 0.08, 'rate_mkt']
    rate_mkt0 = [0.025, 0.04, 0.05, 'rate_mkt0']
    lev_res = [1, 4, 9, 'lev_res']
    lev_inc = [1, 4, 9, 'lev_inc']
    rent_paid = [1200, 1300, 1900, 'rent_paid']
    rent_income = [1100, 1650, 1750, 'rent_income']
    propTax = [0.006, 0.007, 0.01, 'propTax']
    appr_nominal = [0.01, 0.02, 0.03, 'appr_nominal']
    maint_th = [0.0025, 0.0025, 0.0025, 'maint_th']
    maint_h = [0.0075, 0.0075, 0.0075, 'maint_h']
    maint_c = [0.001, 0.001, 0.001, 'maint_c']
    maint_ap = [0, 0, 0, 'maint_ap']
    util_th = [150, 200, 350, 'util_th']
    util_h = [250, 350, 500, 'util_h']
    util_c = [75, 110, 150, 'util_c']
    util_ap = [0, 0, 0, 'util_ap']
    fees_th = [100, 200, 300, 'fees_th']
    fees_h = [0, 0, 0, 'fees_h']
    fees_c = [375, 500, 650, 'fees_c']
    fees_ap = [0, 0, 0, 'fees_ap']




def update_v(infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap):
    get_v()
    varName = np.array(['inflation', 'Mortgage Term \n Residence', 'Mortgage Term \n Income Property', 'Mortgage Rate', 'Stock Market \n Return', 'Stock Market \n Return @ t = 0', 'Leverage \n (Residence)', 'Leverage \n (Income Property)', 'Rent Paid', 'Rental Income', 'Property Tax (Rate)', 'Appreciation', 'Townhouse Maintenance', 'House Maintenance', 'Condo Maintenance', 'Appartment Maintenance', 'Utilities-Townhouse', 'Utilities-House', 'Utilities-Condo', 'Utilities-Appartment', 'Fees-Townhouse', 'Fees-House', 'Fees-Condo', 'Fees-Appartment'])
    varName = varName.reshape(1,varName.size)
    var_lmh = np.array([infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap]).T
    varArray = np.concatenate((varName, var_lmh)).T
    
    
    varArray_pd = pd.DataFrame(varArray, columns=['Variable', 'Low', 'Med', 'High', 'VarName'])
    
    
    
    
    return varArray_pd


def varTable(infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap):
    #get_v()
    in_v = update_v(infl, mterm_res, mterm_inc, rate_m, rate_mkt, rate_mkt0, lev_res, lev_inc, rent_paid, rent_income, propTax, appr_nominal, maint_th, maint_h, maint_c, maint_ap, util_th, util_h, util_c, util_ap, fees_th, fees_h, fees_c, fees_ap)
    return in_v

def updatevarT(in_v1):
    in_v1.iloc[1, 1] = 5


def mort(lev, p_price, mrate, mterm, t_end ):
    dp = p_price/(lev+1)    
    months = np.linspace(0, t_end*12-1, t_end*12)
    years = months/12
    time = np.array([years, months])
    months_xmort = np.zeros(t_end*12-1 - mterm*12)
    isPmt = np.concatenate((np.ones(mterm*12+1), months_xmort))
    mort0 = p_price - dp


    mort_pmt = np.pmt(mrate/12,mterm*12,-mort0)*isPmt
    mort_i = np.concatenate((np.ipmt(0.04/12,months[0:mterm*12+1], mterm*12, -mort0), months_xmort))
    mort_p = np.concatenate((np.ppmt(0.04/12,months[0:mterm*12+1],mterm*12,-mort0), months_xmort))
    
    data = np.concatenate((time, np.reshape(mort_pmt,(1,360))))
    data = np.concatenate((data, np.reshape(mort_i,(1,360))))
    data = np.concatenate((data, np.reshape(mort_p,(1,360)))).T
    
    m_data = pd.DataFrame(data, columns=['Years', 'Months', 'mort_pmt', 'mort_i', 'mort_p'])
    
    return m_data, time.T, mort_pmt, mort_i, mort_p


def simulate(levR, levI, n_income, savings0, m_termR, t_max, p_priceR, m_termI, p_priceI, isInv, notRent):

    get_v()
    m_data, time, m_pmt, m_ipmt, m_ppmt = mort(levR, p_priceR, rate_m[1], m_termR, t_max)
    m_dataI, timeI, m_pmtI, m_ipmtI, m_ppmtI = mort(levI, p_priceI, rate_m[1], m_termI, t_max)
    
    savings0_v = np.empty(t_max*12)
    savings = np.empty(t_max*12)
    eq = np.empty(t_max*12)
    eqI = np.empty(t_max*12)
    nw = np.empty(t_max*12)
    price = np.empty(t_max*12)
    priceI = np.empty(t_max*12)
    cashAfterInv_v = np.empty(t_max*12)
    earned_i_v = np.empty(t_max*12)
    earned_i0_v = np.empty(t_max*12)          
    roeq_RE_v = np.empty(t_max*12)
    totalInv_v = np.empty(t_max*12)
    mkt_r = np.empty(t_max*12)
    ni_RE_v = np.empty(t_max*12)
    
    for i in range(0, t_max*12):
        if time[i,0] == 0:
            dpR = p_priceR/(levR + 1)*notRent
            dpI = p_priceI/(levI + 1)*isInv
            savings0_v[0] = savings0 - dpR - dpI

            savings[0] = 0
            eq[0] = dpR*notRent
            eqI[0] = dpI*isInv
            nw[0] = savings0
            price[0] = p_priceR
            priceI[0] = p_priceI
            ni_RE_v[0] = 0
            
            
            totalInv_v[0] = 0
            roeq_RE_v[0] = 0
            mkt_r[0] = (rate_mkt[1] + 1) / (infl[1] + 1) - 1
            
        else:
        
            year = time[i,0]
            
            cash_in = n_income/12 + isInv*rent_income[1]
            r_rate_mkt0 = ((rate_mkt0[1]+1)/(infl[1]+1)) ** (1/12)-1
            r_rate_mkt = ((rate_mkt[1]+1)/(infl[1]+1)) ** (1/12)-1
            r_appr_nominal = ((appr_nominal[1]+1)/(infl[1]+1)) ** (1/12)-1
            ''' '''
            mkt_r[i] = mkt_r[i-1]
            
            
            price[i] = price[i-1]*(r_appr_nominal + 1)
            priceI[i] = priceI[i-1]*(r_appr_nominal + 1)
            eq[i] = notRent*(eq[i-1] + m_ppmt[i] + price[i] - price[i-1])
            eqI[i] = isInv*(eqI[i-1] + m_ppmtI[i] + priceI[i] - priceI[i-1])
            cash_outR = notRent*(price[i]*maint_c[1]/12 + price[i]*propTax[1]/12 + util_c[1] + fees_c[1] + m_pmt[i]/((infl[1]+1)**year)) + np.abs(notRent-1)*rent_paid[1]
            #paid_iR = notRent*mipmt/((infl[1]+1)**year)
            '''  '''
            cash_outI = isInv*(priceI[i]*maint_c[1]/12 + priceI[i]*propTax[1]/12 + util_c[1] + fees_c[1] + m_pmtI[i]/((infl[1]+1)**year))
            #paid_iI = isInv*(mipmtI/((infl[1]+1)**year))

    
            cashAfterShelter = cash_in - cash_outR
            cashAfterInv = cashAfterShelter - cash_outI

            ni_RE = isInv*(rent_income[1] - priceI[i]*maint_c[1]/12 - priceI[i]*propTax[1]/12 - util_c[1] - fees_c[1] - m_ipmtI[i]/((infl[1]+1)**year) + priceI[i] - priceI[i-1])

            earned_i_v[i] = savings[i-1]*r_rate_mkt
            earned_i0_v[i] = savings0_v[i-1]*r_rate_mkt0
            savings[i] = savings[i-1] + earned_i_v[i] + cashAfterInv
            savings0_v[i] = savings0_v[i-1] + earned_i0_v[i]
            
            delnw = cashAfterInv + eq[i] - eq[i-1] + eqI[i] - eqI[i-1] + earned_i_v[i] + earned_i0_v[i] 
            
            roeq_RE_v[i] = (ni_RE)/eqI[i]*12 if isInv == 1 else 0
            ni_RE_v[i] = (ni_RE) if isInv == 1 else 0
            
            totalInv_v[i] = earned_i_v[i] + earned_i0_v[i]
            
            nw[i] = nw[i-1] + delnw
           
    n_varData = np.array((savings, savings0_v, cashAfterInv_v, earned_i0_v, earned_i_v, ni_RE_v,  eq, eqI, totalInv_v, mkt_r, roeq_RE_v,  nw)).T

    varData = pd.DataFrame(n_varData, columns=['Savings','Initial Savings', 'Cash Flow', 'Return @ t=0', 'Market Return', 'Net Income from Rental Property', 'Equity Residence', 'Equity Income Property', 'Total Market Income', 'Market Return (Real)', 'Return on Real Estate', 'Net Wealth'])
    data = pd.concat([m_data, m_dataI, varData], axis=1)
    
    return data, n_varData

    