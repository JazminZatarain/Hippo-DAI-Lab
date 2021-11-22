import pandas as pd


class DataSets:

    def __init__(self):

        # Load in RICE input parameters for all regions
        self.RICE_DATA = pd.read_excel("InputData/RICE_data.xlsx")
        self.RICE_PARAMETER = pd.read_excel("InputData/RICE_parameter.xlsx")
        self.RICE_input = pd.read_excel("InputData/input_data_RICE.xlsx")
        self.RICE_regional_damage_factor = pd.read_csv("InputData/regional damage frac factor RICE.csv")
        self.RICE_regional_damage_factor = self.RICE_regional_damage_factor.iloc[:, 1:].to_numpy()

        # import World Bank income shares
        self.RICE_income_shares = pd.read_excel("InputData/RICE_income_shares.xlsx")
        self.RICE_income_shares = self.RICE_income_shares.iloc[:, 1:6].to_numpy()

        # import dataframes for SSP (IPCC) uncertainty analysis
        self.RICE_GDP_SSP = pd.read_excel("InputData/Y_Gross_ssp.xlsx").to_numpy()
        self.POP_ssp = pd.read_excel("InputData/pop_ssp.xlsx", header=None)
        self.GDP_ssp = pd.read_excel("InputData/Y_Gross_ssp.xlsx", header=None)
