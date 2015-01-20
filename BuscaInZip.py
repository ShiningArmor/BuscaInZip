from __future__ import print_function
import os, fnmatch
import zipfile
import sys
import re

os.chdir("./")

def function1():

	direccion = str(sys.argv[1])

	if len(sys.argv) > 3:
		refZip=str(sys.argv[3])
	else: 
		refZip = ''

	el_id=str(sys.argv[2])
	buscar= '*'+refZip+'*.zip'
	print(buscar)
	archivos = find(buscar,direccion)
	for archivo in archivos:
		contenido = leeZip(archivo)
		index_match = findID(el_id, contenido)
		if index_match:
			print(archivo)
			try:
				data = zipfile.ZipFile(archivo).extract(contenido[index_match])
			except KeyError:
				print('ERROR: Did not find %s in zip file' % contenido[index_match])
			else:
				print(contenido[index_match], ':')
				print(repr(data))


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def leeZip(archivo):
	zz = zipfile.ZipFile(archivo)
	#zz.printdir()
	contenido = zz.namelist()
	zz.close()
	return contenido


def findID(el_id,contenido):
	for item in contenido:
		if re.search("(.*"+el_id+".*)", item):
			return contenido.index(item)		


if __name__ == "__main__":
	function1()
