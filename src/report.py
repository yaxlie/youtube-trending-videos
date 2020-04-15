from tools.chart_maker import ChartMaker

if __name__ == "__main__":
    json = 'result.json'
    with open(json) as f:
        cm = ChartMaker(f.read())
        cm.plot()