import json
import matplotlib.pyplot as plt
import numpy as np
import os

class ChartMaker():
    def __init__(self, json_data: str):
        self.json_data = json_data
        self.out_dir = 'out'

        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

    def plot (self):
        j = json.loads(self.json_data)

        for filename_key in j.keys():
            for findername_key in j[filename_key].keys():
                for columnname_key in j[filename_key][findername_key].keys():
                    keys = j[filename_key][findername_key][columnname_key].keys()
                    values = j[filename_key][findername_key][columnname_key].values()
                    if keys and values:
                        x = list(keys)
                        y = list(values)
                        fig, ax = plt.subplots() 

                        width = 0.75 
                        ind = np.arange(len(y))
                        ax.barh(ind, y, width)
                        ax.set_yticks(ind+width/2)
                        ax.set_yticklabels(x, minor=False)
                        plt.title(f'{findername_key}-{columnname_key}') 
                        for i, v in enumerate(y):
                            ax.text(v + 3, i + .05, str(v), fontweight='bold')

                        # plt.show()
                        plt.savefig(os.path.join(self.out_dir, f'{findername_key}_{columnname_key}.png'), dpi=300, format='png', bbox_inches='tight')