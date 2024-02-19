from PIL import Image,ImageColor
from os import walk
import os

colorTobeReplace = ImageColor.getcolor("#ff0000", "RGB")
newColor = ImageColor.getcolor("#e6b800", "RGB")
transparentColor = ImageColor.getcolor("#00000000", "RGBA")


folderNames = filenames = next(walk("./red"), (None, None, []))[1]

print(folderNames)

for folder in folderNames:
    os.makedirs(f'./brown/{folder}')
    fileNames = next(walk(f'./red/{folder}'), (None, None, []))[2]
    for file in fileNames:
        image = Image.open(f'./red/{folder}/{file}',"r")
        pixels = image.load()
        width, height = image.size
        for w in range(width):
            for h in range(height):
                r, g, b, a = pixels[(w, h)]
                if (r, g, b) == colorTobeReplace:
                    pixels[w, h] = newColor

        image.save(f'./brown/{folder}/{file}', 'PNG')

