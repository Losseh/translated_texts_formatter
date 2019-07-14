#!/usr/bin/python

import sys
import os
import os.path

name_key = "$name"
file_key = "$content"


def readfile(filename):
  f = open(filename, "r")
  content = f.readlines()
  f.close()
  return content


def read_translations(path, txt_files, orig_name):
    translations = {name: readfile(os.path.join(path[0], name)) for name in filter(lambda f: f != orig_name, txt_files)}
    result = map(lambda name: {name_key: name, file_key: translations[name]}, sorted(translations.keys()))
    return result


def format_normal(line):
  return line.replace("\n", "")


def format_translation(line):
  return "<i>" + format_normal(line) + "</i>"


def process_song(path):
  only_txts = filter(lambda x: "txt" in x, path[2])
  orig_name = "orig.txt"
  if orig_name in only_txts:
    # reading source file
    orig_path = os.path.join(path[0], orig_name)
    orig = readfile(orig_path)

    # transforming translation files
    translations = read_translations(path, only_txts, orig_name)

    # assert that every translation file has the same length as the source lyrics
    for translation in translations:
      len_f, len_orig = len(translation[file_key]), len(orig)
      file_name = str(translation[name_key])
      message = "Both files must have the same length in " + path[0] + ": orig.len=" + str(len_orig) + " != " + file_name + ".len=" + str(len_f)
      assert len_orig == len_f, message
  

    # generating the content
    content = ["<html>\n"]
    for i in range(len(orig)):
      formatted_orig = format_normal(orig[i])
      if formatted_orig == "":
        content.append("<br>\n")
      else:
        content.append(formatted_orig + "<br>\n")
        for translation in translations:
          content.append(format_translation(translation[file_key][i]) + "<br>\n")

        content.append("<br>\n")

    content.append("</html>")

    # writing the content to output file
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
