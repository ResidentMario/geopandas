"""
Plotting with Geoplot and GeoPandas
-----------------------------------

`Geoplot <https://residentmario.github.io/geoplot/index.html>`_ is a Python
library providing a selection of easy-to-use geospatial visualizations. It is
built on top of the lower-level `CartoPy <http://scitools.org.uk/cartopy/>`_,
covered in a separate section of this tutorial, and is designed to work with
GeoPandas input.

This example is a brief tour of the `geoplot` API. For more details on the
library refer to `its documentation
<https://residentmario.github.io/geoplot/index.html>`_.

First we'll load in the data using GeoPandas.
"""
import geopandas as gpd
import geoplot as gplt

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
boroughs = gpd.read_file(gplt.datasets.get_path('nyc_boroughs'))
collisions = gpd.read_file(gplt.datasets.get_path('nyc_injurious_collisions'))

###############################################################################
# Plotting with Geoplot
# =====================
#
# We start out by replicating the basic GeoPandas world plot using Geoplot.
gplt.polyplot(world, figsize=(8, 4))

###############################################################################
# Geoplot can re-project data into any of the map projections provided by
# CartoPy (see the list
# `here <http://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_).

import geoplot.crs as gcrs
ax = gplt.polyplot(world, projection=gcrs.Orthographic(), figsize=(8, 4))
ax.outline_patch.set_visible(True)

###############################################################################
# ``polyplot`` is trivial and can only plot the geometries you pass to it. If
# you want to use color as a visual variable, specify a ``choropleth``. Here
# we sort GDP per person by country into five buckets by color.

gplt.choropleth(
    world, hue=world['gdp_md_est'] / world['pop_est'],
    cmap='Greens', figsize=(8, 4)
)

###############################################################################
# If you want to use size as a visual variable, use a ``cartogram``. Here are
# population estimates for countries in Africa.

africa = world.query('continent == "Africa"')
ax = gplt.cartogram(
    africa, scale='pop_est', limits=(0.2, 1),
    edgecolor='None', figsize=(7, 8)
)
gplt.polyplot(africa, edgecolor='gray', ax=ax)

###############################################################################
# If we have data in the shape of points in space, we may generate a
# three-dimensional heatmap on it using ``kdeplot``.

ax = gplt.kdeplot(
    collisions, clip=boroughs.geometry,
    shade=True, cmap='Reds',
    projection=gcrs.AlbersEqualArea())
gplt.polyplot(boroughs, ax=ax, zorder=1)

###############################################################################
# Alternatively, we may partition the space into neighborhoods automatically,
# using Voronoi tessellation. This is a good way of visually verifying whether
# or not a certain data column is spatially correlated.

ax = gplt.voronoi(
    collisions.head(1000), projection=gcrs.AlbersEqualArea(),
    clip=boroughs.simplify(0.001),
    hue='NUMBER OF PERSONS INJURED', cmap='Reds', k=None,
    legend=True,
    edgecolor='white'
)
gplt.polyplot(boroughs, edgecolor='black', zorder=1, ax=ax)

###############################################################################
# These are just some of the plots you can make with Geoplot. There are
# many other possibilities not covered in this brief introduction. For more
# examples, refer to the
# `Gallery <https://residentmario.github.io/geoplot/gallery.html>`_ in the
# Geoplot documentation.
