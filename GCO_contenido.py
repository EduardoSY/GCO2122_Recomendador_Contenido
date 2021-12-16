import argparse
import collections
# Gestion de los parametros de entrada
parser = argparse.ArgumentParser(description='Analisis de un sistema recomendador')
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

linea_fichero = args.file.readlines() # Devuelve un vector de strings

terminos = []
for i in linea_fichero:
    doc = []
    elemento = i.split()
    for j in elemento:
        j = j.replace(",","")
        j = j.replace(".","")
        j = j.lower()
        doc.append(j)
    terminos.append(doc)

stop_words = []
#f = open('stopwords_english_fixed.txt', 'r')

f = open('stop-words_english_6_en.txt', 'r')
data = f.read().decode("utf-8-sig").encode("utf-8")
stop_words = data
#stop_words = f.read()
f.close()

#print stop_words
#print terminos
for t in terminos:
    for i in t:
         if i in stop_words:
            #print "Elemento eliminado - " + str(t)
            t.remove(i)

#print terminos


terminos_unicos = []
for doc_list in terminos:
    for elemento in doc_list:
        if elemento not in terminos_unicos:
            terminos_unicos.append(elemento)

#print "------------------"
print (len(terminos_unicos))

matriz_tf = [ [ 0 for y in range(len(terminos_unicos)) ] for x in range( len(terminos)) ] #Primero pongo col, luego filas

def show_matriz(matrix):
    for i in range(len(matrix)):
        aux_fila = "[" + str(i) + "] ->  "
        for j in range(len(matrix[i])):
            aux_fila += "{:.2f}".format(matrix[i][j])
            aux_fila += "\t\t"
        print (aux_fila)

show_matriz(matriz_tf)

def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count

for doc in range(len(terminos)):
    recuento = CountFrequency(terminos[doc])
    for k,v in recuento.items():
        matriz_tf[doc][terminos_unicos.index(k)] = v

print
show_matriz(matriz_tf)


#Hasta aqui borrados los stopwords