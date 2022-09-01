#!/usr/bin/python
# Mateus Seenem Tavares

import argparse
import random
import time

# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-s", "--sizeof", required=False, 
                        help="side of a square to walk")
all_args.add_argument("-a", "--ants", required=False, 
                        help="How many ants?")
all_args.add_argument("-i", "--items", required=False, 
                        help="How many items?")
args = vars(all_args.parse_args())

sizeof = 50
if args['sizeof']: 
  sizeof = args['sizeof']
  print("The size of the matrix is {}x{}".format(sizeof, sizeof))
else:
  print("No size was given (-s Number), using {}x{}".format(sizeof, sizeof))

ants = 10
if args['ants']: 
  ants = args['ants']
  print("There is {} ants in the matrix".format(ants))
else:
  print("No ants was given (-a Number), using {}".format(ants))

items = 100
if args['items']: 
  items = args['items']
  print("There is {} items in the matrix".format(items))
else:
  print("No number of items was given (-i Number), using {}".format(items))

##########################

t = time.time()
freeHandsCounter = 0
canWrite = 1
loops = 10000000
radius = 1
groupingFactor =  0.3 # radius 1
groupingFactor =  0.08 # radius 5
symbItem = '.'
symbAnt = '8'
symbEmptyCell = ' '
symbAntGot = '&'
windsRose = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
#             0    1     2    3     4    5     6    7     8

matrix = [' '] * sizeof
for x in range(sizeof):
  matrix[x] = [' '] * sizeof

antsArray = [0] * ants
for x in range(ants):
  antsArray[x] = [0] * 4

itemsArray = [0] * items
for x in range(items):
  itemsArray[x] = [0] * 4


######################

def write_to_file_sync(nameFile, loop, message):
  
  f = open(nameFile, "w+", encoding='utf-8')

  f.write("# {}\n".format(message))

  f.write("# Ants = {}   Matrix = {}x{}\n# Time = {} seconds\n# Loops without carrying something = {}\n# Loops Limit = {} Loop = {}\n".format(ants,sizeof,sizeof, round((time.time() - t)), freeHandsCounter,loops,loop))
  
  for x in range(sizeof):
    for y in range(sizeof):
      f.write("{}".format(matrix[x][y]))
    f.write('\n')
  f.close()

def look(i, j, radius):
  item = 0
  cells = 0

  for a in range(2*radius+1):
    for b in range(2*radius+1):
      if (i+radius)-a >= 0 and (j+radius)-b >= 0:
        if (i+radius)-a < sizeof and (j+radius)-b < sizeof:
          cells += 1
          if matrix[(i+radius)-a][(j+radius)-b] == symbItem:
            item += 1
  
  return item, cells

def walk(a):
  
  x = a[0]
  y = a[1]
  if a[2] == 0:
    a[2] = "S"
  a[3] = a[2]

  while(True):
    while(True):

      direction = random.randint(0,4)
      d = windsRose[(direction + windsRose.index(a[2]) + 2) % len(windsRose)]

      #going N
      if d == "N": 
        if a[0]-1 < 0: 
          continue
        else: 
          x = a[0]
          x -= 1 
          y = a[1]
          break

      #going NE
      elif d == "NE": 
        if a[0]-1 < 0 or a[1]+1 >= sizeof: 
          continue
        else: 
          x = a[0]
          x -= 1
          y = a[1]
          y += 1 
          break

      #going E
      elif d == "E":
        if a[1]+1 >= sizeof: 
          continue
        else: 
          x = a[0]
          y = a[1]
          y += 1 
          break

      #going SE
      elif d == "SE":
        if a[0]+1 >= sizeof or a[1]+1 >= sizeof: 
          continue
        else: 
          x = a[0]
          x += 1
          y = a[1]
          y += 1
          break

      #going S
      elif d == "S":
        if a[0]+1 >= sizeof: 
          continue
        else: 
          x = a[0]
          x += 1
          y = a[1]
          break

      #going SW
      elif d == "SW":
        if a[0]+1 >= sizeof or a[1]-1 < 0: 
          continue
        else: 
          x = a[0]
          x += 1
          y = a[1]
          y -= 1
          break

      #going W
      elif d == "W":
        if a[1]-1 < 0: 
          continue
        else: 
          x = a[0]
          y = a[1]
          y -= 1
          break

      #going NW
      elif d == "NW":
        if a[0]-1 < 0 or a[1]-1 < 0: 
          continue
        else: 
          x = a[0]
          x -= 1
          y = a[1]
          y -= 1
          break
    

    #will walk
    if x != a[0] or y != a[1]:
      #if i'm going into another Ant...think again
      if matrix[x][y] not in ['8', '.8', '&', '.&']:
        break

  if x != a[0] or y != a[1]:
    #where i'm going there is a item
    if matrix[x][y] == symbItem: 
      if matrix[a[0]][a[1]] == symbAnt:
        matrix[x][y] = symbItem + symbAnt #I didn't take it yet
        matrix[a[0]][a[1]] = symbEmptyCell
      
      elif matrix[a[0]][a[1]] == symbAntGot:
        matrix[x][y] = symbItem + symbAntGot
        matrix[a[0]][a[1]] = symbEmptyCell
      
      elif matrix[a[0]][a[1]] == symbItem + symbAnt:
        matrix[x][y] = symbItem + symbAnt
        matrix[a[0]][a[1]] = symbItem

      elif matrix[a[0]][a[1]] == symbItem + symbAntGot:
        matrix[x][y] = symbItem + symbAntGot
        matrix[a[0]][a[1]] = symbItem
    
    #it's a empty cell
    elif matrix[x][y] == symbEmptyCell:
      
      if matrix[a[0]][a[1]] == symbAnt:
        matrix[x][y] = symbAnt
        matrix[a[0]][a[1]] = symbEmptyCell

      elif matrix[a[0]][a[1]] == symbAntGot:
        matrix[x][y] = symbAntGot
        matrix[a[0]][a[1]] = symbEmptyCell

      elif matrix[a[0]][a[1]] == symbItem + symbAnt:
        matrix[x][y] = symbAnt
        matrix[a[0]][a[1]] = symbItem

      elif matrix[a[0]][a[1]] == symbItem + symbAntGot:
        matrix[x][y] = symbAntGot
        matrix[a[0]][a[1]] = symbItem

  #a[0] = x
  #a[1] = y
  #a[2] = d
    return x, y, d
  

def FreeHandsEnd(loop):
  write_to_file_sync("matrix.out", loop, "Ended by too much time without an Ant carrying something")
  
  for i in range(ants):
    if matrix[antsArray[i][0]][antsArray[i][1]] == symbAnt:
      matrix[antsArray[i][0]][antsArray[i][1]] = symbEmptyCell
    elif len(matrix[antsArray[i][0]][antsArray[i][1]]) == 2:
      matrix[antsArray[i][0]][antsArray[i][1]] = matrix[antsArray[i][0]][antsArray[i][1]][0]
  
  write_to_file_sync("matrix-final.out", loop, "Ended by too much time without an Ant carrying something")

###################

cellVisited = 0
while cellVisited != items:
  x = random.randrange(0, sizeof)
  y = random.randrange(0, sizeof)
  if matrix[x][y] == symbEmptyCell:
    cellVisited += 1
    matrix[x][y] = symbItem

cellVisited = 0
while cellVisited < ants:
  x = random.randrange(0,sizeof)
  y = random.randrange(0,sizeof)
  if matrix[x][y] == symbEmptyCell:
    antsArray[cellVisited][0] = x
    antsArray[cellVisited][1] = y
    matrix[x][y] = symbAnt
    cellVisited += 1

write_to_file_sync("matrix.in", 0, "Initial matrix")

for loop in range(loops):  

  if canWrite > 2000:
    write_to_file_sync("matrix.out", loop, "Running matrix")
    canWrite = 0

  if freeHandsCounter > 400:
    FreeHandsEnd(loop)
    break

  freeHandsCounter += 1
  canWrite += 1

  for i in range(ants):
    a = antsArray[i]
    x = a[0]
    y = a[1] 
    item, cells = look(x, y, radius)

    if matrix[a[0]][a[1]] == symbEmptyCell:
      print("We lost an Ant, look at walk function")

    if matrix[a[0]][a[1]] == symbAntGot:
      freeHandsCounter = 0

    # ant with free hands
    if matrix[x][y] == symbItem + symbAnt:
      if item/cells < groupingFactor:
        matrix[x][y] = symbAntGot # got an item
        
        a[0], a[1], a[2] = walk(a)
      else: a[0], a[1], a[2] = walk(a)
    
    elif matrix[x][y] == symbAnt: a[0], a[1], a[2] = walk(a) # search more

    # ant holding a data
    elif matrix[x][y] == symbAntGot:
      if item/cells > groupingFactor:
        matrix[x][y] = symbItem + symbAnt # release item
        a[0], a[1], a[2] = walk(a)
      else: a[0], a[1], a[2] = walk(a)

    elif matrix[x][y] == symbItem + symbAntGot: a[0], a[1], a[2] = walk(a) # full cell, go to another
    
else:
  write_to_file_sync("matrix-final.out", loops, "Ended by reaching the limit of loops")