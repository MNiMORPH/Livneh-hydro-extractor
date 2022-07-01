from osgeo import gdal
import numpy as np
import netCDF4 as nc4
import glob
import datetime
import pandas as pd

filepath = '/media/awickert/data1/Cannon_P_ET_Livneh/Cannon_Livneh_mask/Cannon_Livneh_mask.tif'
outpath = '/home/awickert/Dropbox/CannonLivneh_Date_P_ET.csv'

cannonBinary = gdal.Open(filepath)

mask = cannonBinary.GetRasterBand(1).ReadAsArray()[::-1]

precCannon = []
etCannon = []
dateCannon = []

time_units = "days since 1900-01-01"

ncfilenames = sorted(glob.glob('/media/awickert/data1/Decadal_P_ET_LivnehCONUS/*.nc'))

# NOT CURRENTLY ACCOUNTING FOR DIFFERING AREA ACROSS WATERSHED
# LESS IMPORTANT IN SMALL WATERSHED
for ncfilename in ncfilenames:
    ncfile = nc4.Dataset(ncfilename)
    for i in range(len(ncfile['time'])):
        # mm/s to mm/day [ = mm, with daily time steps ]\
        # Prec looks like it was in m/s, actually: to mm/day
        _date = nc4.num2date(ncfile['time'][i], time_units)
        print _date
        dateCannon.append(_date)
        precCannon.append(np.nanmean(ncfile['prec'][i] * mask) * 86400000)
        etCannon.append(np.nanmean(ncfile['et'][i] * mask) * 86400000)

#precCannon = np.array(precCannon)
#etCannon = np.array(etCannon)

outData = pd.DataFrame()
outData['Date'] = dateCannon
outData['Precipitation [mm/day]'] = precCannon
outData['Evapotranspiration [mm/day]'] = etCannon

outData.to_csv(outpath, index=False)
