#!/usr/bin/python

import sys
import os


def readfile(filename):
  f = open(filename, "r")
  content = f.readlines()
  f.close()
  return content


def format_normal(line):
  return line.replace("\n", "")


def format_translation(line):
  return "<i>" + format_normal(line) + "</i>"


def process_song(path):
  if path[2] == ["orig.txt", "eng.txt"]:
    file1 = readfile(path[0] + "/orig.txt")
    file2 = readfile(path[0] + "/eng.txt")

    assert len(file1) == len(file2), "Both files must have the same length " + path
  
    content = ["<html>\n"]
 
    for i in range(len(file1)):
      content.append(format_normal(file1[i]) + "<br>\n")
      content.append(format_translation(file2[i]) + "<br>\n")
      content.append("<br>\n")

    content.append("</html>")

    outputname = path[0] + ".html"
    print "writing to " + outputname
    output = open(outputname, "w+")
    output.write("".join(content))
    output.close()

    return outputname
  else:
    return None


def process_songs():
  created_files = []

  for path in os.walk("."):
    created_file = process_song(path)
    if created_file is not None:
      created_files.append(created_file)

  created_files.sort()
  return created_files


def create_index(paths):
  content = ["<html>\n"]

  for path in paths:
    path1 = path.replace("./", "")
    name = path1.replace(".html", "")
    content.append("<a href=\"" + path1 + "\">" + name + "</a><br>\n")

  content.append("</html>")

  output = open("index.html", "w+")
  output.write("".join(content))
  output.close()

songs = process_songs()
create_index(songs)
