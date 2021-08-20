import pandas as pd
import os
from pathlib import Path

base_dir = Path(__file__).parents[0]


def integrate(x, y):
    return x*y


class Filter:

    def __init__(self, filter_name, bandpass_file):

        self.name = filter_name
        self.bandpass = self.load_bandpass(bandpass_file)

    def integrate_flux(self, flux):
        return integrate(self.bandpass, flux)

    @staticmethod
    def load_bandpass(bandpass_file):
        path = os.path.join(base_dir, f'tel_data/{bandpass_file}')

        if path[-4:] == ".csv":
            return pd.read_csv(path)
        else:
            return pd.read_table(path)


class Telescope:

    def __init__(self, tel_name, *args):

        self.tel_name = tel_name
        self.filters = {}

        for (filter_name, bandpass) in args:
            self.add_filter(filter_name, bandpass)

    def add_filter(self, filter_name, bandpass):
        self.filters[filter_name] = Filter(filter_name, bandpass)


telescopes = {
    "ZTF": Telescope(
        "ZTF",
        ("g", "g.csv"),
        ("r", "r.csv"),
        ("i", "i.csv")
    ),
    "WISE": Telescope(
            "WISE",
            ("W1", "wise_w1.csv"),
            ("W2", "wise_w2.csv"),
        )
}