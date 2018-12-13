import os
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

fnt = ImageFont.truetype('NotoSans-Thin.ttf', 20)
fnt2 = ImageFont.truetype('NotoSans-Thin.ttf', 11)
points = []
corners = [0, 128, 255]
for x in corners:
	for y in corners:
		points.append((x, y))

def make_folder(folder_name):
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)

def expand_a_b(a, b, w, h):
	if a == 0:
		x0 = 0
		x1 = 1
		da = 0
	elif a == 128:
		x0 = 126
		x1 = 129
		da= -int(w/2)
	elif a == 255:
		x0 = 254
		x1 = 255
		da = -w
	if b == 0:
		y0 = 0
		y1 = 1
		db = 0
	elif b == 128:
		y0 = 126
		y1 = 129
		db = -int(h/2)-2
	elif b == 255:
		y0 = 254
		y1 = 255
		db = -h-2
	return (da, db, x0, x1, y0, y1)

def a_b_2_lat_lng(z, x, y, a, b):
	if a == 0:
		dx = 0
	elif a == 128:
		dx = .5
	elif a == 255:
		dx = 1
	if b == 0:
		dy = 0
	elif b == 128:
		dy = .5
	elif b == 255:
		dy = 1
	x = x + dx
	y = y + dy
	n = 2.0 ** zoom
	lon_deg = x / n * 360 - 180
	lat_rad = math.atan(math.sinh(math.pi*(1-2*y/n)))
	lat_deg = math.degrees(lat_rad)
	return lat_deg, lon_deg



for zoom in range(12):
	make_folder("%d" % zoom)
	for x in range(2**zoom):
		make_folder("%d/%d" % (zoom, x))
		for y in range(2**zoom):
			filename = '%d/%d/%d.png' % (zoom, x, y)
			im = Image.new('RGB', (256, 256), "white")
			draw = ImageDraw.Draw(im)

			draw.line([0,0,255,0], fill="yellow", width=1)
			draw.line([255,0,255,255], fill="yellow", width=1)
			draw.line([0,0,0,255], fill="yellow", width=1)
			draw.line([0,255,255,255], fill="yellow", width=1)

			text = 'zoom: %d\nx: %d\ny: %d' % (zoom, x, y)
			draw.multiline_text((10,30), text, fill="blue", font=fnt)
			draw.text((10, 188), filename, fill="green", font=fnt)
			for pt in points:
				a, b = pt
				lat, lng = a_b_2_lat_lng(zoom, x, y, a, b)
				w, h = draw.textsize("lat: %f\nlng: %f" % (lat, lng), font=fnt2)
				da, db, x0, x1, y0, y1 = expand_a_b(a, b, w, h)
				draw.rectangle([x0, y0, x1, y1], fill='red')
				draw.multiline_text((a+da,b+db), "lat: %f\nlng: %f" % (lat, lng), fill='black', font=fnt2)
			im.save(filename)


