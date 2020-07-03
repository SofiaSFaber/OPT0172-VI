# -*- coding: utf-8 -*-
"""TrabalhoBanco.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AWa9q0ZR1Q6LTg1B9Qi4fCegMcxw9dEY
"""

# IMPORTS BIBLIOTECAS
import pandas as pd
from google.colab import files
!pip install biopython
import Bio
from Bio import Entrez, SeqIO
import json

# IMPORT DO CSV DO MARDY
files.upload()

# LEITURA DO CSV DO MARDY POR GENES
pd.set_option('display.max_rows', 500) #definição do tamanho máximo de linhas e colunas para mostrar o dataframe
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

mardy = pd.read_csv('DB_by_gene.csv',header = 1) #leitura do csv para o dataframe com título definido
mardy.rename(columns = {'Gene name':'GeneName','Found in':'FoundIn','Gene locus':'GeneLocus','AA mutation':'AAMutation',
                        'Tandem repeat name':'TandemRepeatName','Tandem repeat sequence':'TandemRepeatSequence'}, inplace=True) #tirar espaços dos titulos
mardy

# SALVAR GENES DO MARDY

genes = [] #Criação array dos genes do mardy
for i in range(len(mardy.GeneName)): #Percorre todo o dataframe em relação ao GeneName
  genes.append(mardy.GeneName[i]) #Adiciona os genes do dataframe
genes=sorted(set(genes)) #Retira genes duplicados e ordena
print("Genes: ",genes)
print("\nNúmero de Genes: ",len(genes))

# ACESSO AO NCBI E PESQUISA

Entrez.email = "sofia17faber@gmail.com" #Autenticação para poder acessar o NCBI
resultados={} #Criação dicionário para resultados de cada gene
remover = [] #Array para remover genes com menos de 3 resultados
for i in range(len(genes)):
  handle = Entrez.esearch(db="nucleotide", term=genes[i]) #Pesquisa do gene
  record = Entrez.read(handle) #Resultados da pesquisa (20 primeiros)
  if len(record['IdList'])>2: #Se tem pelo menos 3 resultados
    resultados[genes[i]]=record["IdList"][0],record['IdList'][1],record['IdList'][2] #Adiciona no dicionario o gene com os 3 primeiros resultados
  else:
    remover.append(genes[i]) #Adiciona os genes com menos de 3 resultados para depois remover
resultados

for i in range(len(remover)):
  genes.remove(remover[i]) #Remove os genes com menos de 3 resultados

print("Genes: ",genes)
print("\nNúmero de Genes: ",len(genes))

#BUSCA 

dados = {} #Cria o dicionario com os dados finais
for i in range(len(genes)):
    handle = Entrez.efetch(db="nucleotide", id=resultados[genes[i]][0], retmode="xml") #Pesquisa o primeiro resultado no NCBI
    records1 = Entrez.read(handle)
    handle = Entrez.efetch(db="nucleotide", id=resultados[genes[i]][1], retmode="xml") #Pesquisa o segundo resultado no NCBI
    records2 = Entrez.read(handle)
    handle = Entrez.efetch(db="nucleotide", id=resultados[genes[i]][2], retmode="xml") #Pesquisa o terceiro resultado no NCBI
    records3 = Entrez.read(handle)
    if ("GBSeq_references" in records1[0].keys() and "GBSeq_references" in records2[0].keys() and "GBSeq_references" in records3[0].keys() and
    "GBSeq_strandedness" in records1[0].keys() and "GBSeq_strandedness" in records2[0].keys() and "GBSeq_strandedness" in records3[0].keys() and
    "GBSeq_locus" in records1[0].keys() and "GBSeq_locus" in records2[0].keys() and "GBSeq_locus" in records3[0].keys() and
    "GBSeq_length"in records1[0].keys() and "GBSeq_length" in records2[0].keys() and "GBSeq_length" in records3[0].keys() and
    "GBSeq_moltype" in records1[0].keys() and "GBSeq_moltype" in records2[0].keys() and"GBSeq_moltype" in records3[0].keys() and
    "GBSeq_topology" in records1[0].keys() and "GBSeq_topology" in records2[0].keys() and "GBSeq_topology" in records3[0].keys() and
    "GBSeq_division" in records1[0].keys() and "GBSeq_division" in records2[0].keys() and "GBSeq_division" in records3[0].keys() and
    "GBSeq_definition" in records1[0].keys() and "GBSeq_definition" in records2[0].keys() and "GBSeq_definition" in records3[0].keys() and
    "GBSeq_accession-version" in records1[0].keys() and "GBSeq_accession-version" in records2[0].keys() and "GBSeq_accession-version" in records3[0].keys() and
    "GBSeq_definition" in records1[0].keys() and "GBSeq_definition" in records2[0].keys() and "GBSeq_definition" in records3[0].keys()):
      dados[genes[i]]="Primeiro Resultado:",resultados[genes[i]][0],records1[0]["GBSeq_locus"],records1[0]["GBSeq_length"],records1[0]["GBSeq_strandedness"],records1[0]["GBSeq_moltype"],records1[0]["GBSeq_topology"],records1[0]["GBSeq_division"],records1[0]["GBSeq_definition"],records1[0]["GBSeq_accession-version"],records1[0]["GBSeq_source"],records1[0]["GBSeq_references"],\
      "Segundo Resultado:",resultados[genes[i]][1],records2[0]["GBSeq_locus"],records2[0]["GBSeq_length"],records2[0]["GBSeq_strandedness"],records2[0]["GBSeq_moltype"],records2[0]["GBSeq_topology"],records2[0]["GBSeq_division"],records2[0]["GBSeq_definition"],records2[0]["GBSeq_accession-version"],records2[0]["GBSeq_source"],records2[0]["GBSeq_references"],\
      "Terceiro Resultado:",resultados[genes[i]][2],records3[0]["GBSeq_locus"],records3[0]["GBSeq_length"],records3[0]["GBSeq_strandedness"],records3[0]["GBSeq_moltype"],records3[0]["GBSeq_topology"],records3[0]["GBSeq_division"],records3[0]["GBSeq_definition"],records3[0]["GBSeq_accession-version"],records3[0]["GBSeq_source"],records3[0]["GBSeq_references"]
dados

arquivo_json = json.dumps(dados,indent=1, separators=('\r\n', ':'), sort_keys=True)
file = open('arquivo.json', 'w')
file.write(arquivo_json)
file.close()
files.download('arquivo.json')

print(arquivo_json)

