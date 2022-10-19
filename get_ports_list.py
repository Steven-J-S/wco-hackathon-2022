import pandas as pd


def get_ports_list(container):
    list_trace = (
        pd.read_excel("data/ports-per-container.xlsx")[container]
        .dropna()
        .str.upper()
        .values.tolist()
    )
    customs_data = pd.read_excel(
        "data/Dataset-data-interoperability_rev-HA.xlsx", sheet_name="Customs data"
    )
    customs_data = customs_data[customs_data["CONTAINERNUMMER"] == container][
        "ROUTE"
    ].values[0]
    list_customs = customs_data.split("(", 1)[0].upper().split("|")
    return list_trace, list_customs
