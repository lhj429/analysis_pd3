import json
import pandas as pd
import scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt
import math

def correlation_coefficient(x, y):
    n = len(x)
    vals = range(n)

    x_sum = 0.0
    y_sum = 0.0
    x_sum_pow = 0.0
    y_sum_pow = 0.0
    mul_xy_sum = 0.0

    for i in vals:
        mul_xy_sum = mul_xy_sum + float(x[i]) * float(y[i])
        x_sum = x_sum + float(x[i])
        y_sum = y_sum + float(y[i])
        x_sum_pow = x_sum_pow + pow(float(x[i]), 2)
        y_sum_pow = y_sum_pow + pow(float(y[i]), 2)

    try:
        r = ((n * mul_xy_sum) - (x_sum * y_sum)) / math.sqrt(((n * x_sum_pow) - pow(x_sum, 2)) * ((n * y_sum_pow) - pow(y_sum, 2)))
    except ZeroDivisionError:
        r = 0.0

    return r

def analysis_correlation(resultfiles):
    with open(resultfiles['tourspot_visitor'], 'r', encoding='utf-8') as infile:
        json_data = json.loads(infile.read())

    tourspotvisitor_table = pd.DataFrame(json_data, columns=['count_foreigner', 'date', 'tourist_spot'])
    temp_tourspotvisitor_table = pd.DataFrame(tourspotvisitor_table.groupby('date')['count_foreigner'].sum())

    results = []
    for filename in resultfiles['foreign_visitor']:
        with open(filename, 'r', encoding='utf-8') as infile:
            json_data = json.loads(infile.read())

        foreignvisitor_table = pd.DataFrame(json_data, columns=['country_name', 'date', 'visit_count'])
        foreignvisitor_table = foreignvisitor_table.set_index('date')
        merge_table = pd.merge(temp_tourspotvisitor_table, foreignvisitor_table, left_index=True, right_index=True)

        x = list(merge_table['visit_count'])
        y = list(merge_table['count_foreigner'])

        country_name = foreignvisitor_table['country_name'].unique().item()     # unique = district
        r = ss.pearsonr(x, y)[0]
        # r = np.corrcoef(x, y)[0]      # numpy : 부정확함
        results.append({'x':x, 'y':y, 'country_name':country_name, 'r':r})

        merge_table['visit_count'].plot(kind='bar')
        plt.show()

    return results

def analysis_correlation_by_tourspot(resultfiles):

    with open(resultfiles['tourspot_visitor'], 'r', encoding='utf-8') as infile:
        json_data = json.loads(infile.read())

    tourspot_table = pd.DataFrame(json_data, columns=['tourist_spot', 'count_foreigner', 'date'])
    tourist_spot = tourspot_table['tourist_spot'].unique()

    results = []
    for spot in tourist_spot:
        temp_tourspotvisitor_table = tourspot_table[tourspot_table['tourist_spot'] == spot]
        temp_tourspotvisitor_table = temp_tourspotvisitor_table.set_index('date')

        r = []
        for filename in resultfiles['foreign_visitor']:
            with open(filename, 'r', encoding='utf-8') as infile:
                json_data = json.loads(infile.read())

            foreignvisitor_table = pd.DataFrame(json_data, columns=['country_name', 'date', 'visit_count'])
            foreignvisitor_table = foreignvisitor_table.set_index('date')

            merge_table = pd.merge(temp_tourspotvisitor_table, foreignvisitor_table, left_index=True, right_index=True)

            x = list(merge_table['visit_count'])
            y = list(merge_table['count_foreigner'])

            r.append(correlation_coefficient(x, y))
        results.append({'tourspot':spot, 'r_중국':r[0], 'r_일본':r[1], 'r_미국':r[2]})

    return results

    '''
    results = []
    for filename in resultfiles['foreign_visitor']:
        with open(filename, 'r', encoding='utf-8') as infile:
            json_data = json.loads(infile.read())

            for spot in tourist_spot:
                temp_tourspotvisitor_table = tourspot_table[tourspot_table['tourist_spot'] == spot]
                temp_tourspotvisitor_table = temp_tourspotvisitor_table.set_index('date')

                foreignvisitor_table = pd.DataFrame(json_data, columns=['country_name', 'date', 'visit_count'])
                foreignvisitor_table = foreignvisitor_table.set_index('date')

                merge_table = pd.merge(temp_tourspotvisitor_table, foreignvisitor_table, left_index=True, right_index=True)
                print(merge_table)
    '''


            # results.append(r)

    # print(results)




    # country_name = foreignvisitor_table['country_name'].unique().item()  # unique = district
    # r = correlation_coefficient(x, y)
    #
    # results.append({'x': x, 'y': y, 'country_name': country_name, 'r': r})
    # print(results)