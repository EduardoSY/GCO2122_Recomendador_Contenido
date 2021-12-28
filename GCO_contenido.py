# Recomendador basado en contenido
# - Eduardo Da Silva Yanes

import argparse
import collections
import math
import sys

# Gestion de los parametros de entrada
parser = argparse.ArgumentParser(description='Analisis de un sistema recomendador')
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'))
args = parser.parse_args()

original_stdout = sys.stdout

if args.outfile is None:
    print "Mostrar en Pantalla"
else:
    sys.stdout = args.outfile



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

# Analizar palabras y descartar stopwords
for t in range(len(terminos)):
    #print terminos[t]
    for i in range(len(terminos[t])):
         #print "Elemento analizado - " + str(terminos[t][i])
         if terminos[t][i] in stop_words:
            #print "***Elemento eliminado - " + str(terminos[t][i])
            terminos[t][i] = "-"
# Anadir elementos que no son - (palabra eliminada)
for l in range(len(terminos)):
    terminos[l] = [i for i in terminos[l] if i != "-"]

# Palabras analizadas (sin repetirse)
terminos_unicos = []
for doc_list in terminos:
    for elemento in doc_list:
        if elemento not in terminos_unicos:
            terminos_unicos.append(elemento)

# Matriz de terminos donde se almacenan los valores [TF, IDF, TF-IDF]
matriz_terminos = [ [ [0,0,0] for y in range(len(terminos_unicos)) ] for x in range( len(terminos)) ] #Primero pongo col, luego filas

def show_matriz(matrix, pos):
    for i in range(len(matrix)):
        aux_fila = "[" + str(i) + "] ->  "
        for j in range(len(matrix[i])):
            aux_fila += "{:.2f}".format(matrix[i][j][pos])
            aux_fila += "\t\t"
        print (aux_fila)


def show_matriz_sim(matrix):
    print "\n### SIMILITUD ENTRE DOCUMENTOS ###\n"
    cabecera = '{:<11}'.format(" ")
    for i in range(len(matrix)):
        index = "[D." + str(i) + "]"
        aux = '{:<9}'.format(index)
        cabecera += aux
    print cabecera
    
    for i in range(len(matrix)):
        output = ""
        aux_fila = "[Doc " + str(i) + "] ->"
        aux = '{:<11}'.format(aux_fila)
        output += aux
        for j in range(len(matrix[i])):
            aux_numero = "{:.3f}".format(matrix[i][j])
            aux_num = '{:<9}'.format(aux_numero)
            output += aux_num
        print (output)

# Contar cantidad de veces que aparece la palabra
def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count


# Rellenar la matriz con TF
for doc in range(len(terminos)):
    recuento = CountFrequency(terminos[doc])
    for k,v in recuento.items():
        matriz_terminos[doc][terminos_unicos.index(k)][0] = v

#Calcular IDF
def calc_IDF():
    N = len(matriz_terminos)
    for i in range(len(matriz_terminos)):
        for j in range(len(matriz_terminos[i])):
            docs_aparece = 0
            for cont in range(len(matriz_terminos)):
                if (matriz_terminos[cont][j][0] != 0):
                    docs_aparece += 1
            valor = math.log((N/ float(docs_aparece)),10)
            matriz_terminos[i][j][1] = valor

#Calcular TF-IDF
def calc_TF_IDF():
    for i in range(len(matriz_terminos)):
        for j in range(len(matriz_terminos[i])):
            matriz_terminos[i][j][2] =  matriz_terminos[i][j][0] *  matriz_terminos[i][j][1]

# Matriz de similitud de documentos
matriz_sim = [ [ 0 for y in range(len(terminos)) ] for x in range(len(terminos)) ] #Primero pongo col, luego filas

# Calcular similitud coseno
def calc_sim_cos(doc1, doc2):
    parte_superior = 0
    parte_inferior_izquierda = 0
    parte_inferior_derecha = 0
    for i in range(len(terminos_unicos)):
       parte_superior += matriz_terminos[doc1][i][2] * matriz_terminos[doc2][i][2]
       parte_inferior_izquierda += pow(matriz_terminos[doc1][i][2],2)
       parte_inferior_derecha += pow(matriz_terminos[doc2][i][2],2)
    denominador = math.sqrt(parte_inferior_derecha) * math.sqrt(parte_inferior_izquierda)
    return (parte_superior/float(denominador))

# Rellenar la matriz de similitud entre documentos
def fill_matriz_sim():
    for i in range(len(matriz_sim)):
        for j in range(len(matriz_sim[i])):
            matriz_sim[i][j] = calc_sim_cos(i,j)

# Mostrar la informacion de cada documento bien formateada
def show_doc_data():
    for doc in range(len(matriz_terminos)):
        
        print "\n## Documento " + str(doc) + "\n" 
        
        print "Terminos analizados del documento >> " + str(len(terminos[doc])) + " palabras"
        print terminos[doc]
        print

        counter = 0
        
        cabecera = '{:<3} {:<20} {:<3} {:<6} {:<6}'.format("N.", "Termino", "TF", "IDF", "TF-IDF")
        print cabecera
        for term in range(len(matriz_terminos[doc])):
            
            linea_output = []
            if (matriz_terminos[doc][term][0] != 0):
                counter += 1
                linea_output.append(str(counter))
                linea_output.append(str(terminos_unicos[term]))
                linea_output.append(matriz_terminos[doc][term][0])
                idf_str = "{:.3f}".format(matriz_terminos[doc][term][1])
                linea_output.append(idf_str)
                tfidf_str = "{:.3f}".format(matriz_terminos[doc][term][2])
                linea_output.append(tfidf_str)

                
                linea_aux = '{:<3} {:<20} {:<3} {:<6} {:<6}'.format(linea_output[0], linea_output[1], linea_output[2], linea_output[3], linea_output[4])
                print linea_aux
        print "---------------------------------------------------------------"



#print
#show_matriz(matriz_terminos,0)
calc_IDF()
#print
#show_matriz(matriz_terminos,1)
calc_TF_IDF()
#print "-- MATRIZ VALORES TF-IDF"
#show_matriz(matriz_terminos,2)

fill_matriz_sim()
#print "+++ SIMILITUD +++"


show_doc_data()

show_matriz_sim(matriz_sim)

#Hasta aqui borrados los stopwords