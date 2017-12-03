import urllib2, StringIO

from PIL import Image
from os import system

black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
green = (170, 255, 170, 255)
purple = (170, 170, 255, 255)
red = (255, 170, 170, 255)
red_purple = (170, 85, 170, 255)
green_purple = (85, 170, 170, 255)
red_green = (170, 170, 85, 255)

def is_purple(color):
    if color == white or color == green or color == red:
        return False
    if ((color[2] == 170 or color[2] == 255) and color[3] == 255):
        return True
    if color == red_purple or color == green_purple:
        return True
    return False
def is_red(color):
    if color == white or color == green or color == purple:
        return False
    if (color[0] == 170 or color[0] == 255) and color[3] == 255:
        return True
    if color == red_purple or color == red_green:
        return True
    return False
def is_green(color):
    if color == white or color == purple or color == red:
        return False
    if (color[1] == 170 or color[1] == 255) and color[3] == 255:
        return True
    if color == green_purple or color == red_green:
        return True
    return False

def save_image(image,path):
	img = Image.open(image)
	img.save(path)
	return img

def show_image(image):
	img = Image.open(image)
	im = img.load()
	width, height = img.size

	output = ''
	for y in range(0,height,5):
		col = ''
		for x in range(0,width,2):
			if im[x,y] == white:
				col += ' '
			else:
				col += 'X'
		if col.find('X')<0:
			continue
		output += col + '\n'

	print output.rstrip()

def nw_vertical(x,img):
	width, height = img.size
	im = img.load()

	for i in range(height):
		if im[x,i]==black:
			return False
	return True

def extract_number(url):
	layer = []
	system('rm -rf ./data/nums/*')
	
	image = StringIO.StringIO(urllib2.urlopen(url).read()) # save original png
	save_image(image,'./data/ori.png')

	for f in (is_red,is_green,is_purple): # extract layer
		img = Image.open(image)
		im = img.load()
		width, height = img.size
		for x in range(width):
			for y in range(height):
				if f(im[x,y]):
					im[x,y] = black
				else:
					im[x,y] = white
		layer.append(img)

	for l in layer:						 # extract number
		width, height = l.size
		x = 0

		while x<width:
			if not nw_vertical(x,l):
				begin_x = x
				for x2 in xrange(x+1,width):
					if nw_vertical(x2,l):
						end_x = x2
						break
				if end_x - begin_x < 15:
					x = end_x
					continue
				crop_img = l.crop((begin_x,0,end_x,height))
				crop_img.save('./data/nums/{0}.png'.format(begin_x))
				x = end_x
			x += 1
