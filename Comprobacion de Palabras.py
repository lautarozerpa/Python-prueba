#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pattern.web import Wiktionary as wik
from pattern.es import verbs, tag, spelling, lexicon
import string
import json,os
import unicodedata

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s
def limpiarOracion(Oracion):
	sinacentos=elimina_tildes(Oracion)
	sacareditar=sinacentos.replace("[editar]","")
	sacarene=sacareditar.replace("\\n","")
	sacaretimologia=sacarene.replace("Etimologia","")
	return sacaretimologia

def BuscarEnWiki(palabra):
	engine=wik(language='es')
	#SELECCIONA LA PALABRA A BUSCAR
	article=engine.article(palabra)

	try:
		#BUSCA SI ES SUST,ADJ,VERB EN WIKI Y LO GUARDA EN tipowiki
		for section in article.sections:
			if ("SUSTANTIV") in(repr(section)).upper():
				tipowiki="Sustantivo"
				break
			elif("ADJETIV") in repr(section).upper():
				tipowiki="Adjetivo"
				break
			elif("VERB") in repr(section).upper():
				tipowiki="Verbo"
				break
				
	#EXCEPCION POR SI NO ENCUENTRA LA PALABRA
	except (TypeError, AttributeError):
		tipowiki=""
		print("La palabra no esta en Wiktionary")
	return tipowiki
	
def BuscarEnPattern(palabra):
	def clasificar(palabra):
		#if ("NN") in ( tag(palabra,tokenize=True, encoding='utf-8')):
		if((tag(palabra,tokenize=True, encoding='utf-8')[0][1])== "NN"):
			tipopattern="Sustantivo"
		elif((tag(palabra,tokenize=True, encoding='utf-8')[0][1])== "JJ"):
			tipopattern="Adjetivo"
		elif((tag(palabra,tokenize=True, encoding='utf-8')[0][1])== "VB"):
			tipopattern="Verbo"
		else:
			tipopattern=""
		return tipopattern
	if not palabra.lower() in verbs:
		if not palabra.lower() in spelling:
			if (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon)):
				print('La palabra no esta en pattern.es')
				tipopattern=""
			else:
				tipopattern=clasificar(palabra)
		else:
			tipopattern=clasificar(palabra)
	else:
		tipopattern=clasificar(palabra)
				
	print()
	return tipopattern

def BuscarDefinicionEnWiki(palabra):
	engine=wik(language='es')
	article=engine.article(palabra)
	for section in article.sections:
		if ("Etimolog") in repr(section):
			contenido=(repr(section.content))
	return limpiarOracion(contenido)


def GuardarDatos(palabra,tipo,definicion):
	datonuevo={}
	datonuevo.setdefault("Palabra",palabra)
	datonuevo.setdefault("Tipo",tipo)
	datonuevo.setdefault("Definicion",definicion)
	if os.path.isfile("Palabras.json"):  
		with open("Palabras.json", mode='r') as f: 
			data = json.loads(f.read())
		f.close()
		data.append(datonuevo)
		with open("Palabras.json",'w') as f:
			json.dump(data,f,indent=4)
	else:
		data=[datonuevo]
		with open("Palabras.json","w")as f:
			json.dump(data,f,indent=4)
			
def ReportePatternTipo(palabra,tipo):
	Log="La palabra " + palabra + " no se encuentra en pattern como un " + tipo
	f = open('LogPattern.txt','a')
	f.write('\n' + Log)
	f.close()

def ReportePatternYWiki(palabra):
	Log="La palabra " + palabra + " no se encuentra en pattern ni en wiktionary"
	f = open('LogPatternYWiki.txt','a')
	f.write('\n' + Log)
	f.close()

palabra="asfasd"
tipoWiki=BuscarEnWiki(palabra.lower())
tipoPattern=BuscarEnPattern(palabra)
if (tipoWiki!= ""):
	if(tipoPattern!=""):
		#Si wiki y pattern son iguales, se guarda
		if(tipoWiki==tipoPattern):
			definicion=BuscarDefinicionEnWiki(palabra.lower())
			GuardarDatos(palabra,tipoWiki,definicion)
		#Si wiki y pattern son distintas, se toma la de wiki y se hace reporte en pattern
		else:
			definicion=BuscarDefinicionEnWiki(palabra.lower())
			GuardarDatos(palabra,tipoWiki,definicion)
			ReportePatternTipo(palabra,tipoWiki)
	else:
		definicion=BuscarDefinicionEnWiki(palabra.lower())
		GuardarDatos(palabra,tipoWiki,definicion)
		ReportePatternTipo(palabra,tipoWiki)
elif(tipoPattern!=""): #Si no esta en wiki pero si esta en pattern se pide la definicion al profesor y se guarda
	definicion=input(print("Ingrese definicion de la palabra"))
	GuardarDatos(palabra,tipoPattern,definicion)
else:
	ReportePatternYWiki(palabra)

