#--import relevant libraries
#import matplotlib.pyplot as plt 
#from netCDF4 import Dataset
#import cartopy.crs as ccrs

#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import xarray as xr
import pandas as pd
import numpy as np


#--define lat and lon range
#Oyo, Osun, Ondo, Ogun, Ekiti and Lagos States
Oyo = [3.0, 4.20, 7.50, 8.40] #--[minlon, maxlon, minlat, maxlat]
Osun = [4.0, 5.0, 7.8, 8.2]
Ondo = [4.6, 5.0, 6.3, 7.2]
Ogun = [3.0, 4.2, 6.0, 7.1]

area = ['Oyo', 'Osun', 'Ondo', 'Ogun']
coords = [Oyo, Osun, Ondo, Ogun]
year = np.arange(2006,2020,1)

#print(year)

for i,area in enumerate(area):
    print('Processing '+area+' data...')
    #print(coords[i])
    #print(coords[i][0])
    #print(type(coords[i]))
    #print(type(coords[i][0]))
    
    for yr in year:
        print('Extracting data for '+str(yr))
        #dataDIR = '/Users/gbode/tutorial4python/era5/ERA5SfcTRh_'+str(yr)+'.nc'
        
        
        #--load netCDF data with xarray
        #--read netcdf with xArray
        #--load surface data min and max temperature, mean Temp, precipitation
        dataDIR = '/Users/gbode/tutorial4python/era5/ERA5SfcTRh_'+str(yr)+'.nc'
        DS = xr.open_dataset(dataDIR)
        #print(DS)

        #--load dew point temperature
        dataDIRi = "/Users/gbode/tutorial4python/era5/ERA5SfcTd_"+str(yr)+".nc"
        DSi = xr.open_dataset(dataDIRi)

        print("====1===")
        #--read in CHIRPS data 
        #--load chirps precipitation
        dataDIR2 = "/Users/gbode/Documents/COLLAB_WORK/extremePaper/data/v2p0chirps_25.nc"
        DS2 = xr.open_dataset(dataDIR2)
        #print(DS2)
        #--read in lon and lat coordinates
        long2 = DS2.coords["lon"]
        lati2 = DS2.coords["lat"]
        time2 = DS2.coords["time"]
        chirps_pr = DS2["pr"].sel(time=slice(str(yr)+"-01-01", str(yr)+"-12-31"))
        #print(chirps_pr.shape)

        print("====2===")
        # OR multiple files
        #mfdataDIR = '../self_study/data/l*_sst.nc'
        #DS = xr.open_mfdataset(mfdataDIR)

        #--read in lon and lat coordinates
        # modify a 2D region using loc()
        long = DS.coords["longitude"]
        lati = DS.coords["latitude"]
        #timei = DS.coords["time"]
        time = DS.coords["time"].resample(time='D').mean()
        #tim_val = time.dt.strftime('%Y-%m-%d') #('%Y-%b-%d %H:%M')
        Year = time.dt.strftime('%Y').values
        month = time.dt.strftime('%m').values
        day = time.dt.strftime('%d').values

        #long2 = DS.coords["longitude"].loc[dict(longitude=long[(long >= 2) & (long <= 15)])]
        #lati2 = DS.coords["latitude"].loc[dict(latitude=lati[(lati >= 2) & (lati <= 15)])]

        #--dewpoint temperature
        d2m = DSi["d2m"].resample(time='D').mean()
        np_d2m = np.nanmean(np.nanmean(d2m.loc[dict(longitude=long[(long >= coords[i][0]) & (long <= coords[i][1])], 
                                    latitude=lati[(lati >= coords[i][2]) & (lati <= coords[i][3])])].values, axis=1), axis=1) -273.15
                                                                        #--convert Kelvin to degree Celcius
        #--temperature at 2 meters
        t2m = DS["t2m"].resample(time='D').mean()
        np_t2m = np.nanmean(np.nanmean(t2m.loc[dict(longitude=long[(long >= coords[i][0]) & (long <= coords[i][1])], 
                                    latitude=lati[(lati >= coords[i][2]) & (lati <= coords[i][3])])].values, axis=1), axis=1) -273.15
                                 #--convert Kelvin to degree Celcius

        #--maximum temperature at 2 meters
        mx2t = DS["mx2t"].resample(time='D').mean()
        np_mx2t = np.nanmean(np.nanmean(mx2t.loc[dict(longitude=long[(long >= coords[i][0]) & (long <= coords[i][1])], 
                                    latitude=lati[(lati >= coords[i][2]) & (lati <= coords[i][3])])].values, axis=1), axis=1) -273.15
                                                                        #--convert Kelvin to degree Celcius
        #--minimum temperature at 2 meters
        mn2t = DS["mn2t"].resample(time='D').mean()
        np_mn2t = np.nanmean(np.nanmean(mn2t.loc[dict(longitude=long[(long >= coords[i][0]) & (long <= coords[i][1])], 
                                    latitude=lati[(lati >= coords[i][2]) & (lati <= coords[i][3])])].values, axis=1), axis=1) -273.15
                                        #--convert Kelvin to degree Celcius

        print("====3===")
        #--relative humidty at 1000hPa
        #rh = DSrh["r"].resample(time='D').mean()
        #Oyo_rh = np.mean(np.mean(rh.loc[dict(longitude=long3[(long3 >= Oyo[0]) & (long3 <= Oyo[1])], 
        #                            latitude=lati3[(lati3 >= Oyo[2]) & (lati3 <= Oyo[3])])].values, axis=1), axis=1) 
        #                                                                #--RH

        print("====4===")
        #--ERA5 precipitation
        tp = DS["tp"].resample(time='D').sum()
        np_tp = np.nanmean(np.nanmean(tp.loc[dict(longitude=long[(long >= coords[i][0]) & (long <= coords[i][1])], 
                                    latitude=lati[(lati >= coords[i][2]) & (lati <= coords[i][3])])].values, axis=1), axis=1) * 1000 
                                                                            #--convert meter to millimeters
        #--CHIRPS precipitation
        np_chirps = np.nanmean(np.nanmean(chirps_pr.loc[dict(lon=long2[(long2 >= coords[i][0]) & (long2 <= coords[i][1])], 
                                    lat=lati2[(lati2 >= coords[i][2]) & (lati2 <= coords[i][3])])].values, axis=1), axis=1) 


        '''
        Compute Relative Humidity (Bolton 1980):
        es = 6.112*exp((17.67*T)/(T + 243.5));
        e = 6.112*exp((17.67*Td)/(Td + 243.5));
        RH = 100.0 * (e/es);
             where:
               es = saturation vapor pressure in mb; 
               e = vapor pressure in mb;
               RH = Relative Humidity in percent
               SD = saturation vapor pressure deficit 
        '''

        es =  6.112 * np.exp((17.67 * np_t2m) / (np_t2m + 243.5))
        e = 6.112 * np.exp(( 17.67 * np_d2m) / (np_d2m + 243.5))
        #--saturation deficit SD = es - e
        SD = es - e #--
        RH = 100.0 * (e/es)

        #print(df.shape)
        #df_pd = pd.DataFrame(np.array([Year, month, day, Oyo_t2m]), columns =['Year', 'month', 'day', 'Oyo_t2m'])
        #--header ==> Day Max Min Ave Precip SD RH
        #dfp = {'Year':Year, 'Month':month, 'day':day, 'Oyo_t2m [degC]':Oyo_t2m, 
        #       'Oyo_mx2t [degC]':Oyo_mx2t, 'Oyo_mn2t [degC]':Oyo_mn2t, 'Oyo_rh [%]':Oyo_rh,
        #       'Oyo_tp [mm]':Oyo_tp, 'Oyo_chirps [mm]':Oyo_chirps}

        dfp = {'Year':Year, 'Month':month, 'Day':day,  
               'MaxT':np_mx2t, 'MinT':np_mn2t, 'AveT':np_t2m,
               'Precip':np_chirps, 'SD':SD, 'RH':RH}

        df_pd = pd.DataFrame(data=dfp)
        df_pd.to_csv('/Users/gbode/Documents/COLLAB_WORK/OlugbengaDataExt/extractedData/'+area+'_'+str(yr)+'.csv', index=False)

