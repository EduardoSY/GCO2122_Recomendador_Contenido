import argparse
import collections
import math
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
f = open('stopwords_english_fixed.txt', 'r')

#f = open('stop-words_english_6_en.txt', 'r')
#data = f.read().decode("utf-8-sig").encode("utf-8")
#stop_words = data
stop_words = f.read()
f.close()

#print stop_words
#print terminos
for t in range(len(terminos)):
    print terminos[t]
    for i in range(len(terminos[t])):
         print "Elemento analizado - " + str(terminos[t][i])
         if terminos[t][i] in stop_words:
            print "***Elemento eliminado - " + str(terminos[t][i])
            terminos[t][i] = "-"

for l in range(len(terminos)):
    terminos[l] = [i for i in terminos[l] if i != "-"]


print
print terminos

#print terminos


terminos_unicos = []
for doc_list in terminos:
    for elemento in doc_list:
        if elemento not in terminos_unicos:
            terminos_unicos.append(elemento)

#print "------------------"
print (len(terminos_unicos))

matriz_tf = [ [ [0,0,0] for y in range(len(terminos_unicos)) ] for x in range( len(terminos)) ] #Primero pongo col, luego filas

def show_matriz(matrix, pos):
    for i in range(len(matrix)):
        aux_fila = "[" + str(i) + "] ->  "
        for j in range(len(matrix[i])):
            aux_fila += "{:.2f}".format(matrix[i][j][pos])
            aux_fila += "\t\t"
        print (aux_fila)


def show_matriz_sim(matrix):
    for i in range(len(matrix)):
        aux_fila = "[" + str(i) + "] ->  "
        for j in range(len(matrix[i])):
            aux_fila += "{:.2f}".format(matrix[i][j])
            aux_fila += "\t\t"
        print (aux_fila)

show_matriz(matriz_tf, 0)

def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count

print terminos_unicos
for doc in range(len(terminos)):
    recuento = CountFrequency(terminos[doc])
    for k,v in recuento.items():
        matriz_tf[doc][terminos_unicos.index(k)][0] = v


def calc_IDF():
    N = len(matriz_tf)
    for i in range(len(matriz_tf)):
        for j in range(len(matriz_tf[i])):
            docs_aparece = 0
            for cont in range(len(matriz_tf)):
                if (matriz_tf[cont][j][0] != 0):
                    docs_aparece += 1
            valor = math.log((N/ float(docs_aparece)),10)
            matriz_tf[i][j][1] = valor

def calc_TF_IDF():
    for i in range(len(matriz_tf)):
        for j in range(len(matriz_tf[i])):
            matriz_tf[i][j][2] =  matriz_tf[i][j][0] *  matriz_tf[i][j][1]

matriz_sim = [ [ 0 for y in range(len(terminos)) ] for x in range(len(terminos)) ] #Primero pongo col, luego filas

def calc_sim_cos(doc1, doc2):
    parte_superior = 0
    parte_inferior_izquierda = 0
    parte_inferior_derecha = 0
    for i in range(len(terminos_unicos)):
       parte_superior += matriz_tf[doc1][i][2] * matriz_tf[doc2][i][2]
       parte_inferior_izquierda += pow(matriz_tf[doc1][i][2],2)
       parte_inferior_derecha += pow(matriz_tf[doc2][i][2],2)
    denominador = math.sqrt(parte_inferior_derecha) * math.sqrt(parte_inferior_izquierda)
    return (parte_superior/float(denominador))

def fill_matriz_sim():
    for i in range(len(matriz_sim)):
        for j in range(len(matriz_sim[i])):
            matriz_sim[i][j] = calc_sim_cos(i,j)

print
show_matriz(matriz_tf,0)
calc_IDF()
print
show_matriz(matriz_tf,1)
calc_TF_IDF()
print "-- MATRIZ VALORES TF-IDF"
show_matriz(matriz_tf,2)

fill_matriz_sim()
print "+++ SIMILITUD +++"
show_matriz_sim(matriz_sim)

#Hasta aqui borrados los stopwords