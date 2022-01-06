"""
Class to read exported Microtrac 3500 Particle Analysis CSV File
2021, Ramanan Pitchumani
"""
import pandas as pd
import numpy as np


class MicrotracS3500:

    def __init__(self, path_csv):

        self.path_csv = path_csv
        self.df = pd.read_csv(path_csv,
                              index_col=None, header=0, engine="python")
        self.df.columns = ["Column 1", "Column 2", "Column 3"]
        self.get_indices()
        self.get_sample_information()
        self.get_statistics()
        self.get_percentiles()

    def get_sample_information(self):

        filter_title = self.df[self.df["Column 1"].str.contains("Title", na=False)].reset_index()
        self.title = filter_title["Column 2"][0]

        filter_id_1 = self.df[self.df["Column 1"].str.contains("ID  1:", na=False)].reset_index()
        # print("id1", filter_id_1)
        self.id_1 = filter_id_1["Column 2"][0]

        filter_id_2 = self.df[self.df["Column 1"].str.contains("ID  2:", na=False)].reset_index()
        # print("id2", filter_id_2)
        self.id_2 = filter_id_2["Column 2"][0]

        filter_date = self.df[self.df["Column 1"].str.contains("Date:", na=False)].reset_index()
        # print("date", filter_date)
        self.date = filter_date["Column 2"][0]

        filter_time = self.df[self.df["Column 1"].str.contains("Time:", na=False)].reset_index()
        # print("time", filter_time)
        self.time = filter_time["Column 2"][0]

        filter_db_rec = self.df[self.df["Column 1"].str.contains("Db  Rec#:", na=False)].reset_index()
        # print("db rec", filter_db_rec)
        self.db_rec = filter_db_rec["Column 2"][0]

        filter_db_name = self.df[self.df["Column 1"].str.contains("DB  Name:", na=False)].reset_index()
        # print("db name", filter_db_name)
        self.db_name = filter_db_name["Column 2"][0]

    def get_statistics(self):

        filter_mv = self.df[self.df["Column 2"].str.contains("MV\(um\):", na=False)].reset_index()
        self.mv = filter_mv["Column 3"][0]

        filter_mn = self.df[self.df["Column 2"].str.contains("MN\(um\):", na=False)].reset_index()
        self.mn = filter_mn["Column 3"][0]

        filter_ma = self.df[self.df["Column 2"].str.contains("MA\(um\):", na=False)].reset_index()
        self.ma = filter_ma["Column 3"][0]

        filter_cs = self.df[self.df["Column 2"].str.contains("CS:", na=False)].reset_index()
        self.cs = filter_cs["Column 3"][0]

        filter_sd = self.df[self.df["Column 2"].str.contains("SD:", na=False)].reset_index()
        self.sd = filter_sd["Column 3"][0]

        filter_mz = self.df[self.df["Column 2"].str.contains("Mz:", na=False)].reset_index()
        self.mz = filter_mz["Column 3"][0]

        filter_si = self.df[self.df["Column 2"].str.contains("si:", na=False)].reset_index()
        self.si = filter_si["Column 3"][0]

        filter_ski = self.df[self.df["Column 2"].str.contains("Ski:", na=False)].reset_index()
        self.ski = filter_ski["Column 3"][0]

        filter_kg = self.df[self.df["Column 2"].str.contains("Kg:", na=False)].reset_index()
        self.kg = filter_kg["Column 3"][0]

    @property
    def percentiles(self):

        self.get_percentiles()
        return self.df_percentiles

    def get_percentiles(self):

        idx_start = self.df[self.df["Column 1"].str.contains("Percentiles", na=False)].index[0]
        idx_end = self.df[self.df["Column 1"].str.contains("Size  Percent", na=False)].index[0]

        # print("idx", idx_start)
        # print("idx", idx_end)

        self.df_percentiles = self.df.iloc[idx_start+1:idx_end-1]
        self.df_percentiles.reset_index(drop=True, inplace=True)
        self.df_percentiles = self.df_percentiles.rename(columns=self.df_percentiles.iloc[0])
        self.df_percentiles = self.df_percentiles[1:]
        self.df_percentiles.drop(columns=self.df_percentiles.columns[0],
                                 axis=1,
                                 inplace=True)

    @property
    def psd(self):

        self.get_psd()
        return self.df_psd

    def get_psd(self):

        idx_start = self.df[self.df["Column 1"].str.contains("Size\(um\)", na=False)].index[0]
        # print("idx", idx_start)

        self.df_psd = self.df.iloc[idx_start:self.df.shape[0]]
        self.df_psd.reset_index(drop=True, inplace=True)
        self.df_psd = self.df_psd.rename(columns=self.df_psd.iloc[0])
        self.df_psd = self.df_psd[1:]

    def get_indices(self):

        find_strings = ["Summary Data", "User  Defined  Calculations",
                        "Percentiles", "Peaks", "Size(um)"]

        self.dict_indices ={}

        for item in find_strings:

            self.dict_indices[item] = np.where(self.df == item)
