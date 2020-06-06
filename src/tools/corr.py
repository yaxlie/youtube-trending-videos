import glob
import os
import pandas as pd
import csv
import re

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

    ignored_words = [
        'person',
        'tv'
    ]

    for directory in directories:
        dir_name = os.path.basename(directory)
        merged_csv_file = f'out/summary_{dir_name}.csv'
        open(merged_csv_file, 'a').close()

        merged_content = None
        
        for csv_file_name in glob.glob(f'{directory}/*.csv'):
            new_content = []
            with open(csv_file_name) as csv_file:
                lines = csv_file.readlines()

                if not merged_content:
                    if not lines_number:
                        lines_number = len(lines)
                    merged_content = ['' for n in range(lines_number) ]

                for line1, line2 in zip(merged_content, lines):
                    # convert array representation of string to one word
                    # if '[' in line2:
                    #     words = line2.strip('][').split(', ')
                    #     words = [word for word in words if word not in ignored_words]
                    #     line2 = words[0] + ';'
                    
                    if '{' in line2 or '[' in line2:
                        temp = line2.split("'")
                        if len(temp) > 1:
                            line2 = temp[1]
                            try:
                                line2 = ''.join([str(int(l)) for l in line2])
                            except Exception as e:
                                line2 = ''.join([str(ord(l)) for l in line2[0:4]])
                        else:
                            line = '-1'
                    line2 = re.sub(r'[^a-zA-z\-0-9]+', '', line2) + ';'

                    if re.search(r'[a-zA-Z]', line2):
                        if len(line2) > 4:
                            line2 = ''.join([str(ord(l)) for l in line2[0:4]]) + ';'
                        else:
                            line2 = ''.join([str(ord(l)) for l in line2[:-1]]) + ';'
                    # merge to one csv
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


# lines_number = 1001
lines_number = None
directories = ['out/data/GB_videos_5p', 'out/data/US_videos_5p']
# directories = ['out/data/GB_videos_5p']

merge_columns(lines_number, directories)

for directory in directories:
    dir_name = os.path.basename(directory)
    merged_csv_file = f'out/summary_{dir_name}.csv'

    print_correlation(merged_csv_file)