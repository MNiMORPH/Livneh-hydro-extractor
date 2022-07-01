from matplotlib import pyplot as plt
import pandas as pd

pet = pd.read_csv('/home/awickert/Dropbox/CannonLivneh_Date_P_ET.csv')
pet['Date'] = pet['Date'].astype('datetime64[ns]') 

plt.figure(figsize=(17,5))
plt.plot(pet['Date'], pet['Precipitation [mm/day]'], 'b-')
plt.plot(pet['Date'], pet['Evapotranspiration [mm/day]'], 'r-')
plt.legend(loc='upper left')
plt.xlabel('Date', fontsize=18)
plt.ylim(0, plt.ylim()[-1])
plt.tight_layout()

plt.savefig('/home/awickert/Dropbox/CannonLivneh_plt.png')

