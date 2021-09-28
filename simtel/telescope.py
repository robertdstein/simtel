import pandas as pd
import os
import numpy as np
from pathlib import Path
import scipy
from scipy.interpolate import interp1d

base_dir = Path(__file__).parents[0]


class Filter:

    def __init__(self, filter_name, bandpass_file):

        self.name = filter_name
        self.bandpass = self.load_bandpass(bandpass_file)
        self.t_f = interp1d(self.bandpass["wavelength"], self.bandpass["transmission"])
        self.mean_wl = np.average(self.bandpass["wavelength"], weights=self.bandpass["transmission"])

    def integrate_flux(self, flux_f):

        def f(wl):
            return flux_f(wl) * self.t_f(wl)

        print(self.bandpass["wavelength"])

        print(self.bandpass["wavelength"].loc[1],self.bandpass["wavelength"].loc[-1])

        i = self.bandpass["transmission"]*flux_f(self.bandpass["wavelength"])/np.sum(self.bandpass["transmission"])
        i2 = scipy.integrate.quad(f, self.bandpass["wavelength"].loc[0], self.bandpass["wavelength"].loc[-1])

    @staticmethod
    def load_bandpass(bandpass_file):
        path = os.path.join(base_dir, f'tel_data/{bandpass_file}')

        if path[-4:] == ".csv":
            return pd.read_csv(path)
        else:
            return pd.read_table(path, columns=["wavelength", "transmission"])


class Telescope:

    def __init__(self, tel_name, *args):

        self.tel_name = tel_name
        self.filters = {}

        for (filter_name, bandpass) in args:
            self.add_filter(filter_name, bandpass)

    def add_filter(self, filter_name, bandpass):
        self.filters[filter_name] = Filter(filter_name, bandpass)


telescopes = {
    "Swift": Telescope(
        "Swift",
        ("W2", "swift_W2.csv"),
        ("M2", "swift_M2.csv"),
        ("W1", "swift_W1.csv"),
        ("U", "swift_U.csv"),
        ("white", "swift_white.csv"),
        ("B", "swift_B.csv"),
        ("V", "swift_V.csv"),
    ),
    "ZTF": Telescope(
        "ZTF",
        ("g", "g.csv"),
        ("r", "r.csv"),
        ("i", "i.csv")
    ),
    "WISE": Telescope(
            "WISE",
            ("W1", "wise_W1.csv"),
            ("W2", "wise_W2.csv"),
        ),
}
