import geopandas
import pandas as pd
import matplotlib.pyplot as plt


def convert_value(value):
    """1800S -> -180"""

    if value.endswith("N") or value.endswith("E"):

        return int(value[:-1]) / 100.

    if value.endswith("S") or value.endswith("W"):

        return -int(value[:-1]) / 100.


def get_ports_coordinates():
    dfg = pd.read_csv("Downloads/code-list_csv.csv")
    #dfg = pd.read_csv("code-list_csv.csv")
    dfg = dfg.dropna(subset=["Coordinates"])

    df = pd.DataFrame()
    df["UNLocode"] = dfg["Country"] + dfg["Location"]

    dfk = pd.DataFrame(
        dfg["Coordinates"].dropna().str.split(" ").to_list(), columns=["lon", "lan"]
    )
    x = dfk["lon"].apply(convert_value)
    y = dfk["lan"].apply(convert_value)

    dfg = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(x=y, y=x))

    return dfg

def plot_ports(list_of_ports):
    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
    dfg = get_ports()
    dfg = dfg[dfg['UNLocode'].isin(list_of_ports)]
    ax = dfg.plot(color='k', marker='o', zorder=2)
    world.plot(ax=ax, zorder=1)
    plt.show()
