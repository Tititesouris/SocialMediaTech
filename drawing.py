

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


#46.227638	2.213749 france



m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='l',lat_0=55., lon_0=10., lat_1=0, lat_2=-35)
#m.bluemarble()
m.drawcoastlines(linewidth=0.4)
m.drawcountries()
m.drawmapboundary(fill_color='aquamarine')
#m.fillcontinents(color='limegreen',lake_color='red')
#m.fillcontinents(color='0.8', lake_color=None)
m.drawlsmask(land_color="0.8", ocean_color="w", lsmask=None)

lat, lon = 46.227638, 2.213749
xpt,ypt = m(lon,lat)
arrow=u'$\u2b06$'
#2b07 je strelica dolje
m.plot(xpt, ypt, c="red", marker=arrow, ms=15, alpha=0.8)



plt.show()
plt.cla()
plt.clf()
plt.close()

    # crtanje tocaka na karti
#m.plot(5, 10, c="crimson", marker='o', ms=5, alpha=0.8)
    






#SJEVERNA AMERIKA
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

plt.show()
plt.cla()
plt.clf()
plt.close()
