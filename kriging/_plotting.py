# encoding: utf-8

"""
Add the map path according to mapData
"""

from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

def plot_map(mapdata,ax=None):
    """
    Add the map path according to mapData

    Parameters
    ----------
    mapdata: array of map data.
    """
    if ax is None:
        _, ax = plt.subplots()
    for shap in mapdata:
        ax.add_patch(PathPatch(Path(shap),facecolor='None',edgecolor='k'))
    ax.autoscale_view()
