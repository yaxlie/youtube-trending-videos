from src.analyzers.analyzer import Analyzer

class DummyAnalyzer(Analyzer):
    '''Just copy the value in cell.'''

    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
        super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'Copy', multiple=True)

    def decide(self, data: str):
        return data