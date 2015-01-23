# -*- coding: utf-8 -*-
from __future__ import print_function
import os, fnmatch
import zipfile
import sys
import re

os.chdir("./")

#PARTE GRAFICA	
from gi.repository import Gtk


class Handler:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def on_btnBuscar_clicked(self, button):
		self.resultado = builder.get_object("resultado").get_buffer()
		self.cal =  builder.get_object("calendar").get_date()
		self.server = builder.get_object("fileServidor").get_uri()
		self.out = builder.get_object("fileOut").get_uri()
		self.el_id = builder.get_object("txtID").get_text()
		self.progress = builder.get_object("progressbar1")
		self.progress.set_fraction(self.progress.get_fraction()+ 0.1)

		self.resultado.insert(self.resultado.get_end_iter(), builder.get_object("fileServidor").get_uri() + "\n")
		resultado = function1(self.server,self.cal,self.el_id,self.out)
		if resultado:
			self.resultado.insert(self.resultado.get_end_iter(), "Se encontro audio!\n" +resultado +"\n")
		else:
			self.resultado.insert(self.resultado.get_end_iter(),'No se encontro el Audio.'+"\n")
			self.progress.set_fraction(self.progress.get_fraction()+ 1)



def function1(direccion,fecha,el_id,salida):
	res = builder.get_object("resultado").get_buffer()
	res.insert(res.get_end_iter(), "Buscar en:\n"+str(direccion)[7:]+"\n")
	print(str(direccion)[7:])
	anio = str(fecha[0])
	mes = str(fecha[1] + 1)
	if len(mes) == 1:
		mes = str(0)+ str(fecha[1] + 1)
	
	dia = str(fecha[2])
	if len(dia) == 1:
		dia = str(0) + str(fecha[2])

	buscar= 'CAMP_*_'+anio+'_'+mes+'_'+dia+'*.zip'
	res.insert(res.get_end_iter(),"Cadena: " +buscar + "\n")
	print(buscar)
	archivos = find(buscar,str(direccion[7:]))
	barra(0.3)
	for archivo in archivos:

		res.insert(res.get_end_iter(), archivo +"\n")

		contenido = leeZip(archivo)
		index_match = findID(el_id, contenido)
		barra(0.6)
		if index_match:
			barra(0.9)
			print(archivo)
			try:
				data = zipfile.ZipFile(archivo).extract(contenido[index_match],str(salida)[7:])
				barra(1)
				return contenido[index_match]
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

def barra(cant):
	barra = builder.get_object("progressbar1")
	barra.set_fraction(cant)

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

window = builder.get_object("applicationwindow1")
window.show_all()

Gtk.main()
