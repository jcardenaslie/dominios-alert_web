import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time


def get_dominios(r):
	soup = BeautifulSoup(r.text, 'lxml')
	dominios = soup.find('table', {'class': 'tablabusqueda'}).findAll('div')
	strip_dominios = []
	for dom in dominios[::2]:
	    dom = dom.text
	    dom = dom.replace('\n', "")
	    dom = dom.replace('\t', "")
	    strip_dominios.append(dom)
	free_date = str(datetime.datetime.now()).split('.')[0]
	dominios = pd.DataFrame({'dominio':strip_dominios, 'free_date': free_date, 'last_check': None})
	return dominios

r = requests.get('https://www.nic.cl/registry/Eliminados.do?t=1d')

link = 'C://Users//joaquin//Desktop//Scrap Dominios//dominios_liberados.csv'
f_exists = True
try:
	lib_dom = pd.read_csv(link, index_col=0)
except:
	print('File does not exist')
	f_exists = False

if r.status_code == 200:
	dominios = get_dominios(r)
	if f_exists:
		lib_dom = lib_dom.append(dominios)
		lib_dom.to_csv(link)
	else:
		dominios.to_csv(link)
	print('Finish')
