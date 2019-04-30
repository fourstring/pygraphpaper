from __future__ import annotations
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas,textobject
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from typing import List
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other: Coordinate):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __rmul__(self, other: float):
        return Coordinate(other * self.x, other * self.y)

    def __sub__(self, other: Coordinate):
        return Coordinate(self.x - other.x, self.y - other.y)


class CustomCanvas(canvas.Canvas):
    def line(self, c1: Coordinate, c2: Coordinate, unit=mm):
        super().line(c1.x * unit, c1.y * unit, c2.x * unit, c2.y * unit)

    def lines(self, coordinates: List[Coordinate], closed: bool = False):
        for i in range(0, len(coordinates) - 1):
            self.line(coordinates[i], coordinates[i + 1])
        if closed:
            self.line(coordinates[-1], coordinates[0])

    def drawString(self, position: Coordinate, unit=mm, *args, **kwargs):
        super().drawString(position.x*unit, position.y*unit, *args, **kwargs)

    def translate(self, delta:Coordinate,unit=mm):
        super().translate(delta.x*unit,delta.y*unit)

if __name__ == '__main__':
    paper = CustomCanvas("graphpaper.pdf", pagesize=A4)
    paper_width=210
    paper_height=297
    margin = 10
    bold_line = 0.3 * mm
    regular_line = 0.1 * mm
    minor = 1
    major = 10
    bottom_left = Coordinate(0, 0)
    top_right = Coordinate(paper_width, paper_height)
    graph_bottom_left = bottom_left + Coordinate(margin, margin)
    graph_top_right = top_right - Coordinate(margin, margin)
    graph_top_left = graph_bottom_left + Coordinate(0, paper_height - 2 * margin)
    graph_bottom_right = graph_bottom_left + Coordinate(paper_width - 2 * margin, 0)
    # draw Frame
    pdfmetrics.registerFont(TTFont('SourceHans', 'SourceHanSans-Medium.ttc'))
    paper.setStrokeColor(colors.grey)
    paper.setLineWidth(bold_line)
    paper.lines([graph_bottom_left, graph_bottom_right, graph_top_right, graph_top_left], True)
    paper.setFont("SourceHans",size=5,leading=0)
    # draw Vertical Lines
    for i in range(graph_bottom_left.x + 1, graph_bottom_right.x):
        if i % major == 0:
            paper.setLineWidth(bold_line)
            #draw label
            paper.saveState()
            # Add displacement to label position for better appearance
            label_number=paper_width - 2 * margin-(i - graph_bottom_left.x)
            paper.translate(Coordinate(i+0.2, graph_bottom_left.y -1-len(str(label_number)) \
                                       ))
            paper.rotate(90)
            paper.drawString(Coordinate(0,0), text=str(label_number))
            paper.restoreState()
        else:
            paper.setLineWidth(regular_line)
        paper.line(Coordinate(i, graph_bottom_left.y), Coordinate(i, graph_top_right.y))
    # draw Horizontal Lines
    for i in range(graph_bottom_left.y + 1, graph_top_left.y):
        if i % major == 0:
            paper.setLineWidth(bold_line)
            paper.saveState()
            label_number=i - graph_bottom_left.y
            paper.translate(Coordinate(graph_bottom_right.x + 3, (i-0.8)))
            paper.rotate(90)
            paper.drawString(Coordinate(0,0), text=str(label_number))
            paper.restoreState()
        else:
            paper.setLineWidth(regular_line)
        paper.line(Coordinate(graph_bottom_left.x, i), Coordinate(graph_top_right.x, i))
    paper.showPage()
    paper.save()
