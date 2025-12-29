import os
import sys
import math
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

def drawRect(c, x, y, w, h, a, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * a)
    p.arcTo(x, y, x + a, y + a, startAng = 180, extent = 90)  # arc left below
    p.lineTo(x + w, y)                                                           # horizontal line
    p.arcTo(x + w, y, x + w + a, y + a, startAng = 270, extent = 90)  # arc right below
    p.lineTo(x + w + a, y + h)                                                      # vertcal line
    p.arcTo(x + w, y + h, x + w + a, y + h + a, startAng = 0, extent = 90)     # arc right above
    p.lineTo(x + 0.5 * a, y + h + a)                                                   # horizontal line
    p.arcTo(x, y + h, x + a, y + h + a, startAng = 90, extent = 90)    # arc left above
    p.lineTo(x, y + 0.5 * a)                                                                # vertcal line
    c.drawPath(p, stroke = 0, fill = 1)
    
def drawTriangle(c, x, y, w, h, d, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    if d == 0:                    #hexagonal right under
        p.moveTo(x, y)
        p.lineTo(x + w, y)
        p.lineTo(x + w, y + h)
        p.lineTo(x, y)
    if d == 1:                    #hexagonal left under
        p.moveTo(x + w, y)
        p.lineTo(x, y + h)
        p.lineTo(x, y)
        p.lineTo(x + w, y)
    if d == 2:                    #hexagonal left above
        p.moveTo(x, y)
        p.lineTo(x + w, y + h)
        p.lineTo(x, y + h)
        p.lineTo(x, y)
    if d == 3:                    #hexagonal right above
        p.moveTo(x, y + h)
        p.lineTo(x + w, y + h)
        p.lineTo(x + w, y)
        p.lineTo(x, y + h)
    c.drawPath(p, stroke = 0, fill = 1)
    
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

A4_width = A4[0]
A4_height = A4[1]

c = Canvas("PDF/Reggae.pdf", pagesize=landscape(A4))
c.drawImage("Photos/Example.png", 200, 100, width = 115, height = 76, mask='auto')
gimg = transform_svg("Photos/BobMarley.svg", 300, 300, 0.5 , 0.5)
print("gimp", gimg)
drawRect(c, 300, 300, 50, 50, 20, yellowbackground)
drawTriangle(c, 200, 200, 50, 75, 0, yellowbackground)
drawTriangle(c, 150, 200, 50, 75, 1, yellowbackground)
drawTriangle(c, 150, 275, 50, 75, 2, yellowbackground)
drawTriangle(c, 200, 275, 50, 75, 3, yellowbackground)
c.save()

key = input("Wait")
