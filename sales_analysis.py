from imghdr import what
from math import prod
from typing import Any
from unittest import result
import pandas as pd
import os

import matplotlib.pyplot as plt
# empty_dataframe = pd.DataFrame()


# files = [file for file in os.listdir('./Sales_Data')]

# for file in files:
#     df = pd.read_csv('./Sales_Data/'+file)
#     empty_dataframe = pd.concat([empty_dataframe,df])


empty_list = [0,0,0,0,0,0,0,0,0,0,0,0]



def search_for_best_month_in_terms_of_value():
    df = pd.read_csv('all_month_data.csv')
    df = df.drop(columns=['Order ID', 'Product', 'Purchase Address'])
    df = df.dropna()
    print(df.head())
    for index,row in df.iterrows():
     order_date = row['Order Date']
     try:
        order_date = int(order_date[:2])
        #print(row['Price Each'])
        empty_list[order_date-1] += int(row['Quantity Ordered'])*float(row['Price Each'])
     except:
        pass
    print ('Month '+str(empty_list.index(max(empty_list))+1) + ' had the most sales in value')

def add_month_column():
    df = pd.read_csv('all_month_data.csv')
    df = df.drop(columns=['Order ID', 'Product', 'Purchase Address'])
    df = df.dropna()
    #df['Month'] = 0
    #for index,row in df.iterrows():
    #    try:
    #        simple_date = row['Order Date'][:2]
    #        df.at[index,'Month'] = simple_date
    #    except:
    #        pass
    df = df[df['Order Date'].str[:2] != 'Or']
    print(df.head())
    df['Month'] = df['Order Date'].str[:2]
    df['Month'] = df['Month'].astype('int32')
    df['Sales'] = (df['Quantity Ordered'].astype('int32') * df['Price Each'].astype('float32'))
    print(df.head())

    result = df.groupby('Month').sum()

    import matplotlib.pyplot as plt

    months = range(1,13)
    plt.bar(months, result['Sales'])
    plt.show()


def what_city_had_the_most_sale():
    df = pd.read_csv('all_month_data.csv')
    df = df.dropna()

    df['City'] = df['Purchase Address'].str.extract(r',([^,]*)')
    cities = []
    for index,row in df.iterrows():
        if row['City'] in cities:
            pass
        else:
            cities.append(row['City'])
    
    cities_dict = dict.fromkeys(cities,0)
    for index, row in df.iterrows():
        try:
            value = (float(row['Quantity Ordered'])) * (float(row['Price Each']))
            cities_dict[row['City']] += value
        except:
            pass

    
    city_name = list(cities_dict.keys())
    sold_in_city = list(cities_dict.values())

    plt.bar(range(len(cities_dict)), sold_in_city, tick_label=city_name)
    plt.show()
    print(cities_dict)


def get_city_and_PO(x):
    try:
        x = x.split(',')
        city = x[1]
        PO = x[2].split(' ')[1]
        x = city+" "+PO
    except:
        pass
    return x


def what_city_had_the_most_sale_BV():
    df = pd.read_csv('all_month_data.csv')
    df = df.dropna()
    df = df[df['Order Date'].str[:2] != 'Or']
    #df['City'] = df['Purchase Address'].str.extract(r',([^,]*)')
    df['City'] = df['Purchase Address'].apply(lambda x: get_city_and_PO(x))

    

    
    df['Value'] = (df['Quantity Ordered'].astype('int32') * df['Price Each'].astype('float32'))

    result = df.groupby('City').sum()
    print(result)
    #print(df.head())
    #print(df.columns)

    cities = df['City'].unique()
    cities.sort()
    print (cities)
    
    plt.bar(cities,result['Value'])
    plt.xticks(cities,rotation='vertical')
    plt.show()

def getDate(x):
    x = x.split('/')
    x = x[0]
    return int(x)

def what_time_to_show_ads():
    df = pd.read_csv('all_month_data.csv')
    df = df.dropna()
    df = df[df['Order Date'].str[:2] != 'Or']

    df['Order Date'] = pd.to_datetime(df['Order Date'])

    df['Hour'] = df['Order Date'].dt.hour
    df['Minute'] = df['Order Date'].dt.minute

    hours = df['Hour'].unique()
    hours.sort()

    print(df.groupby('Hour').count())


    
    
    


    print(df.head())

def what_products_are_most_often_sold_together():
    df = pd.read_csv('all_month_data.csv')
    df = df.dropna()
    df = df[df['Order Date'].str[:2] != 'Or']

    df = df[df['Order ID'].duplicated(keep=False)]
    print(df.head())

    df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
    df = df[['Order ID', 'Grouped']].drop_duplicates()

    res = df.groupby('Grouped').count()
    print(res)


    print(df.head())

    ####### No clue how to do this honestly



def what_products_are_sold_the_most():
    df = pd.read_csv('all_month_data.csv')
    df = df.dropna()
    df = df[df['Order Date'].str[:2] != 'Or']

    res = df.groupby('Product').count()
    #res = res['Order ID'].to_list()

    #products = df['Product'].unique()
    #print(products)

    # plt.bar(products,res)
    # plt.xticks(products, rotation='vertical')
    # plt.show()
    res = res.sort_values('Order ID')
    print(res['Order ID'])


if __name__ == '__main__':
    what_products_are_sold_the_most()


