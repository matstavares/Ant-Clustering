#!/usr/bin/python
# Mateus Seenem Tavares

import argparse
from cmath import inf
import random
import asyncio
import time
import math

# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-s", "--sizeof", required=False, 
                        help="side of a square to walk")
all_args.add_argument("-a", "--ants", required=False, 
                        help="How many ants?")
all_args.add_argument("-d", "--data", required=False, 
                        help="File name to read")                        
all_args.add_argument("-i", "--itens", required=False, 
                        help="How many itens?")
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

file = "Square1-DataSet-400itens.txt"
# file = "R15.txt"
if args['data']: 
  file = args['data']
  print("Reading from {}".format(file))
else:
  print("No file was given to read, using {}".format(file))

##########################

matrix = [' '] * sizeof
for x in range(sizeof):
  matrix[x] = [' '] * sizeof

antsArray = [0] * ants
for x in range(ants):
  antsArray[x] = [0] * 4

t = time.time()
loops = 100000000
radius = 1
k1 =  0.2
k2 = 0.1
avgDistanceFactor = 1      # dynamically corrected
# avgDistanceFactor = 6.5  # for the 15 group dataset
# avgDistanceFactor = 35.5 # for the 4 group dataset
distanceAVG = [0, 0]       # correcting avgDistanceFactor
freeHandsCounter = 0
canWrite = 0
ending = 0
symbItem = '.'
symbAnt = '£'
symbEmptyCell = ' '
symbAntGot = '&'
windsRose = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
#             0    1     2    3     4    5     6    7     8

######################

def write_to_file_sync(nameFile, loop, message):
  
  f = open(nameFile, "w+", encoding='utf-8')

  f.write("# {}\n".format(message))

  f.write("# Ants = {}   Matrix = {}x{}\n# Time = {} minutes\n# Loops without carrying something = {}\n# Loops Limit = {} Loop = {}\n".format(ants,sizeof,sizeof, round((time.time() - t)/60), freeHandsCounter,loops,loop))
  
  for x in range(sizeof):
    for y in range(sizeof):
    
      if len(matrix[x][y][0]) > 1:
        f.write("{}".format(matrix[x][y][0][2]))
      else:
        f.write("{}".format(matrix[x][y]))

    f.write('\n')
  f.close()

async def write_to_file(nameFile, matrix, loop):
  f = open(nameFile, "w+", encoding='utf-8')
  
  f.write("# Running matrix\n")

  f.write("# Ants = {}   Matrix = {}x{}\n# Time = {} minutes  k1 = {} k2 ={}\n# Loops without carrying something = {}\n# Loops Limit = {} Loop = {}\n".format(ants,sizeof,sizeof, round((time.time() - t)/60), k1,k2,freeHandsCounter,loops, loop))
  
  for x in range(sizeof):
    for y in range(sizeof):
    
      if len(matrix[x][y][0]) > 1:
        f.write("{}".format(matrix[x][y][0][2]))
      else:
        f.write("{}".format(matrix[x][y]))
    
    f.write('\n')
  f.close()

def lookData(i, j, raio):
  item = 0
  cells = 0
  distance = []
  
  centerI = float(matrix[i][j][0][0])
  centerJ = float(matrix[i][j][0][1])

  for a in range(2*raio+1):
    for b in range(2*raio+1):
      if (i+raio)-a >= 0 and (j+raio)-b >= 0:
        if (i+raio)-a < sizeof and (j+raio)-b < sizeof:
          if (i+raio)-a != i or (j+raio)-b != j:
            cells += 1
            if (matrix[(i+raio)-a][(j+raio)-b] != symbEmptyCell and
                matrix[(i+raio)-a][(j+raio)-b] != symbAnt):
              if len(matrix[(i+raio)-a][(j+raio)-b]) > 1:
                dataI = float(matrix[(i+raio)-a][(j+raio)-b][0][0])
                dataJ = float(matrix[(i+raio)-a][(j+raio)-b][0][1])
              else:
                dataI = float(matrix[(i+raio)-a][(j+raio)-b][0][0])
                dataJ = float(matrix[(i+raio)-a][(j+raio)-b][0][1])
            
              distance.append([(i+raio)-a, (j+raio)-b, math.sqrt(
                              (centerI - dataI) ** 2 + 
                              (centerJ - dataJ) ** 2)])
              item += 1

  return item, cells, distance

def fi (i, j, raio):
  item, cells, distance = lookData(int(i), int(j), int(raio))
  
  sum = 0
  for d in distance:
    distanceAVG[0] += d[2]
    distanceAVG[1] += 1
    j = 1-(d[2]/avgDistanceFactor)
    sum += j

  # if (item ** 2) != 0:
  #   fi = sum/(item ** 2)
  #   avgCellItem = ((cells**2)+(item**2))/2
  #   fi =  sum/(avgCellItem ** 2)
  # else:    
  fi =  sum/(cells ** 2)

  # It doesn't happen, but...
  if fi > 1:
    return 1
  elif fi > 0:
    return fi
  else:
    return 0

def pp(i, j, raio):
  p = (k1 / (k1 + fi(i, j, raio))) ** 2
  # It doesn't happen, but...
  if p > 1:
    return 1
  return p

def pd(i, j, raio):
  fxi = fi(i, j, raio)
  p = (fxi / (k2 + fxi)) ** 2
  # It doesn't happen, but...
  if p > 1:
    return 1
  return p
  
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
      if not(len(matrix[x][y]) > 1 or matrix[x][y] == symbAnt):
        break

  if x != a[0] or y != a[1]:
    # syntactic sugar for better interpretation
    # itemLocal and itemGot are mostly in the same matrix's field
    if len(matrix[a[0]][a[1]]) == 2:
      if matrix[a[0]][a[1]][1] == symbAntGot:
        itemGot = matrix[a[0]][a[1]][0]
      else:  
        itemLocal = matrix[a[0]][a[1]][0]

    if len(matrix[a[0]][a[1]]) == 3:
      itemGot = matrix[a[0]][a[1]][1]
      itemLocal = matrix[a[0]][a[1]][0]


    #where i'm going there is a item
    if matrix[x][y] != symbEmptyCell: 
      if matrix[a[0]][a[1]] == symbAnt:
        matrix[x][y] = [matrix[x][y][0], symbAnt] #I didn't take it yet
        matrix[a[0]][a[1]] = symbEmptyCell
      
      elif len(matrix[a[0]][a[1]]) == 2:
        if matrix[a[0]][a[1]][1] == symbAntGot:
          matrix[x][y] = [matrix[x][y][0], itemGot, symbAntGot]
          matrix[a[0]][a[1]] = symbEmptyCell
      
        elif matrix[a[0]][a[1]][1] == symbAnt:
          matrix[x][y] = [matrix[x][y][0], symbAnt]
          matrix[a[0]][a[1]] = [itemLocal]

      elif len(matrix[a[0]][a[1]]) == 3:
        matrix[x][y] = [matrix[x][y][0], itemGot, symbAntGot]
        matrix[a[0]][a[1]] = [itemLocal]
    
    #it's a empty cell
    elif matrix[x][y] == symbEmptyCell:
      
      if matrix[a[0]][a[1]] == symbAnt:
        matrix[x][y] = symbAnt
        matrix[a[0]][a[1]] = symbEmptyCell

      elif len(matrix[a[0]][a[1]]) == 2:
        if matrix[a[0]][a[1]][1] == symbAntGot:
          matrix[x][y] = [itemGot, symbAntGot]
          matrix[a[0]][a[1]] = symbEmptyCell

        elif matrix[a[0]][a[1]][1] == symbAnt:
          matrix[x][y] = symbAnt
          matrix[a[0]][a[1]] = [itemLocal]

      elif len(matrix[a[0]][a[1]]) == 3:
        matrix[x][y] = [itemGot, symbAntGot]
        matrix[a[0]][a[1]] = [itemLocal]

  #a[0] = x
  #a[1] = y
  #a[2] = d
    return x, y, d
  
def feed_matrix_from_file():
  f = open(file, "r+", encoding='utf-8')

  itensList = [0] * 3
  cellVisited = 0
  data = 0

  while True:
    x = random.randrange(0, sizeof)
    y = random.randrange(0, sizeof)
    if matrix[x][y] == symbEmptyCell:
      line = f.readline()

      if not line:
        break
      
      if line in ['\t\n', '\n']:
        continue

      if not line.startswith('#'):
        line = line.replace('\t', ' ')
        line = line.replace(',', '.')
        itensList = line.split()
        matrix[x][y] = [itensList]
        data += 1

def feed_ants_to_matrix():
  cellVisited = 0
  while cellVisited < ants:
    x = random.randrange(0,sizeof)
    y = random.randrange(0,sizeof)
    if matrix[x][y] == symbEmptyCell:
      antsArray[cellVisited][0] = x
      antsArray[cellVisited][1] = y
      matrix[x][y] = symbAnt
      cellVisited += 1

def FreeHandsEnd(loop):
  write_to_file_sync("matrix.out", loop, "Ended by too much time without an Ant carrying something")
  
  #removing ants
  for i in range(ants):
    if matrix[antsArray[i][0]][antsArray[i][1]] == symbAnt:
      matrix[antsArray[i][0]][antsArray[i][1]] = symbEmptyCell
    elif len(matrix[antsArray[i][0]][antsArray[i][1]]) == 2:
      matrix[antsArray[i][0]][antsArray[i][1]] = matrix[antsArray[i][0]][antsArray[i][1]][0]
  
  write_to_file_sync("matrix-final.out", loop, "Ended by too much time without an Ant carrying something")

###################

feed_matrix_from_file()
feed_ants_to_matrix()

# stop all to write the initial matrix
write_to_file_sync("matrix.in", 0, "Initial matrix")

for loop in range(loops):  

  if freeHandsCounter > 600:
    FreeHandsEnd(loop)
    break

  if canWrite > 50000:
    try:
      # getting to know the data, wasting some iterations
      asyncio.run(write_to_file("matrix.out", matrix, loop))
    except Exception:
      pass
    avgDistanceFactor = distanceAVG[0]/distanceAVG[1]
    canWrite = 0

  if loop + 100000 > loops:
    ending = 1

  freeHandsCounter += 1
  canWrite += 1

  # randomly getting an Ant
  i = random.randrange(0,ants)
  a = antsArray[i]
  x = a[0]
  y = a[1] 

  if matrix[x][y] == symbAnt: # nothing to think here
    a[0], a[1], a[2] = walk(a) 
  
  elif len(matrix[x][y]) == 2:

    # ant with free hands
    if matrix[x][y][1] == symbAnt:
      if random.random() < pp(x, y, radius):
        if not ending:
          matrix[x][y] = [matrix[x][y][0], symbAntGot] # got a data
          freeHandsCounter = 0
        a[0], a[1], a[2] = walk(a)
      else: a[0], a[1], a[2] = walk(a)
  
    # ant holding a data
    elif matrix[x][y][1] == symbAntGot:
      freeHandsCounter = 0
      if  random.random() < pd(x, y, radius):
        matrix[x][y] = [matrix[x][y][0], symbAnt] # dropped the data
        a[0], a[1], a[2] = walk(a)
      else: a[0], a[1], a[2] = walk(a)

  elif len(matrix[x][y]) == 3: 
    freeHandsCounter = 0
    a[0], a[1], a[2] = walk(a) # full cell GET OUT OF HERE

else:
  write_to_file_sync("matrix-final.out", loops, "Ended by reaching the limit of loops")