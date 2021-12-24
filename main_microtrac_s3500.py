"""
Test code to show functionality of the Microtrac Class
2021, Ramanan Pitchumani
"""

from microtrac_s3500 import MicrotracS3500

microtracs3500_data_filename = "MTData_25_6_2021_11_24_7.csv"

mt = MicrotracS3500(microtracs3500_data_filename)

df = mt.df

idxs = mt.dict_indices

df_psd = mt.psd

df_pct = mt.percentiles


print("-------------------------")
print(df)

print(mt.title)
print(mt.id_1)
print(mt.id_2)
print(mt.date)
print(mt.db_rec)
print(mt.db_name)

print(mt.mv)
print(mt.mn)
print(mt.ma)
print(mt.cs)
print(mt.sd)

print(mt.mz)
print(mt.si)
print(mt.ski)
print(mt.kg)
