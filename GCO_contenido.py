import argparse
from nltk.corpus import stopwords
# Gestion de los parametros de entrada
parser = argparse.ArgumentParser(description='Analisis de un sistema recomendador')
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

linea_fichero = args.file.readlines() # Devuelve un vector de strings
terminos = []
for i in linea_fichero:
    elemento = i.split()
    for j in elemento:
        j = j.replace(",","")
        j = j.replace(".","")
        j = j.lower()
        #print j
        terminos.append(j)

stop_words = []
f = open('stop-words_english_6_en.txt', 'r')
stop = f.readlines().decode("utf-8-sig").encode("utf-8")
stop_words = []
for i in stop:
    i = i.replace("\r\n", "")
    stop_words.append(i)

print stop_words


#print stop_words

for t in terminos:
    if t in stop_words:
        print "Elemento eliminado - " + str(t)




    



