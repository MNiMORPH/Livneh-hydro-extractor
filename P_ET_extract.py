#! /usr/bin/python2

import glob
import numpy as np
from matplotlib import pyplot as plt
import netCDF4 as nc4
import datetime

def get_YearMonth(fname):
    YYYYMM = fname.split('.')[-2]
    YYYY = int(YYYYMM[:4])
    MM = int(YYYYMM[4:])
    return YYYY, MM


def date_prec_et(decade_yyyy, outname_nc):

    ncfiles = sorted(glob.glob('VIC_fluxes_Livneh_CONUSExt_v.1.2_2013.'
                                + ('%04d' %decade_yyyy)[:3] + '*.nc'))

    date_list_object = []
    date_list = []
    prec_list = []
    ET_list = []
    
    time_units = "days since 1900-01-01"

    for ncfile in ncfiles:
        print ncfile
        yyyy, mm = get_YearMonth(ncfile)
        fluxes = nc4.Dataset(ncfile)
        for i in range(len(fluxes.variables['time'])):
            dd = int(np.round(fluxes.variables['time'][i]/86400)) + 1
            date = datetime.datetime(yyyy, mm, dd)
            prec = fluxes.variables['Prec'][i].data
            prec[prec > 1E19] = np.nan
            ET = fluxes.variables['ET'][i].data
            ET[ET > 1E19] = np.nan
            print date
            date_list_object.append(date)
            #date_list.append(date.isoformat())
            date_list.append( nc4.date2num(date, time_units) )
            prec_list.append(prec)
            ET_list.append(ET)

    prec_list = np.array(prec_list)
    ET_list = np.array(ET_list)

    outnc = nc4.Dataset(outname_nc, 'w', format='NETCDF4')

    outnc.createDimension('lon', len(fluxes['lon']))
    outnc.createDimension('lat', len(fluxes['lat']))
    outnc.createDimension('time', len(date_list))

    _lon = outnc.createVariable('lon', 'f4', fluxes['lon'].dimensions)
    _lat = outnc.createVariable('lat', 'f4', fluxes['lat'].dimensions)
    _time = outnc.createVariable('time', 'i4', fluxes['time'].dimensions)
    _prec = outnc.createVariable('prec', 'f4', fluxes['Prec'].dimensions)
    _et = outnc.createVariable('et', 'f4', fluxes['ET'].dimensions)
    
    _time.units = time_units

    _lon[:] = fluxes['lon']
    _lat[:] = fluxes['lat']
    _time[:] = date_list
    _prec[:] = prec_list
    _et[:] = ET_list
    
    outnc.close()
    
decade_list = [1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]

for decade in decade_list:
    outname_nc = '/media/awickert/data1/Decadal_P_ET_LivnehCONUS/' \
                  + 'LivnehCONUS_P_ET_' + str(decade) + 's.nc'
    date_prec_et(decade, outname_nc)

