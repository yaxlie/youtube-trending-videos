from tools.chart_maker import ChartMaker

json = 'result.json'
with open(json) as f:
    cm = ChartMaker(f.read())
    cm.plot()