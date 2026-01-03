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

yellowbackground = "#ffde22"
yellowjamaica = "#fcea2b"
greenjamaica = "#5c9e31"
legendsdata = []
s = 80
dx = 0.5 * s
dy = math.sqrt(s**2 - (0.5 * s)**2)

class Hexagon(_Symbol):
    def __init__(self, x, y):
        self.x = x     # middle point
        self.y = y
        self.fillColor = HexColor(yellowbackground)
        self.strokeColor = HexColor(yellowbackground)

    def draw(self):
        g = shapes.Group()
        #mcircle = shapes.Circle(self.x, self.y, 2, 
        #          fillColor = blue,
        #          strokeColor = blue,
        #          strokeWidth = 1)
        #g.add(mcircle)
        xl = self.x - dx - 0.5 * dy
        xr = self.x + dx + 0.5 * dy
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
        l1 = shapes.Line(xl, self.y, xl + dx, self.y + dy, strokeColor = white, strokeWidth = 5, strokeLineCap = 1)
        g.add(l1)
        l2 = shapes.Line(xl, self.y, xl + dx, self.y - dy, strokeColor = white, strokeWidth = 5, strokeLineCap = 1)
        g.add(l2)
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
        l3 = shapes.Line(xr, self.y, xr - dx, self.y + dy, strokeColor = white, strokeWidth = 5, strokeLineCap = 1)
        g.add(l3)
        l4 = shapes.Line(xr, self.y, xr - dx, self.y - dy, strokeColor = white, strokeWidth = 5, strokeLineCap = 1)
        g.add(l4)
        la = shapes.Line(xl + dx, self.y + dy, xr - dx, self.y + dy, strokeColor = white, strokeWidth = 5, strokeLineCap = 1)
        g.add(la)
        lb = shapes.Line(xl + dx, self.y - dy, xr - dx, self.y - dy, strokeColor = white, strokeWidth = 5, strokeLineCap = 1)
        g.add(lb)
        return g
        
def drawLegend(d, i):
    # 1200 w 1588 h  149 w 179 h factor 8.05
    img = "Photos/Posters/" + legendsdata[i][0] + ".jpg"
    d.add(Image(path = img, width = 149, height = 179, x = float(legendsdata[i][1]) - dx - 0.5 * dy, y = float(legendsdata[i][2]) - 110, mask = None))
    h = Hexagon(float(legendsdata[i][1]), float(legendsdata[i][2]))
    bgrect = shapes.Rect(float(legendsdata[i][1]) - dx - 0.5 * dy, float(legendsdata[i][2]) - 110, 149, 40, fillColor = yellowbackground, strokeColor = yellowbackground, strokeWidth = 0)
    d.add(bgrect)
    d.add(h)
    d.add(String(float(legendsdata[i][1]) - dx, float(legendsdata[i][2]) - 100, legendsdata[i][0], fontName='Courier', fontSize = 15))
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

file_to_open = "Data/ReggaeLegends.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        legendsdata.append(row)
        count += 1
print("Count csv", count)
avatars = 0.1
d = Drawing(A4[1], A4[0])
bgrect = shapes.Rect(0, 0, A4[1], A4[0], fillColor = yellowbackground, strokeColor = yellowbackground, strokeWidth = 0)
d.add(bgrect)
d.add(transform_svg("Photos/BobMarley.svg", 275, 100, avatars, avatars))
d.add(transform_svg("Photos/PeterTosh.svg", 380, 100, avatars, avatars))
for i in range(len(legendsdata)):
    drawLegend(d, i)

renderPDF.drawToFile(d, 'PDF/ReggaeLegends.pdf')

key = input("Wait")
