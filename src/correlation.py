# NOT NEEDED ANYMORE

import pandas as pd
import numpy as np
import geopandas as gpd


def percentage(df_in):
    df = df_in.copy()

    # Change types etc.
    df = df.replace('...', 0)
    df = df.fillna(0)
    df['YES_IN_PER'] = df['YES_IN_PER'].astype(float)
    df['BIKE_STREET_PER'] = df['BIKE_STREET_PER'].astype(float)

    # Change percentages to decimals
    df['YES_IN_PER'] = df['YES_IN_PER'] / 100
    df['BIKE_STREET_PER'] = df['BIKE_STREET_PER'] / 100

    return df


def calc_ratio(df_in):
    df = df_in

    max = df['BIKE_STREET_PER'].max()
    df['MAX_RATIO'] = ((df['BIKE_STREET_PER'] * 100) / max)
    df['MAX_RATIO'] = round(df['MAX_RATIO'] / 100, 4)

    return df


def calc_corr_bz(df_in, master):
    df = df_in

    #df = df.replace('...', 0)
    #df['YES_IN_PER'] = df['YES_IN_PER'].astype(float) /100
    #df['MAX_RATIO'] = df['MAX_RATIO']/100

    correlations = df.groupby(
        'BZNR')[['YES_IN_PER', 'MAX_RATIO']].corr(numeric_only=True)

    df = correlations.reset_index()
    df_selected = df[df.index % 2 == 0]
    # create a new DataFrame with only the 'BZNR' and 'MAX_RATIO' columns
    df_new = df_selected[['BZNR', 'MAX_RATIO']].copy()
    df_new = df_new.rename(columns={'MAX_RATIO': 'CORR'})

    # merge master and de_new on 'BZNR' and only keep the 'CORR' column from df_new

    # only merge the column 'CORR' from df_new
    df_out = master.merge(df_new, on='BZNR', how='left')

    #df_out = df_out.drop(columns=['MAX_RATIO'])

    return df_out


def calc_corr_ch(df_in):
    df = df_in
    # calculate correlation between 'YES_IN_PER' and 'BIKE_STREET_PER'
    correlation = df.corr(method='pearson', min_periods=1)[
        'YES_IN_PER']['BIKE_STREET_PER']

    return correlation


def acc_per100k(df_in):
    master = df_in
    master = master.fillna(0)
    master['ACCIDENTS_PER_100K'] = master['ACCIDENTS'] / \
        master['POP_TOTAL'] * 100000
    master = master.replace([np.inf, -np.inf], 0)

    return master


def export_accidents(df_in):
    # Export the mean accidents per 100k inhabitants per KTNR
    df = df_in
    df = df.groupby('KTNR')['ACCIDENTS_PER_100K'].mean()
    # Rename columns to 'KTNR' and 'ACCIDENTS_PER_100K'
    df = df.reset_index()
    df.ACCIDENTS_PER_100K = df.ACCIDENTS_PER_100K.round(2)
    df.to_csv('../export/accidents/acc_p_100.csv', index=False)
    return print('Accidents Dataframe exported to ../export/accidents/acc_p_100.csv')


def export_geojson(df_in):
    df_in.to_file("../export/master/master_acc_bike_pop_street_corr.geojson",
                  driver='GeoJSON')
    return print('Dataframe exported to ../export/master/master_acc_bike_pop_street_corr.geojson')


if __name__ == '__main__':
    master = gpd.read_file(
        '../export/master/master_acc_bike_pop_street.geojson')
    master = acc_per100k(master)
    export_accidents(master)
    master = percentage(master)
    corr_df = calc_corr_bz(calc_ratio(master), master)
    export_geojson(corr_df)
    print(calc_corr_ch(master))
