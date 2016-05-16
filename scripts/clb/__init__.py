# -*- coding: utf-8 -*-
"""This package provides modules and functions to estimate the cloud base level
by measuring the downward longwave radiation.
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.constants


__all__ = ['create_dummy_data',
           'lwr_to_temperature',
           'lapse_rate',
           'standard_atmosphere',
           ]


def create_dummy_data(LWR=350, N=500, noise=False):
    """Create a dumm array representing LWR data."""
    lwr = LWR * np.ones(N)

    if noise:
        lwr += np.random.randn(N)

    return lwr


def lwr_to_temperature(lwr):
    """Transform LWR radiances into brightness temperatures.

    Parameters:
        lwr (np.array): Measured LWR radiances.

    Returns:
        np.array: Brightness temperature in Kelvin."""
    return (lwr / sp.constants.Stefan_Boltzmann)**0.25


def lapse_rate(T_s, z, lapse_rate=-0.0065):
    """Generate a time series of temperature profiles.

    This functions takes a time series of surface temperatures and returns an
    first order temperature profile for each time step. For this purpose a
    temperature lapse rate as well as height levels have to be specified.

    Parameters:
        T_s (np.array): Surface temperatures.
        z (np.array): Height levels.
        lapse_rate (float): Lapse rate.

    Returns:
        np.array: Atmospheric temperature profile (T_s x z).

    """
    tt, zz = np.meshgrid(T_s, z)
    return tt + lapse_rate * zz


def standard_atmosphere(z=np.linspace(0, 86000, 100), T_s=19., unit='K'):
    """International standard atmosphere temperature at given heights.

    Parameters:
        z (np.array): Array of level heights in m.
        T_s (float): Surface temperature.
        unit (str): Temperature unit 'K' (default) or 'C'.

    Returns:
        np.array: Temperatures at given height levels.

    """

    # https://en.wikipedia.org/wiki/International_Standard_Atmosphere
    T = -86.28 * np.ones(z.size)
    T[z < 86000] = -58.5 - 0.0020 * (z[z < 86000] - z[z <= 71802].max())
    T[z < 71802] = -02.5 - 0.0028 * (z[z < 71802] - z[z <= 51413].max())
    T[z < 51413] = -02.5
    T[z < 47350] = -44.5 + 0.0028 * (z[z < 47350] - z[z <= 32162].max())
    T[z < 32162] = -56.5 + 0.0010 * (z[z < 32162] - z[z <= 20063].max())
    T[z < 20063] = -56.5
    T[z < 11019] = 19.00 - 0.0065 * z[z < 11019]

    # adjust surface temperature
    T = T + (T_s - 19.)

    if unit == 'K':
        T += 273.15
    elif unit != 'C':
        raise Exception("Unknown unit. Allowd units are 'K' and 'C'.")

    return T