#! /usr/bin/env python3

from subprocess import call
from subprocess import Popen
from time import sleep
import quantities
print("Enter Filenmae")
file_name = input()

Popen(['pdfseparate', '-f', '2', file_name, 'part_%d.pdf'])

print("Tuning left Border")
print("Decimal mark is \".\"")

tmp_left = "18.65"
tmp_bottom = "30.15"
tmp_right = "573.1"
tmp_top = "811.3"
left = "1"
bottom = "1"
right = "50"
top = "50"

print("Example Values are 18 30 575 815")


while tmp_left != '':
  left = tmp_left
  Popen(["pdfcrop", "--bbox", left+" "+bottom+" "+right+" "+top, "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  tmp_left = input("Enter left margin: ")

while tmp_bottom != '':
  bottom = tmp_bottom
  Popen(["pdfcrop", "--bbox", left+" "+bottom+" "+right+" "+top, "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  tmp_bottom = input("Enter bottom margin: ")

while tmp_right != '':
  right = tmp_right
  Popen(["pdfcrop", "--bbox", left+" "+bottom+" "+right+" "+top, "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  tmp_right = input("Enter right position: ")

while tmp_top != '':
  top = tmp_top
  Popen(["pdfcrop", "--bbox", left+" "+bottom+" "+right+" "+top, "--margins", "0", "part_2.pdf", "cropped_2.pdf"])
  sleep(0.5)
  print()
  tmp_top = input("Enter top position: ")

rows = input("Please enter number of rows: ")
cols = input("Please enter number of columns: ")

file_names = []
num_files = int(rows)*int(cols)
start = int(rows) + 1
while start >= 2:
  colcnt = 0
  offset = 0
  while colcnt < int(cols):
    file_id = start+offset
    tmp_file_name = "part_"+str(file_id)+".pdf"
    file_name = "cropped_"+str(file_id)+".pdf"
    Popen(["pdfcrop", "--bbox", left+" "+bottom+" "+right+" "+top, "--margins", "0", tmp_file_name, file_name])
    file_names.append(file_name)
    offset += int(rows)
    colcnt += 1
  start -= 1
print(file_names)
print("Sleeping for 10 secons")
sleep(10)

sizex = (float(right) - float(left)) * float(cols)
sizey = (float(top) - float(bottom)) * float(rows)

command = ['pdfnup', '--nup', str(cols)+'x'+str(rows), '--papersize', '{'+str(sizey)+'bp, '+str(sizex)+'bp}', '--outfile', 'comb.pdf']
Popen(command + file_names)
