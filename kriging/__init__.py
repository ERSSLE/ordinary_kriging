# encoding: utf-8
"""
Ordinary Kriging interpolation is a linear estimation of regionalized variables.
It assumes that the data change into a normal distribution,
and considers that the expected value of regionalized variable Z is unknown.
The interpolation process is similar to the weighted sliding average,
and the weight value is determined by spatial data analysis.
"""

from ._kriging import interpolate,shape_shadow,Kriging
from ._plotting import plot_map
from .base import load_mapdata

