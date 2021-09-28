import numpy as np
from astropy.cosmology import WMAP9 as cosmo
from astropy.modeling import models
from astropy import units as u
from astropy import constants as const


class Source:

    def __init__(self, time_evolution=lambda t: 1.):
        self.time_evolution = time_evolution

    def luminosity(self, wl_aa, t_days):
        return self.peak_luminosity(wl_aa) * self.time_evolution(t_days)

    def peak_luminosity(self, wl_aa):
        raise NotImplementedError

    @staticmethod
    def lum_to_flux(lum, z):
        dl = cosmo.luminosity_distance(z=z).to(u.cm)
        return lum/(4. * np.pi * dl**2.)

    @staticmethod
    def lum_to_abs_mag(l_nu):
        flux = l_nu / (4. * np.pi * (10. * u.pc)**2.)
        abs_mag = flux.to(u.ABmag)
        return abs_mag

    def peak_flux(self, wl_aa, z):
        return (1.+z) * self.lum_to_flux(self.peak_luminosity(wl_aa/(1.+z)), z)

    @staticmethod
    def lambda_to_nu(wl_aa):
        return (wl_aa * u.AA)**2./const.c

    def peak_flux_nu(self, wl_aa, z):
        return self.peak_flux(wl_aa, z) * self.lambda_to_nu(wl_aa/(1.+z))

    def peak_luminosity_nu(self, wl_aa):
        return self.peak_luminosity(wl_aa) * self.lambda_to_nu(wl_aa)


class EmptySource(Source):

    def peak_luminosity(self, wl_aa):
        return wl_aa * 0.


class BlackBody(Source):

    def __init__(self, t_k, r_cm, *args):
        Source.__init__(self, *args)
        self.temp_k = t_k * u.K
        self.r_cm = r_cm * u.cm

    def peak_intensity(self, wl_ang):

        i = (
                (
                        (2. * const.h * const.c**2.)/(wl_ang * u.AA)**5.) * (
                        1. / (np.exp((const.h * const.c)/(const.k_B * self.temp_k * (wl_ang * u.AA))) - 1.))
        ).to("W m-2 AA-1") * np.pi

        # extra pi factor comes from integrating over solid angle

        return i

    def peak_luminosity(self, wl_ang):

        i = self.peak_intensity(wl_ang)

        llt = i * (4 * np.pi * self.r_cm**2.)

        return llt.to("W AA-1")


class PowerLaw(Source):

    def __init__(self, index, norm, ref_wl_ang, *args):
        Source.__init__(self, *args)
        self.index = index
        self.norm = norm
        self.ref_wl = ref_wl_ang

    def peak_luminosity(self, wl_ang):
        return self.norm * (wl_ang / self.ref_wl) ** self.index




