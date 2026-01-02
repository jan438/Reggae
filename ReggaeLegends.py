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
legendsdata = []

class Hexagon(_Symbol):
    def __init__(self, x, y):
        self.x = x     # middle point
        self.y = y
        self.fillColor = HexColor(yellowbackground)
        self.strokeColor = HexColor(yellowbackground)

    def draw(self):
        s = 80
        g = shapes.Group()
        mcircle = shapes.Circle(self.x, self.y, 2, 
                  fillColor = blue,
                  strokeColor = blue,
                  strokeWidth = 1)
        g.add(mcircle)
        dx = 0.5 * s
        dy = math.sqrt(s**2 - 0.5 * s**2)
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
        
def drawLegend(i):
    h = Hexagon(350, 400)
    d.add(h)
    print(legendsdata[i])
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

A4_width = A4[0]
A4_height = A4[1]

avatars = 0.1

d = Drawing(297*mm, 210*mm)
d.add(transform_svg("Photos/BobMarley.svg", 300, 200, avatars, avatars))
d.add(transform_svg("Photos/PeterTosh.svg", 380, 100, avatars, avatars))
drawLegend(0)

renderPDF.drawToFile(d, 'PDF/ReggaeLegends.pdf')

key = input("Wait")
