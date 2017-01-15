#! /usr/bin/env python3

from subprocess import Popen
from subprocess import DEVNULL
from subprocess import PIPE
from time import sleep
from uuid import uuid1
from os import mkdir
from os.path import isfile
from os.path import splitext
from shutil import rmtree
from itertools import groupby
import cv2
import numpy
import sys
import re

MM2IN = 0.039370079
MM2BP = 2.834645688
PX2BP = 0.24
x_arr = []
y_arr = []

def BPs (ival):
  return str(ival*PX2BP)

def flatten (in_arr):
  try:
    for c in in_arr:
      if isinstance(c, (int, numpy.uint8, numpy.int32)):
        if not len(in_arr) == 2:
          return
        x_arr.append(in_arr[0])
        y_arr.append(in_arr[1])
        return
      else:
        flatten(c)
  except IndexError:
    return;

def getBorders(file_name):
  image = cv2.imread(file_name)
  height, width, channels = image.shape
  edged = cv2.Canny(image, 25, 150)

  cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
  flatten(cnts)
  x_arr1 = sorted(x_arr)
  y_arr1 = sorted(y_arr)
  x_graph = []
  x_max = 0
  y_graph = []
  y_max = 0
  for key, group in groupby(x_arr1):
    count = len(list(group))
    if count > x_max:
      x_max = count
    x_graph.append([key, count])
  for key, group in groupby(y_arr1):
    count = len(list(group))
    if count > y_max:
      y_max = count
    y_graph.append([key, count])
  x_result = []
  y_result = []
  for c in x_graph:
    if c[1] > (x_max*0.75):
      x_result.append(c[0])
  for c in y_graph:
    if c[1] > (y_max*0.75):
      y_result.append(c[0])
  return (min(x_result), height-max(y_result), max(x_result), height-min(y_result))

def cut_file(file_name):
  Popen(['pdftocairo', '-png', '-r', '300', file_name, file_name])
  sleep(1)
  borders = getBorders(file_name+'-1.png')
  print(BPs(borders[0]))
  print(BPs(borders[1]))
  print(BPs(borders[2]))
  print(BPs(borders[3]))
  print(file_name)
  Popen(["pdfcrop", "--bbox", BPs(borders[0])+" "+BPs(borders[1])+" "+BPs(borders[2])+" "+BPs(borders[3]), "--margins", "0", file_name, file_name+"-cropped.pdf"], stdout=DEVNULL)

def main(file_name):
  if not isfile(file_name):
    print("File '"+file_name+"' does not exist", file=sys.stderr)
    exit()
  filename, file_extension = splitext(file_name)
  if not ".pdf" == file_extension.lower():
    print ("File '"+file_name+"' ist not a pdf file", file=sys.stderr)
    exit()
  pdfinfo = Popen(['pdfinfo', file_name], stdout=PIPE)
  infostr = pdfinfo.stdout.read()
  regresult = re.search(r"pages:\s*([0-9]+)", str(infostr), flags=re.IGNORECASE)
  num_pages = int(regresult.group(1))
  print("This document ("+filename+") has %d pages" % num_pages)
  start_page = int(input("Enter first page of cut pattern: "))
  if start_page > num_pages:
    print("Start page is lager than num pages", file=sys.stderr)
    exit()


  tmpdir = "/tmp/cnv_"+str(uuid1())+"/"
  mkdir(tmpdir)

  Popen(['pdfseparate', '-f', str(start_page), file_name, tmpdir+'part_%d.pdf'])
  sleep(2)
  for x in range(start_page, num_pages+1):
    cut_file(tmpdir+'part_%d.pdf' % x)
  sleep(5)
  exit()
  rmtree(tmpdir)


if len(sys.argv) != 2:
  print("Please specify file!", file=sys.stderr)
  exit()
try:
  main(sys.argv[1])
except KeyboardInterrupt:
  pass
