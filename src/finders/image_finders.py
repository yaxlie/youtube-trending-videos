from finders.image_finder import ImageFinder

class ColorsFinder(ImageFinder):
    '''
    Find main colors of the image
    '''
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Main colors', multiple=True)

    def is_condition_met(self, data: str):
        from PIL import Image
        from collections import Counter
        from io import BytesIO
        import tools.colors
        from collections import Counter

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


# class TextFinder(AttributeFinder):
#     '''
#     Check if image contain text
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Has text', multiple=True)

# class MainObjectFinder(AttributeFinder):
#     '''
#     Find name of main object in the image
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Main object', multiple=True)

# class ObjectsNumberFinder(AttributeFinder):
#     '''
#     Find number of objects in the image
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Number of objects', multiple=True)

# class AccentFinder(AttributeFinder):
#     '''
#     Does image contain accent elements (i.e. bright color)?
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Has accent', multiple=True)

# class EmotionsFinder(AttributeFinder):
#     '''
#     Detect emotions emanating from image
#     '''
#     def __init__(self, file_name: str, column_name: str, data):
#         super().__init__(file_name, column_name, data, f'Emotions', multiple=True)