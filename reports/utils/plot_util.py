import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
from plotly.graph_objs import *
from io import StringIO

class PlotUtil():
    def __init__(self, files, json_file):
        self.files = files
        self.json_file = open(json_file)
        self.data = json.load(self.json_file)

    def __json2csv(self, data, file, analyzer):
        csv=''
        
        if type(list(data[self.files[0]][analyzer].values())[0]) == dict:
            keys = list(data[file][analyzer].values())[0].keys()
            csv += 'Columns,' + ','.join(keys)

            for column in list(data[file][analyzer]):
                csv += '\n' + f'{column},' + ','.join([str(data[file][analyzer][column].get(key, 0)) for key in keys])
            return csv
        elif type(list(data[self.files[0]][analyzer].values())[0]) == int:
            keys = list(data[file][analyzer].keys())
            values = list(data[file][analyzer].values())
            csv += ','.join(keys)
            csv += '\n'
            csv += ','.join([str(val) for val in values])
            return csv

    def close(self):
        self.json_file.close()

    def plot_table(self, analyzer):
        try:
            for file in self.files:
                csv = self.__json2csv(self.data, file, analyzer)
                df = pd.read_csv(StringIO(csv), sep=",")
                layout = go.Layout(title=f'{analyzer} {file}')

                table = ff.create_table(df)
                fig = go.Figure(data=table, layout=layout)

                plotly.offline.iplot(fig)
        except Exception as e:
            print('Nie można wyświetlić', e)


    def plot_graph(self, analyzer):
        try:
            for file in self.files:
                csv = self.__json2csv(self.data, file, analyzer)
                df = pd.read_csv(StringIO(csv), sep=",")
                layout = go.Layout(title=f'{analyzer} {file}', barmode='stack')
                columns=list(df.columns)
                
                if len(list(df.iloc)) == 1:
                    data = [go.Bar(name=analyzer, x=columns, y=list(df.iloc)[0])]
                else:
                    data = [go.Bar(name=row[0], x=columns[1:], y=row[1:]) for row in list(df.iloc)]

                fig = go.Figure(data=data, layout=layout)
                plotly.offline.iplot(fig)
        except Exception as e:
            print('Nie można wyświetlić', e)