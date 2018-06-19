import json


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


count_austria, count_uk, count_us, count_france, count_croatia = 0, 0, 0, 0, 0
rate_austria, rate_uk, rate_us, rate_france, rate_croatia = 0, 0, 0, 0, 0

load = json.load(open("visualisations/data.json", "r"))
test = load["counts"]["austria"]["uk"]
print test

    
#IDK WHAT TO DO
counts = []
count_austria = int(load["counts"]["austria"]["austria"])
count_uk = int(load["counts"]["uk"]["uk"])
count_usa = int(load["counts"]["usa"]["usa"])
count_france = int(load["counts"]["france"]["france"])
count_croatia = int(load["counts"]["croatia"]["croatia"])
    
score_austria = float(load["self_image"]["austria"]["score"])
score_uk = float(load["self_image"]["uk"]["score"])
score_usa = float(load["self_image"]["usa"]["score"])    
score_france = float(load["self_image"]["france"]["score"])   
score_croatia = float(load["self_image"]["croatia"]["score"])

    
    
    
    
    
m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='l',lat_0=55., lon_0=10., lat_1=0, lat_2=-35)

m.drawcoastlines(linewidth=0.4)
m.drawcountries()
m.drawmapboundary(fill_color='aquamarine')
m.drawlsmask(land_color="0.8", ocean_color="w", lsmask=None)

color = [0, 1*score_france, 0]
arrow=u'$\u2b06$'
#2b07 je arrow down

#AUSTRIA
lat, lon = 47.516231, 14.550072
xpt,ypt = m(lon,lat)
m.plot(xpt, ypt, c= [0, score_austria/count_austria*3, 0], marker='o', ms= 10 * count_austria/10, alpha=0.8)

#UK
lat, lon = 55.378051, -3.435973
xpt,ypt = m(lon,lat)
m.plot(xpt, ypt, c=[0, score_uk/count_uk*3, 0], marker='o', ms= 10 * count_uk/200, alpha=0.8)

#FRANCE
lat, lon = 46.227638, 2.213749
xpt,ypt = m(lon,lat)
m.plot(xpt, ypt, c=[0, score_france/count_france*3, 0], marker='o', ms= 10 * count_france/200, alpha=0.8)

#CROATIA
lat, lon = 45.1, 15.2
xpt,ypt = m(lon,lat)
m.plot(xpt, ypt, c=[0, score_croatia/count_croatia*3, 0], marker='o', ms= 10 * score_croatia/3, alpha=0.8)







plt.show()
plt.cla()
plt.clf()
plt.close()



#AMERICA
# setup Lambert Conformal basemap.
n = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
# draw coastlines.
n.drawcoastlines(linewidth=0.4)
n.drawcountries()

# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
n.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
#m.fillcontinents(color='coral',lake_color='aqua')
n.drawlsmask(land_color="0.8", ocean_color="w", lsmask=None)

#USA
#for some reason it doesnt work and im pretty sure coordinates are right
lat, lon = -104.237, 40.125 
xpt,ypt = n(lon,lat)
n.plot(xpt, ypt, c=[0, score_usa/count_usa, 0], marker='o', ms=count_usa*100, alpha=0.8)

plt.show()
plt.cla()
plt.clf()
plt.close()
