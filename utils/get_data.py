import os
import time
from collections import defaultdict
import pandas as pd

main_directory = './db'

folder_count_by_date = defaultdict(int)

for folder in os.listdir(main_directory):

    folder_path = os.path.join(main_directory, folder)

    if os.path.isdir(folder_path) and folder.startswith('faiss_index_'):

        try:
            date_part = folder.split('_')[2]
            folder_count_by_date[date_part] += 1
        except IndexError:
            continue
        
dataframe = pd.DataFrame(
    {
        "date": folder_count_by_date.keys(),
        "num_used": folder_count_by_date.values()
    }
)

dataframe.to_csv('./db/data_usage.csv')
time.sleep(60)