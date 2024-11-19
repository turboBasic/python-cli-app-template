"""
CLI for geo command
"""

import logging
from typing import Annotated

import cartopy.feature

# import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import typer

# from cartopy.io import shapereader
from python_cli_app_template import config
from python_cli_app_template.geo import Country

app = typer.Typer()


def setup_country_map(country: Country) -> mpl.pyplot.Axes:
    """Set up the map with the borders of Germany"""
    ax = plt.axes(projection=cartopy.crs.Mercator())
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':', edgecolor='0.33')
    ax.add_geometries(
        country.borders,
        cartopy.crs.PlateCarree(),
        facecolor='none',
        edgecolor='0.5',
    )

    # Add administrative division borders
    ax.add_geometries(
        country.admin_borders, cartopy.crs.PlateCarree(), facecolor='gray', edgecolor='0.3', linestyle='--', alpha=0.5
    )

    ax.coastlines(country.resolution, color='0.5')
    ax.set_extent(
        [
            country.map_bounds.low_lon,
            country.map_bounds.high_lon,
            country.map_bounds.low_lat,
            country.map_bounds.high_lat,
        ]
    )
    return ax


def geo_data() -> str:
    return config.geo_data('15_min')


@app.command()
def draw(country_name: Annotated[str, typer.Argument(..., help='Country')]) -> None:
    """Draw the map of the country."""
    logging.getLogger(__name__).info(f'geo/draw: country_name={country_name}')

    # Prepare map
    country = Country(country_name)
    setup_country_map(country)
    plt.title(country.name)
    plt.show()
    plt.close()


@app.command()
def population() -> None:
    """Display population data."""
    logging.getLogger(__name__).info('geo/population: Listing all countries')

    input_data = np.loadtxt(geo_data(), skiprows=6)
    input_data[input_data < 0] = 0
    typer.echo(input_data)


@app.callback()
def main(ctx: typer.Context):
    """Various Geomapping commands."""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.command.name}/{ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
