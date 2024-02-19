from PIL import Image,ImageColor
from os import walk

colorTobeReplace = ImageColor.getcolor("#ff0000", "RGB")
newColor = ImageColor.getcolor("#32a852", "RGB")
transparentColor = ImageColor.getcolor("#00000000", "RGBA")

horizontalLine = 243
verticalLine = 322

def removeTopRetical(pixels,x,y):
    if(x>=306 and x<=333 and y <= 231):
        pixels[x,y] = transparentColor

def formatDots(xDotsCoordinate,yDotsCoordinate):
    if xDotsCoordinate[3] - xDotsCoordinate[1] > 25: 
        return xDotsCoordinate,yDotsCoordinate
    else:
        lengthMinorArr = len(xDotsCoordinate) // 2
        xMinor_1 = xDotsCoordinate[:lengthMinorArr]
        xMinor_2 = xDotsCoordinate[lengthMinorArr:]

        xMinor_1.pop(-1)
        xMinor_1.reverse()
        xMinor_2.pop(0)

        xMinor_1 = [x for index,x in enumerate(xMinor_1) if (index-2)%4==0 or (index-3)%4==0]
        xMinor_2 = [y for index,y in enumerate(xMinor_2) if (index-2)%4==0 or (index-3)%4==0]

        xMinor_1.reverse()

        xResult = xMinor_1 + xMinor_2
        yResult = [yCoor for index, yCoor in enumerate(yDotsCoordinate) if (index-2)%4==0 or (index-3)%4==0]

        return xResult,yResult


filenames = next(walk("./reticle_ccd_type_0"), (None, None, []))[2]

for filename in filenames:
    image = Image.open(f'./reticle_ccd_type_0/{filename}',"r")
    pixels = image.load()
    width, height = image.size

    xDotsCoordinate = []
    yDotsCoordinate = []
    dots = []

    for x in range(width):
        for y in range(height):
            removeTopRetical(pixels,x,y)

    for x in range(width):
        r, g, b, a = pixels[(x, horizontalLine)]
        if (r, g, b) == colorTobeReplace:
            xDotsCoordinate.append(x)

    for y in range(height):
        r, g, b, a = pixels[(verticalLine, y)]
        if (r, g, b) == colorTobeReplace:
            yDotsCoordinate.append(y)

    xDots,yDots = formatDots(xDotsCoordinate,yDotsCoordinate[2:])

    for x in xDots:
        for y in yDots:
            dots.append((x,y))

    for x in range(width):
        for y in range(height):
            if (x,y) in dots:
                pixels[x,y] = colorTobeReplace

    image.save(f'./new_reticle_ccd_type_0/{filename}', 'PNG')



