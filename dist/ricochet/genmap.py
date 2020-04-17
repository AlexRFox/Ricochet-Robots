#! /usr/bin/env python

file = open ("first.map", 'w')

string = ""

for x in range (16):
    for y in range (16):
        string += str ((x, y))
        string += " 0 0 0 0"
        string += "\n"

file.write (string)
file.close ()
