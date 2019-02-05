#Created by Neil Marsden 2019
#This file is provided as is without warrenty of any kind
#Released under MIT license 

import random,sys,math,os,glob

try:
	from PIL import Image
except:
	print ("Opps - you need 'Pillow' try 'pip install pillow'")
	print ("Script will now exit")
	print
	sys.exit(0)



try:
	#https://github.com/rienafairefr/python-ldraw
	from ldraw.colour import *
	from ldraw.figure import *
	from ldraw.pieces import Group, Piece
except:
	print ("Opps - you need 'python-ldraw' try 'pip install pyldraw'")
	print ("Script will now exit")
	print
	sys.exit(0)

	
#From http://stackoverflow.com/questions/34366981/python-pil-finding-nearest-color-rounding-colors
def distance(c1, c2): # Work out the nearest colour 
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

def checkInput(nosOfFiles):
	userNumber = raw_input("Choose number? (q to quit) ")
	#print nosOfFiles,userNumber

	if userNumber == "q" or userNumber == "Q" or userNumber == "Quit":
		sys.exit()
	
	try:
		numberChosen = int(userNumber)
		#print "In the try statement ",numberChosen
		
		
		if numberChosen < 1 or numberChosen > nosOfFiles:
			if nosOfFiles == 1:
				print
				print "You need to choose '1'!"				
				userNumber = checkInput(nosOfFiles)
				numberChosen = int(userNumber)
				return numberChosen
			else:	
				print
				print "Opps that number is not between 1 and ", nosOfFiles
				userNumber = checkInput(nosOfFiles)	
		else:
			print "Good choice...",numberChosen	
			return numberChosen
	except:
		print
		print "Opps that's not a number"
		userNumber = checkInput(nosOfFiles)
		numberChosen = int(userNumber)
		return numberChosen


		
def getFile():
	pathName = os.path.dirname(os.path.abspath(__file__))
	# Find all the .bmps in the script folder...
	fileList=[] 
	nosOfFiles = 0
	for file in sorted(glob.glob( os.path.join(pathName, '*.bmp') )):
		fileName = os.path.basename(file)
		fileList.append(fileName)
		nosOfFiles=nosOfFiles + 1

	if nosOfFiles > 0:	
		#print (fileList)
		#print (nosOfFiles)
		print ("Enter the number of the file you want to make a mosiac of...")
		for fileName in fileList:
			indexNumber = fileList.index(fileName)
			print indexNumber+1, "-", fileName
		confirmedNumber = checkInput(nosOfFiles)
		#print confirmedNumber
		#raw_input()
		nameOfFile = fileList[int(confirmedNumber)-1]
	else:
		print ("Please add some .bmp images files to the script folder") 
		print ("Script will now quit...")
		print
		sys.exit()
	
	return (nameOfFile)	
	
#Open the image
print ("Looking for images...")
fileName = getFile()
print "You chose: ", fileName 
im = Image.open(fileName).convert('RGB')
#Get the pixel data
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
rgbPixels = im.load()

if width >= 256 or height >= 256:
	print ("Opps that files is big - your file needs to be less than 256 pixels in width and height")
	print ("Script will now exit")
	print
	sys.exit(0)
	

#print pixels #Used for checking

print ("Creating Lego...")
print "Width...", width, "  Height...", height
onexonexone = Group(Vector(0, 0, 0), Identity())

#Set up the LDraw file
mosaicFilename = fileName[:-4] + "_mosiac.ldr"
#LDrawFile = open('picture.ldr', 'w')
LDrawFile = open(mosaicFilename, 'w')
LDrawFile.write('0 // Mosaic Maker Colour - Neil Marsden'+'\n')

#Set Up the Lego Colour Dictionary
#rgb_code_dictionary = {(27,42,53):26, (242,243,243):1, (163,162,165):194}	
#(255, 217, 168):RED,(196, 0, 255):FLESH,(30, 0, 255):PURPLE
#rgb_code_dictionary = {(0,0,0):0, (87,87,87):8, (110,110,110):7, (190,190,190):503, (255,255,255):15} #GreyScaleOnly - Black,DarkGrey,Grey,LightGrey,White
rgb_code_dictionary = {(252, 252, 252): 15, (199, 200, 223): 20, (84, 163, 173): 11, (248, 227, 148): 18, (239, 203, 54):14, (153, 159, 155): 7, (87, 56, 39): 6, (198, 111, 158):5, (185, 230, 11): 27, (0, 84, 189): 1, (239, 111, 93): 12, (37, 121, 61): 2, (5, 19, 29): 0, (74, 157, 73): 10, (144, 56, 119): 26, (249, 149, 170): 13, (178,208, 224): 9, (128, 0, 122): 22, (113, 14, 15): 320, (167, 84, 0): 484, (0, 129, 141): 3, (199, 26, 9): 4, (108, 109, 91): 8, (192, 216, 182): 17, (225, 203, 156): 19, (32, 49, 174): 23,(100, 73, 61): 19,(86, 59, 43): 92,(116, 66, 4): 25}

#set start co-ordinates
x=0
y=-20
z=0
rot = 0
counter = 0
col = 0
#Work through each row of pixels in the image
for i,row in enumerate(pixels): 
	#print row
	for j,pixel in enumerate(row): # Then work through each pixel in the row
		#Get the  RGBA value (colour) of each pixel

		col = rgbPixels[j,i]
		#Check the pixel colour with the Lego dictionary colours
		point = col
		colors = list(rgb_code_dictionary.keys())
		closest_colors = sorted(colors, key=lambda color: distance(color, point))
		closest_color = closest_colors[0]
		code = rgb_code_dictionary[closest_color]
		
		
		#set the Lego colour to the colour code
		col = int(code)
		#Up the counter and increment the brick position
		
		counter += 1
		y += 20
		#Create a new row when the counter is greater than the width of the image
		if counter > width: 
			#print "new row"
			LDrawFile.write('0 // NEW ROW '+ str(x/20) + '\n')
			x += 20
			y = 0
			counter = 1
			
		#print i,j,x,y,col,code #Used for checking
		#Write the brick to the file
		#print "Wrting brick here..."
		LDrawFile.write(str(Piece(Colour(col), Vector(x, z, y), Identity().rotate(rot, YAxis), "3024", onexonexone))+'\n')

print	
print "Your mosiac file ", mosaicFilename, " is ready"	
