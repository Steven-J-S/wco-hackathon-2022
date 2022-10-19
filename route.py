import geopandas
import pandas as pd
import matplotlib.pyplot as plt

# functies Maarten
def convert_value(value):
    """1800S -> -180"""

    if value.endswith("N") or value.endswith("E"):

        return int(value[:-1]) / 100.0

    if value.endswith("S") or value.endswith("W"):

        return -int(value[:-1]) / 100.0


def get_ports_coordinates(refresh_file=False):
    if refresh_file:
        dfg = pd.read_csv("data/code-list_csv.csv")
        dfg = dfg.dropna(subset=["Coordinates"])

        df = pd.DataFrame()
        df["UNLocode"] = dfg["Country"] + dfg["Location"]
        df["Name"] = dfg["Name"].str.upper()

        dfk = pd.DataFrame(
            dfg["Coordinates"].dropna().str.split(" ").to_list(), columns=["lon", "lan"]
        )
        x = dfk["lon"].apply(convert_value)
        y = dfk["lan"].apply(convert_value)

        dfg = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(x=y, y=x))
        dfg.to_file('ports.shp')
    else:
        try:
            dfg = geopandas.read_file('ports.shp')
        except:
            print("NOT FOUND")
            dfg = get_ports_coordinates(True)
    return dfg


    
def get_ports(list_of_ports, unloc=True):
    """if unloc ["NLRTM", "CNXMG", "CNNBG"] 
                ["ROTTERDAM, SHANGHAI, LONDON"] """
    dfg = get_ports_coordinates()
    if unloc:
        dfg = dfg[dfg["UNLocode"].isin(list_of_ports)]
    else:
        dfg = dfg[dfg["Name"].isin(list_of_ports)]
    return dfg

def plot_ports(shipping_ports, customs_ports, unloc=True):
    dfg1 = get_ports(shipping_ports, unloc=False)
    dfg2 = get_ports(customs_ports, unloc=unloc)
    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
    fig, ax = plt.subplots()
    dfg1.plot(ax=ax, color='tab:purple', marker="o", alpha=0.8, zorder=2, label="Shipping Data")
    dfg2.plot(ax=ax, color='tab:orange', marker="*", alpha=0.8, zorder=2, label="Customs Data")
    
    plt.legend(loc="lower left")
    
    world.plot(ax=ax, zorder=1)
    return fig, ax


def ports_to_x_dx(list_of_ports, unloc=True):
    """ports_to_x_dx(["NLRTM", "CNXMG", "CNNBG"]) -> [(10, 11, 2, 2), (12, 13, 1, 1), ...]"""
    dfg = get_ports(list_of_ports, unloc=unloc)

    list_ = []
    for i, port_origin in enumerate(list_of_ports[:-1]):
        port_origin_xy = dfg.query("UNLocode == @port_origin").iloc[0].geometry
        x, y = port_origin_xy.x, port_origin_xy.y

        port_dest = list_of_ports[i + 1]
        port_dest_xy = dfg.query("UNLocode == @port_dest").iloc[0].geometry
        dx, dy = port_dest_xy.x - x, port_dest_xy.y - y

        list_.append((x, y, dx, dy))
    return list_

def test_1():
# data laden
    customs = pd.read_excel("data/Dataset-data-interoperability_rev-HA.xlsx", engine='openpyxl', sheet_name='Customs data')

# shipping company data
    tclu = pd.read_excel("data/TCLU8710985.xlsx", engine='openpyxl')
    ports_oocl = tclu['Port'].str.upper().to_list()

# customs data
    route = customs['ROUTE'].str.split('|')
    route.columns = ['route_lijst']
    customs_route = pd.concat([customs['CONTAINERNUMMER'],route],axis=1)
    ports_customs = customs_route.loc[customs_route['CONTAINERNUMMER']=='TCLU8710985','ROUTE'].values[0]
    plot_ports(ports_oocl,ports_customs)
