#! /usr/bin/python2

import glob
import numpy as np
from matplotlib import pyplot as plt
import netCDF4 as nc4
import datetime

def date_prec_tw(decade_yyyy, outname_nc):

    ncfilesP = sorted(glob.glob('/media/awickert/data1/LivnehUpdated/precip/livneh_unsplit_precip.2021-05-02.'
                                + ('%04d' %decade_yyyy)[:3] + '*.nc'))
    ncfilesTW = sorted(glob.glob('/media/awickert/data1/LivnehUpdated/temp_and_wind/livneh_lusu_2020_temp_and_wind.2021-05-02.'
                                + ('%04d' %decade_yyyy)[:3] + '*.nc'))

    date_list = []
    prec_list = []
    Tmax_list = []
    Tmin_list = []
    Wind_list = []
    
    # time_units = "days since 1899-12-31"

    print("Precipitation")
    for ncfile in ncfilesP:
        print ncfile
        yyyy = fname.split('.')[-2]
        fluxesP = nc4.Dataset(ncfile)
        for i in range(len(fluxesP.variables['Time'])):
            # Given in days since 1915.01.01
            # Adjusted as a counter
            dd = int(np.round(fluxesP.variables['Time'][i])) + 5478 + 1
            print dd
            prec = fluxesP.variables['PRCP'][i].data # mm
            prec[prec < -1E35] = np.nan
            prec_list.append(prec)
            
    print("Temperature and wind speed")
    for ncfile in ncfilesTW:
        print ncfile
        yyyy = fname.split('.')[-2]
        fluxesTW = nc4.Dataset(ncfile)
        for i in range(len(fluxesTW.variables['time'])):
            # Given in days since 1900.01.01
            dd = int(np.round(fluxesTW.variables['time'][i])) + 1
            print dd
            date_list.append(dd)
            # Values
            Tmax = fluxesTW.variables['Tmax'][i].data # degC
            Tmin = fluxesTW.variables['Tmin'][i].data # degC
            Wind = fluxesTW.variables['Wind'][i].data # m/s
            # Fill values
            Tmax[Tmax > 1E19] = np.nan
            Tmin[Tmin > 1E19] = np.nan
            Wind[Wind > 1E19] = np.nan
            Tmax_list.append(Tmax)
            Tmin_list.append(Tmin)
            Wind_list.append(Wind)

    prec_list = np.array(prec_list)
    Tmax_list = np.array(Tmax_list)
    Tmin_list = np.array(Tmin_list)
    Wind_list = np.array(Wind_list)

    outnc = nc4.Dataset(outname_nc, 'w', format='NETCDF4')

    outnc.createDimension('lon', len(fluxes['lon']))
    outnc.createDimension('lat', len(fluxes['lat']))
    # Sort of a hack -- these two are equal, but different capitalization
    # is used in each one and I don't want to deal with repeating
    outnc.createDimension('time', len(date_list))
    outnc.createDimension('Time', len(date_list))

    _lon = outnc.createVariable('lon', 'f4', fluxesP['lon'].dimensions)
    _lat = outnc.createVariable('lat', 'f4', fluxesP['lat'].dimensions)
    _Time = outnc.createVariable('Time', 'i4', fluxesP['Time'].dimensions)
    _time = outnc.createVariable('time', 'i4', fluxesTW['time'].dimensions)
    _prec = outnc.createVariable('Prec', 'f4', fluxesP['PRCP'].dimensions)
    _tmax = outnc.createVariable('Tmax', 'f4', fluxesTW['Tmax'].dimensions)
    _tmin = outnc.createVariable('Tmin', 'f4', fluxesTW['Tmin'].dimensions)
    _wind = outnc.createVariable('Wind', 'f4', fluxesTW['Wind'].dimensions)
    
    _time.units = time_units
    _Time.units = time_units

    _lon[:] = fluxes['lon']
    _lat[:] = fluxes['lat']
    _Time[:] = date_list
    _time[:] = date_list
    _prec[:] = prec_list
    _tmax[:] = Tmax_list
    _tmin[:] = Tmin_list
    _wind[:] = Wind_list
    
    outnc.close()
    
# 1910 and 2010 are partial decades
decade_list = [1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]

for decade in decade_list:
    outname_nc = '/media/awickert/data1/Decadal_P_TW_LivnehCONUS/' \
                  + 'LivnehCONUS_P_TW_' + str(decade) + 's.nc'
    date_prec_tw(decade, outname_nc)

