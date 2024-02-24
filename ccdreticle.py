from PIL import Image,ImageColor
from os import walk

colorTobeReplace = ImageColor.getcolor("#ff0000", "RGB")
newColor = ImageColor.getcolor("#32a852", "RGB")
transparentColor = ImageColor.getcolor("#00000000", "RGBA")

horizontalLine = 191
verticalLine = 191

def removeTopRetical(pixels,x,y):
    if(x>=175 and x<=205 and y <= 185):
        pixels[x,y] = transparentColor

def formatDots(xDotsCoordinate,yDotsCoordinate):
    lengthMinorArr = len(xDotsCoordinate) // 2
    xMinor_1 = xDotsCoordinate[:lengthMinorArr]
    xMinor_2 = xDotsCoordinate[lengthMinorArr:]

    xMinor_2.pop(0)
    
    if xDotsCoordinate[3] - xDotsCoordinate[2] > 25: 
        return xMinor_1,xMinor_2,yDotsCoordinate
    else:
        xMinor_1.reverse()
        xMinor_1 = [x for index,x in enumerate(xMinor_1) if index%2==1]
        xMinor_2 = [y for index,y in enumerate(xMinor_2) if index%2==1]
        xMinor_1.reverse()
        yResult = [yCoor for index, yCoor in enumerate(yDotsCoordinate) if index%2==1]
        return xMinor_1,xMinor_2,yResult


filenames = next(walk("./red/reticle_type_0"), (None, None, []))[2]


for filename in filenames:
    image = Image.open(f'./red/reticle_type_0/{filename}',"r")
    pixels = image.load()
    width, height = image.size

    xDotsCoordinate = []
    yDotsCoordinate = []
    lDots = []
    rDots = []

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

    x1,x2,yDots = formatDots(xDotsCoordinate,yDotsCoordinate[1:])

    # print(x1,x2,yDots,None)
    for x in x1:
        for y in yDots:
            lDots.extend([(x,y),(x-1,y),(x,y+1),(x-1,y+1)])

    for x in x2:
        for y in yDots:
            rDots.extend([(x,y),(x+1,y),(x,y+1),(x+1,y+1)])

    for x in range(width):
        for y in range(height):
            if (x,y) in lDots+rDots:
                pixels[x,y] = colorTobeReplace

    image.save(f'./red/new_reticle_type_0/{filename}', 'PNG')



