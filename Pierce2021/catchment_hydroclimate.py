#! /usr/bin/python2

from osgeo import gdal
import numpy as np
import netCDF4 as nc4
import glob
import datetime
import pandas as pd

river_names = [
               'cannon',
               'cottonwood',
               'grant',
               'kickapoo',
               'platte',
               'pomme_de_terre',
               'redwood',
               'root',
               'tremp',
               'vermillion',
               'yellow_medicine',
               'zumbro'
               ]

maskpath = '/home/awickert/Dropbox/Livneh_data_masks/'
outpath = '/home/awickert/Dropbox/River_hydroclimate_1915_2018/'
livnehpath = '/media/awickert/data1/Decadal_P_TW_LivnehCONUS/'

for river_name in river_names:

    print( "" )
    print( river_name + " STARTING" )
    print( "" )

    filepath = maskpath + river_name + '_mask.tif'

    _binary = gdal.Open(filepath)

    mask = _binary.GetRasterBand(1).ReadAsArray()[::-1]
    mask = mask.astype(float)
    
    # 1s are in catchment. All other values are out.
    mask[mask != 1] = np.nan

    Prec = []
    Tmax = []
    Tmin = []
    Wind = []
    date = []

    time_units = "days since 1899-12-31"

    ncfilenames = sorted(glob.glob('/media/awickert/data1/Decadal_P_TW_LivnehCONUS/*.nc'))

    # NOT CURRENTLY ACCOUNTING FOR DIFFERING AREA ACROSS WATERSHED
    # LESS IMPORTANT IN SMALL WATERSHED
    for ncfilename in ncfilenames:
        ncfile = nc4.Dataset(ncfilename)
        for i in range(len(ncfile['time'])):
            # mm/s to mm/day [ = mm, with daily time steps ]\
            _date = nc4.num2date(ncfile['time'][i], time_units)
            date.append(_date)
            Prec.append(np.nanmean(ncfile['Prec'][i] * mask)) # mm
            Tmax.append(np.nanmean(ncfile['Tmax'][i] * mask)) # degC
            Tmin.append(np.nanmean(ncfile['Tmin'][i] * mask)) # degC
            Wind.append(np.nanmean(ncfile['Wind'][i] * mask)) # m/s
            print( river_name, _date, Prec[-1], Tmax[-1], Tmin[-1], Wind[-1] )

    outData = pd.DataFrame()
    outData['Date'] = date
    outData['Precipitation [mm/day]'] = Prec
    outData['Maximum temperature [degC]'] = Tmax
    outData['Minimum temperature [degC]'] = Tmin
    outData['Wind speed [m/s]'] = Wind

    outData.to_csv(outpath+river_name+'.csv', index=False)
    print( "" )
    print( outpath+river_name+'.csv' + " WRITTEN" )
    print( "" )
    
