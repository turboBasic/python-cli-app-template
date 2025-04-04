"""
Geographical data module.
"""

from dataclasses import dataclass

import geopandas
from cartopy.io import shapereader


@dataclass(frozen=True)
class MapBounds:
    low_lat: float
    high_lat: float
    low_lon: float
    high_lon: float


class Country:
    __RESOLUTION = '10m'
    __NE_CULTURAL = 'cultural'
    __NE_COUNTRIES = 'admin_0_countries'
    __NE_PROVINCES = 'admin_1_states_provinces'

    def __init__(self, name: str, map_bounds: MapBounds | None = None):
        self.name = name
        self.__map_bounds = map_bounds
        self.__borders = None
        self.__admin_borders = None
        self.__world = None

    @property
    def resolution(self):
        return self.__RESOLUTION

    @property
    def admin_borders(self) -> geopandas.GeoSeries | None:
        """Get administrative division borders of the country."""
        if self.__admin_borders is None:
            df = geopandas.read_file(
                shapereader.natural_earth(self.resolution, self.__NE_CULTURAL, self.__NE_PROVINCES)
            )
            self.__admin_borders = df.loc[df['admin'] == self.name]['geometry'].values
        return self.__admin_borders

    @property
    def borders(self) -> geopandas.GeoDataFrame:
        """Get border of country."""
        if self.__borders is None:
            self.__borders = self._world().loc[self._world()['ADMIN'] == self.name]['geometry'].values
        return self.__borders

    @property
    def bounds(self) -> MapBounds:
        """Get the low and high latitude and longitude values for a given country."""
        low_lon, low_lat, high_lon, high_lat = self.borders[0].bounds
        return MapBounds(low_lat=low_lat, high_lat=high_lat, low_lon=low_lon, high_lon=high_lon)

    @property
    def map_bounds(self) -> MapBounds:
        """Get the low and high latitude and longitude bounds of the country map."""
        if self.__map_bounds is None:
            self.__map_bounds = MapBounds(
                low_lat=self.bounds.low_lat - 0.5,
                high_lat=self.bounds.high_lat + 0.5,
                low_lon=self.bounds.low_lon - 0.5,
                high_lon=self.bounds.high_lon + 0.5,
            )
        return self.__map_bounds

    def _world(self) -> geopandas.GeoDataFrame:
        """Read World shapefile."""
        if self.__world is None:
            self.__world = geopandas.read_file(
                shapereader.natural_earth(self.__RESOLUTION, self.__NE_CULTURAL, self.__NE_COUNTRIES)
            )
        return self.__world
