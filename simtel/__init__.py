from simtel.source import EmptySource, BlackBody, PowerLaw
from simtel.telescope import telescopes

class Comparison:

    def __init__(self, source, host=None, *args):

        self.source = source
        if host is not None:
            self.host = host
        else:
            self.host = EmptySource()

        self.bkg_model = lambda wl_nm, z, t: self.source.luminosity(wl_nm, z, t) + self.host.luminosity(wl_nm, z. t)

        self.tels = {}

        for tel in args:
            self.add_telescope(tel)

    def add_telescope(self, tel):
        self.tels[tel] = tel

    def calculate_snr(self, tel, f_name, z, t=0.):

        sig = self.tels[tel].filter[f_name].integrate_flux(self.source.luminosity, z, t)
        bkg = self.tels[tel].filter[f_name].integrate_flux(self.bkg_model, z, t)

        snr = sig/bkg

        return snr