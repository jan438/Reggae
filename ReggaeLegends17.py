import os
import sys
import math
import csv
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from ics import Calendar, Event
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER, A4, landscape, portrait
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import blue, green, black, red, pink, gray, brown, purple, orange, yellow, white
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer
from pypdf import PdfReader, PdfWriter
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.graphics.shapes import *
from reportlab.graphics import shapes
from reportlab.graphics import widgetbase
from reportlab.graphics.widgetbase import Widget
from reportlab.graphics.widgets import signsandsymbols
from reportlab.graphics.widgets.signsandsymbols import _Symbol
from reportlab.graphics.charts.textlabels import Label

background1 = "#61869E"
background2 = "#C99D74"

legendsdata = []
s = 70
dx = 0.5 * s                         #                            width hexagon  160
dy = math.sqrt(s**2 - (0.5 * s)**2)  # sqrt(6400 - 1600) = 69.282 height hexagon 138.564 ratio 1.154701077
strokew = 10
strokedx = 0.5 * strokew
strokedy = math.sqrt(strokew**2 - (0.5 * strokew)**2)
ratiodydx = 1.2
extension = 4.35
leftmargin = 25
bottommargin = 6
maxnamewidth = 78.305
reggaefont = "LiberationSerif"

# width = s + 2 * dx      1200
# height = 2 * dy         1039

class HexagonTriangle(_Symbol):
    def __init__(self, x, y):
        self.x = x     # middle point
        self.y = y
        self.fillColor = HexColor(background1)
        self.strokeColor = HexColor(background1)

    def draw(self):
        g = shapes.Group()
        #mcircle = shapes.Circle(self.x, self.y, 2, 
        #          fillColor = blue,
        #          strokeColor = blue,
        #          strokeWidth = 1)
        #g.add(mcircle)
        xl = self.x - dx - 0.5 * s
        xr = self.x + dx + 0.5 * s
        triangle1 = shapes.Polygon(
        points=[xl, self.y,
                xl, self.y + dy,
                xl + dx, self.y + dy],
               fillColor = self.fillColor,
               strokeColor = self.strokeColor,
               strokeWidth = 0)
        g.add(triangle1)
        triangle2 = shapes.Polygon(
        points=[xl, self.y,
                xl, self.y - dy,
                xl + dx, self.y - dy],
               fillColor = self.fillColor,
               strokeColor = self.strokeColor,
               strokeWidth = 0)
        g.add(triangle2)
        triangle3 = shapes.Polygon(
        points=[xr, self.y,
                xr, self.y - dy,
                xr - dx, self.y - dy],
               fillColor = self.fillColor,
               strokeColor = self.strokeColor,
               strokeWidth = 0)
        g.add(triangle3)
        triangle4 = shapes.Polygon(
        points=[xr, self.y,
                xr, self.y + dy,
                xr - dx, self.y + dy],
               fillColor = self.fillColor,
               strokeColor = self.strokeColor,
               strokeWidth = 0)
        g.add(triangle4)
        return g
        
class HexagonLines(_Symbol):
    def __init__(self, x, y):

        self.x = x     # middle point
        self.y = y
        self.fillColor = HexColor(background1)
        self.strokeColor = HexColor(background1)

    def draw(self):
        g = shapes.Group()
        #mcircle = shapes.Circle(self.x, self.y, 2, 
        #          fillColor = blue,
        #          strokeColor = blue,
        #          strokeWidth = 1)
        #g.add(mcircle)
        xl = self.x - dx - 0.5 * s
        xr = self.x + dx + 0.5 * s
        l1 = shapes.Line(xl - strokedx, self.y, xl + dx - strokedx + extension, self.y + dy + extension * ratiodydx, strokeColor = white, strokeWidth = strokew, strokeLineCap = 1)
        g.add(l1)
        l2 = shapes.Line(xl - strokedx, self.y, xl + dx - strokedx + extension, self.y - dy - extension * ratiodydx, strokeColor = white, strokeWidth = strokew, strokeLineCap = 1)
        g.add(l2)
        l3 = shapes.Line(xr + strokedx, self.y, xr - dx + strokedx - extension, self.y + dy + extension * ratiodydx, strokeColor = white, strokeWidth = strokew, strokeLineCap = 1)
        g.add(l3)
        l4 = shapes.Line(xr + strokedx, self.y, xr - dx + strokedx - extension, self.y - dy - extension * ratiodydx, strokeColor = white, strokeWidth = strokew, strokeLineCap = 1)
        g.add(l4)
        la = shapes.Line(xl + dx, self.y + dy + strokedx, xr - dx, self.y + dy + strokedx, strokeColor = white, strokeWidth = strokew, strokeLineCap = 1)
        g.add(la)
        lb = shapes.Line(xl + dx, self.y - dy - strokedx, xr - dx, self.y - dy - strokedx, strokeColor = white, strokeWidth = strokew, strokeLineCap = 1)
        g.add(lb)
        return g
        
def drawLegendTriangle(d, i):
    # 1200 w 1588 h orig file
    img = "Photos/Posters/" + legendsdata[i][0] + ".png"
    d.add(Image(path = img, width = 139.5, height = 121, x = leftmargin + float(legendsdata[i][1]) - 4.5 - dx - 0.5 * dy, y = bottommargin + float(legendsdata[i][2]) - 60.5, mask = None))
    h = HexagonTriangle(leftmargin + float(legendsdata[i][1]), bottommargin + float(legendsdata[i][2]))
    d.add(h)
    return
    
def drawLegendLines(d, i):
    h = HexagonLines(leftmargin + float(legendsdata[i][1]), bottommargin + float(legendsdata[i][2]))
    d.add(h)
    namewidth = pdfmetrics.stringWidth(legendsdata[i][0], reggaefont, 12)
    print(legendsdata[i][0], namewidth)
    d.add(String(leftmargin + float(legendsdata[i][1]) - dx - 4.0 + 0.5 * (maxnamewidth - namewidth), bottommargin + float(legendsdata[i][2]) - 83, legendsdata[i][0], font = reggaefont, fillColor = HexColor(background2), fontSize = 12))
    return
    
def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing
    
def transform_svg(svgfile, tx, ty, sx, sy): 
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    df1 = svgRenderer.render(svg_root)
    gimg = df1.asGroup()
    gimg.translate(tx, ty)
    gimg.scale(sx, sy)
    return gimg
    
if sys.platform[0] == 'l':
    path = '/home/jan/git/Reggae'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Reggae"
os.chdir(path)
pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Regular.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBold', 'Ubuntu-Bold.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuItalic', 'Ubuntu-Italic.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBoldItalic', 'Ubuntu-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DancingScript', 'DancingScript-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DancingScriptBold', 'DancingScript-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DancingScriptItalic', 'DancingScript-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DancingScriptBoldItalic', 'DancingScript-Bold.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramond', 'CormorantGaramond-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramondBold', 'CormorantGaramond-Bold.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramondItalic', 'CormorantGaramond-Italic.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramondBoldItalic', 'CormorantGaramond-BoldItalic.ttf'))

file_to_open = "Data/ReggaeLegends17.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        legendsdata.append(row)
        count += 1
print("Count csv", count)
#pagesize=(595.27,841.89)
d = Drawing(A4[1], A4[0])
bgrect = shapes.Rect(0, 0, A4[1], A4[0], fillColor = background1, strokeColor = background1, strokeWidth = 0)
d.add(bgrect)
for i in range(len(legendsdata)):
    drawLegendTriangle(d, i)
d.add(transform_svg("Tribe of Judah.svg", 35.0, 450, 0.40, 0.40))    
for i in range(len(legendsdata)):
    drawLegendLines(d, i)

renderPDF.drawToFile(d, 'PDF/ReggaeLegends17.pdf')

key = input("Wait")
