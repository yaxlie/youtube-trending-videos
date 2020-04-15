import tools.colors
from analyzers.image_analyzer import ImageAnalyzer
from PIL import Image
from collections import Counter
from io import BytesIO

class ColorsAnalyzer(ImageAnalyzer):
    '''
    Find main colors of the image
    '''
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Main colors', multiple=True)

    def decide(self, data: str):
        if data in self.images:
            image_data = self.images[data]
        else:
            return None

        image = Image.open(BytesIO(image_data))
        image = image.crop((20, 20, 100, 60))
        image = image.resize((20, 20))
        colors = image.getcolors(400) # width * height
        color_names = [tools.colors.get_colour_name(color[1]) for color in colors] # TODO: optimize
        colors_count = Counter(color_names)
        
        return '-'.join(sorted([color[0] for color in colors_count.most_common(5)]))


# class TextAnalyzer(Analyzer):
#     '''
#     Check if image contain text
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Has text', multiple=True)

# class MainObjectAnalyzer(Analyzer):
#     '''
#     Find name of main object in the image
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Main object', multiple=True)

# class ObjectsNumberAnalyzer(Analyzer):
#     '''
#     Find number of objects in the image
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Number of objects', multiple=True)

# class AccentAnalyzer(Analyzer):
#     '''
#     Does image contain accent elements (i.e. bright color)?
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Has accent', multiple=True)

# class EmotionsAnalyzer(Analyzer):
#     '''
#     Detect emotions emanating from image
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Emotions', multiple=True)