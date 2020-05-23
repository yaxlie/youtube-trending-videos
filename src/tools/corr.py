import glob
import os
import pandas as pd
import csv

def merge_columns(lines_number, directories):
    mapper = {
        "False": 0,
        "True": 1,
        "Monday": 1,
        "Wednesday": 2,
        "Tuesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
    }
    for directory in directories:
        dir_name = os.path.basename(directory)
        merged_csv_file = f'out/summary_{dir_name}.csv'
        open(merged_csv_file, 'a').close()

        merged_content = ['' for n in range(lines_number) ]
        
        for csv_file_name in glob.glob(f'{directory}/*.csv'):
            new_content = []
            with open(csv_file_name) as csv_file:
                lines = csv_file.readlines()
                for line1, line2 in zip(merged_content, lines):
                    new_content.append('{}{}'.format(line1.rstrip(), line2.rstrip()))
                merged_content = new_content


        merged_content = '\n'.join(merged_content)
        for key, value in mapper.items():
            merged_content = merged_content.replace(key, str(value))

        with open(merged_csv_file, 'w+', encoding='utf-8') as merged_file:
            merged_file.write(merged_content)


def print_correlation(filename):
    d = pd.read_csv(filename, sep=';')
    corr = d.corr().abs()
    corr.style.background_gradient(cmap='coolwarm')


lines_number = 1001
directories = ['out/data/GB_videos_5p', 'out/data/US_videos_5p']

merge_columns(lines_number, directories)

for directory in directories:
    dir_name = os.path.basename(directory)
    merged_csv_file = f'out/summary_{dir_name}.csv'

    print_correlation(merged_csv_file)