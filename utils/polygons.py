"""Exposes a function that returns the HTMP code for containing rectangles."""

import os
import pathlib
import uuid

from geopy.geocoders import Nominatim
from shapely.geometry import Point
import folium
import geopandas as gpd


def make_map(post_code):
    """Creates the HTML to display the conaining polygon for the post code.

    :param str post_code: The post code to lookup.

    :return: The HTML to display as a string.
    """
    global _polygons
    if not _polygons:
        _polygons = _Polygons()

    return _polygons._plot_polygon_for_postcode(post_code)


###############################################################################
#
# What follows is private stuff that is not meant to be used from the outside.
#
###############################################################################

# Aliases.
_HOME_DIR = pathlib.Path.home()
_GEO_DB = os.path.join(_HOME_DIR, "resources", "polygons.gpkg")


class _Polygons:
    """Keeps the multi-polygons database in memory."""

    def __init__(self, rows=None):
        """Initializer."""
        if rows is None:
            gdf = gpd.read_file(_GEO_DB)
        else:
            gdf = gpd.read_file(_GEO_DB, rows=rows)
        self.__gdf = gdf.to_crs(epsg=4326)

    def _get_containing_polygon(self, post_code):
        """Find the containing polygon for the passed in post_code.

        :param str post_code: The post code to lookup.

        :return: The containing polygon.
        :rtype: MultiPolygon

        :raises: ValueError is the post code is not found.
        """
        point = self._make_point_from_postcode(post_code)
        for index, row in self.__gdf.iterrows():
            polygon = row['geometry']
            if polygon.contains(point):
                return polygon
        raise ValueError

    def _plot_polygon_for_postcode(self, post_code, fill_color=None):
        """For the passed in post_code returns the HTML for the polygon.

        :param str post_code: The post code to lookup.

        :param str fill_color: The color to use to fill the area (optional).

        :returns: The HTML document for the containing polygon.
        """
        fill_color = fill_color or 'green'
        p = self._get_containing_polygon(post_code)
        centroid_longitude = p.centroid.x
        centroid_latitude = p.centroid.y

        m = folium.Map(
            location=[centroid_latitude, centroid_longitude], zoom_start=15
        )

        geojson_object = folium.GeoJson(
            p,
            style_function=lambda feature: {
                'fillColor': fill_color,
                'weight': 2
            }
        )

        geojson_object.add_to(m)
        filename = f"{str(uuid.uuid4())[:8]}.html"
        filepath = os.path.join(_HOME_DIR, "temp", filename)
        m.save(filepath)
        with open(filepath) as fin:
            return fin.read()

    @classmethod
    def _make_point_from_postcode(cls, postcode):
        """Retrieves the centroid for the passed in postcode.

        :param str post_code: The post code to lookup.

        :returns: Shapely.Point
        """
        geolocator = Nominatim(user_agent="junkapp")
        location = geolocator.geocode(postcode)
        if location:
            return Point(location.longitude, location.latitude)
        raise ValueError


_polygons = None

if __name__ == '__main__':
    # Self test..
    POST_CODE = "EC4N 8BH"
    print(make_map(POST_CODE))
