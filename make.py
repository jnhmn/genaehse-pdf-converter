#! /usr/bin/env python3

from subprocess import call
from subprocess import Popen
from time import sleep

MM2IN = 0.039370079
MM2BP = 2.834645688

def BPs (ival):
  return str(ival*MM2BP)

file_name = input("Enter filename: ")

Popen(['pdfseparate', '-f', '2', file_name, 'part_%d.pdf'])

print("Tuning left Border")
print("Decimal mark is \".\"")

tmp_left = 6.5
tmp_bottom = 10.5
tmp_right = 202
tmp_top = 286
left = 1
bottom = 1
right = 50
top = 50

print("Example Values are 6.5 10.5 202 286")


while tmp_left != -1.0:
  left = tmp_left
  Popen(["pdfcrop", "--bbox", BPs(left)+" "+BPs(bottom)+" "+BPs(right)+" "+BPs(top), "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  try:
    tmp_left = float(input("Enter left margin: "))
  except ValueError:
    tmp_left = -1.0

while tmp_bottom != -1.0:
  bottom = tmp_bottom
  Popen(["pdfcrop", "--bbox", BPs(left)+" "+BPs(bottom)+" "+BPs(right)+" "+BPs(top), "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  try:
    tmp_bottom = float(input("Enter bottom margin: "))
  except ValueError:
    tmp_bottom = -1.0

while tmp_right != -1.0:
  right = tmp_right
  Popen(["pdfcrop", "--bbox", BPs(left)+" "+BPs(bottom)+" "+BPs(right)+" "+BPs(top), "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  try:
    tmp_right = float(input("Enter right position: "))
  except ValueError:
    tmp_right = -1.0

while tmp_top != -1.0:
  top = tmp_top
  Popen(["pdfcrop", "--bbox", BPs(left)+" "+BPs(bottom)+" "+BPs(right)+" "+BPs(top), "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  try:
    tmp_top = float(input("Enter top position: "))
  except ValueError:
    tmp_top = -1.0

rows = int(input("Please enter number of rows: "))
cols = int(input("Please enter number of columns: "))

file_names = []
num_files = int(rows)*int(cols)
start = rows + 1
while start >= 2:
  colcnt = 0
  offset = 0
  while colcnt < cols:
    file_id = start+offset
    tmp_file_name = "part_"+str(file_id)+".pdf"
    file_name = "cropped_"+str(file_id)+".pdf"
    Popen(["pdfcrop", "--bbox", BPs(left)+" "+BPs(bottom)+" "+BPs(right)+" "+BPs(top), "--margins", "0", tmp_file_name, file_name])
    file_names.append(file_name)
    offset += rows
    colcnt += 1
  start -= 1
print(file_names)
print("Sleeping for 10 secons")
sleep(10)

sizex = BPs((right - left) * cols)
sizey = BPs((top - bottom) * rows)

command = ['pdfnup', '--nup', str(cols)+'x'+str(rows), '--papersize', '{'+sizey+'bp, '+sizex+'bp}', '--outfile', 'comb.pdf']
Popen(command + file_names)
