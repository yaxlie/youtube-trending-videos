import src.tools.colors
import numpy as np
import re
from src.analyzers.image_analyzer import ImageAnalyzer
from PIL import Image
from collections import Counter
from io import BytesIO
from imageai.Detection import ObjectDetection
from imageai.Prediction import ImagePrediction

class ColorsAnalyzer(ImageAnalyzer):
    '''
    Find main colors of the image
    '''
    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
        super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Main colors', multiple=True)

    def decide(self, image:Image):
        image = image.crop((20, 20, 100, 60))
        image = image.resize((20, 20))
        colors = image.getcolors(400) # width * height
        color_names = [src.tools.colors.get_colour_name(color[1]) for color in colors] # TODO: optimize
        colors_count = Counter(color_names)
        
        return '-'.join(sorted([color[0] for color in colors_count.most_common(5)]))


class TextAnalyzer(ImageAnalyzer):
    '''
    Check if image contain text.
    WARNING: Tesseract-ocr installation is needed! 
    refs https://github.com/tesseract-ocr/tesseract/wiki
    '''
    
    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
        super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Has text', multiple=True)

    def decide(self, image:Image):
        import pytesseract
        text = pytesseract.image_to_string(image)
        text = re.sub(r"[^A-Za-z]+", '', text)
        return text


class ObjectsNamesAnalyzer(ImageAnalyzer):
    '''
    Find objects in the image
    '''

    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv): #TODO: no limit
        super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Objects', multiple=True)
        self.detector = init_detector("./data/yolo.h5")

    def decide(self, image:Image):
        image_data = np.array(image)
        try:
            # Library bug: if prediction array is empty (e.g. no object with p > 0.1) there will be ValueError
            # + For 'stream' there is no return, lol
            # We have to set output_type=None - doesn't mention in ImageAI docs
            # TODO: Report on https://github.com/OlafenwaMoses/ImageAI
            detected_copy, detected_objects = self.detector.detectObjectsFromImage(input_image=image_data, input_type="array", 
            minimum_percentage_probability=0, output_type='array')
        except ValueError:
            return None

        if not detected_objects:
            return 'Unknown'
        else:
            objects = [obj['name'] for obj in detected_objects] 
            objects = list(dict.fromkeys(objects))
            return objects


class ObjectsNumberAnalyzer(ImageAnalyzer):
    '''
    Return number of different objects on image
    '''

    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
        super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Number of objects', multiple=True)
        self.detector = init_detector("./data/yolo.h5")

    def decide(self, image:Image):
        image_data = np.array(image) 
        try:
            detected_copy, detected_objects = self.detector.detectObjectsFromImage(input_image=image_data, input_type="array", 
            minimum_percentage_probability=0, output_type='array')
        except ValueError:
            return None

        if not detected_objects:
            return 0
        else:
            objects = [obj['name'] for obj in detected_objects] 
            objects = list(dict.fromkeys(objects))
            return str(len(objects))


# class AccentAnalyzer(Analyzer):

# class EmotionsAnalyzer(Analyzer):
#     '''
#     Detect emotions emanating from image (not only face)
#     '''

def init_detector(model_path):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    return detector