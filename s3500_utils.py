"""
Utility Functions which work together with the Microtrac S3500 Class
"""

from typing import List, Dict, Any
import os
import glob
from pathlib import Path
import datetime
from tqdm import tqdm
import re

from s3500 import S3500


def get_s3500_file_list(s3500_path: str) -> List:

    s3500_psd_pattern = "MTData*.csv"

    s3500_psd_files = glob.glob(os.path.join(s3500_path, s3500_psd_pattern))

    return s3500_psd_files


def get_s3500_data_from_file_list(psd_files: List) -> List[Dict]:

    re_pattern_sample_id = "([LR]\d{8}-\d{3})_(\d*)_(\d*)_(\d*)_(\d*)_(\d*)_(\d*)"
    list_s5000_data = []

    for psd_file in tqdm(psd_files):

        psd_pathlib = Path(psd_file)
        psd_stem = psd_pathlib.stem

        re_pattern_extract = re.findall(re_pattern_sample_id, psd_stem)

        file_name_id = re_pattern_extract[0][0]
        file_name_date = int(re_pattern_extract[0][1])
        file_name_month = int(re_pattern_extract[0][2])
        file_name_year = int(re_pattern_extract[0][3])
        file_name_hour = int(re_pattern_extract[0][4])
        file_name_minute = int(re_pattern_extract[0][5])
        file_name_second = int(re_pattern_extract[0][6])

        file_name_datetime = datetime.datetime(file_name_year, file_name_month, file_name_date, file_name_hour, file_name_minute, file_name_second)

        try:
            s3500 = S3500(psd_file)

            # print(s3500.percentiles)
            # print(file_name_id)

            dict_s3500_data = {
                "file_name": psd_stem,
                "file_name_id": file_name_id,
                "file_name_date_time": file_name_datetime
            }

            for dp in s3500.percentiles["%Tile"].to_list():

                dict_s3500_data.update(
                    {f"d{dp:.0f}": s3500.percentiles.loc[s3500.percentiles["%Tile"]==dp, "Size(um)"].iloc[0]}
                )

            dict_s3500_data.update({"psd": s3500.psd})

            list_s5000_data.append(dict_s3500_data)

        except Exception as e:
            ...

    return list_s5000_data
