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
    #dfg = pd.read_csv("Downloads/code-list_csv.csv")
    dfg = pd.read_csv("data/code-list_csv.csv")
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

def ports_to_x_dx(list_of_ports):
    dfg = get_ports_coordinates()
    dfg = dfg[dfg['UNLocode'].isin(list_of_ports)]
   
    list_ = []
    for i, port_origin in enumerate(list_of_ports[:-1]):
        port_origin_xy = dfg.query("UNLocode == @port_origin").iloc[0].geometry
        x, y = port_origin_xy.x, port_origin_xy.y 
        
        port_dest = list_of_ports[i + 1]
        port_dest_xy = dfg.query("UNLocode == @port_dest").iloc[0].geometry
        dx, dy = port_dest_xy.x - x, port_dest_xy.y - y
        list_.append((x, y, dx, dy))
    return list_

a = ports_to_x_dx(["NLRTM", "CNXMG", "CNNBG"])
