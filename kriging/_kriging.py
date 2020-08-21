# encoding: utf-8

"""
Ordinary Kriging interpolation is a linear estimation of regionalized variables.
It assumes that the data change into a normal distribution,
and considers that the expected value of regionalized variable Z is unknown.
The interpolation process is similar to the weighted sliding average,
and the weight value is determined by spatial data analysis.
"""

import numpy as np
from shapely.geometry import Polygon,Point,shape
from shapely.geometry.multipolygon import MultiPolygon
from shapely.prepared import prep

class Kriging():
    """Ordinary Kriging interpolation class"""
    def _distance(self,xy1,xy2):
        xdmat = (xy1[:,[0]] - xy2[:,0])**2
        ydmat = (xy1[:,[1]] - xy2[:,1])**2
        return np.sqrt(xdmat + ydmat)
    def _rh(self,z):
        return 1/2 * (z - z.reshape(-1,1))**2
    def _proportional(self,x,y):
        """ x*y / x**2 """     
        return (x*y).sum()/(x ** 2).sum()
    def fit(self,xy=None,z=None):
        """
        The training process mainly includes half variance and distance matrix calculation.
        """
        self.xy = xy.copy()
        self.z = z.copy()
        h = self._distance(xy,xy)
        r = self._rh(z)
        hh_f = np.triu(h+1,0)
        rr_f = np.triu(r+1,0)
        hh=np.triu(h,0)
        rr=np.triu(r,0)
        self.k = self._proportional(hh[(hh!=0) | (hh_f!=0)],rr[(rr!=0) | (rr_f!=0)])
        self.hnew=h*self.k
        self.hnew = np.r_[self.hnew,np.ones((1,self.hnew.shape[1]))]
        self.hnew = np.c_[self.hnew,np.ones((self.hnew.shape[0],1))]
        self.hnew[self.hnew.shape[0]-1,self.hnew.shape[1]-1] = 0
    def predict(self,xy):
        """
        The interpolating weights are calculated and the interpolating results are obtained.
        """
        oh = self._distance(self.xy,xy)
        oh = self.k * oh
        oh = np.r_[oh,np.ones((1,oh.shape[1]))]
        self.w = np.dot(np.linalg.inv(self.hnew),oh)
        res = (self.z.reshape(-1,1) * self.w[:-1,:]).sum(0)
        return res

def shape_shadow(xgrid,ygrid,mapdata):
    """
    Mask processing.

    Parameters
    ----------
    xgrid: grid coordinates of longitude.
    ygrid: grid coordinates of latitude.
    mapdata: array of map data.

    Return
    ------
    np.ndarray: An array of Boolean types.
    
    """
    newshp = Polygon()
    for shap in mapdata:
        newshp = newshp.union(shape({'type':'Polygon','coordinates':[shap]}))
    points = []
    for xi,yi in zip(xgrid.ravel(),ygrid.ravel()):
        points.append(Point([xi,yi]))
    prep_newshp = prep(newshp)
    mask = []
    for p in points:
        mask.append(bool(prep_newshp.contains(p)-1))
    mask = np.array(mask).reshape(xgrid.shape)
    return mask

def interpolate(xy,z,extension=1.2,point_counts=(100,100)):
    """
    Interpolate through the Kriging class, and return the grid points
    of the longitude and latitude interpolation results

    Parameters
    ----------
    xy: The latitude and longitude coordinates of a spatial data point.
    z: The latitude and longitude coordinates of a spatial data point.
    extension: The interpolating region is expanded to cover a wider area.
    point_counts: How many data points to interpolate, default is 100 * 100.
    
    """
    kri = Kriging()
    kri.fit(xy,z)
    x_max,x_min,y_max,y_min = xy[:,0].max(),xy[:,0].min(),xy[:,1].max(),xy[:,1].min()
    p = (extension - 1.0)/2
    x_s = x_min - (x_max-x_min)*p
    x_e = x_max + (x_max-x_min)*p
    y_s = y_min - (y_max-y_min)*p
    y_e = y_max + (y_max-y_min)*p
    xls = np.linspace(x_s,x_e,point_counts[0])
    yls = np.linspace(y_s,y_e,point_counts[1])
    xgrid,ygrid = np.meshgrid(xls,yls)
    xgridls,ygridls = xgrid.ravel(),ygrid.ravel()
    if len(xgridls) > 100000: # Consider memory limit loop handling.
        zgridls = np.array([])
        for s,e in zip(np.arange(0,len(xgridls),100000)[:-1],np.arange(0,len(xgridls),100000)[1:]):
            zgridls = np.concatenate([zgridls,kri.predict(np.c_[xgridls[s:e],ygridls[s:e]])])
        if e < len(xgridls):
            zgridls = np.concatenate([zgridls,kri.predict(np.c_[xgridls[e:],ygridls[e:]])])
    else:
        zgridls = kri.predict(np.c_[xgridls,ygridls])
    zgrid = zgridls.reshape(xgrid.shape)
    return xgrid,ygrid,zgrid




    
