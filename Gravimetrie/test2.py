import matplotlib.pyplot as plt
import numpy
from scipy.interpolate import griddata
import scipy.interpolate as interp

x = numpy.array([0, 4, 3, 0])
y = numpy.array([0, 0, 3, 4])
z = numpy.array([1, 2, 3, 4])

# target grid to interpolate to
xi = numpy.arange(0, 4.05, 0.05)
yi = numpy.arange(0, 4.05, 0.05)
xi, yi = numpy.meshgrid(xi, yi)

# interpolate
zi = griddata((x, y), z, (xi, yi), method='linear')

yy, xx = numpy.meshgrid(y,x)
sparse_points = numpy.stack([x.ravel(), y.ravel()], -1)
zz = interp.RBFInterpolator(sparse_points, z.ravel(), smoothing=0, kernel='cubic')  # explicit default smoothing=0 for interpolation

# plot
fig = plt.figure()
ax = fig.add_subplot(111)
plt.contourf(xi,yi,zi)
plt.plot(x, y, 'k.')
plt.xlabel('xi', fontsize=16)
plt.ylabel('yi', fontsize=16)
# plt.savefig('interpolated.png',dpi=100)
plt.show()
plt.close(fig)