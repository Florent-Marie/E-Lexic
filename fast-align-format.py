# coding: utf-8
"""
	Programme qui fusionne deux textes dans un unique fichier texte 
	après les avoir nettoyés afin que leur format soit accepté par 
	fast_align.
	
	Usage : 
		python fast-align-format.py texte1 texte2
		
		ou :
		
		python fast-align-format.py texte1 texte2 nomSortie
	
	Arguments:
		
		texte1 -- Chemin d'accès au fichier contenant le texte 
		dans la langue source
		
		texte2 -- Chemin d'accès au fichier contenant le texte 
		dans la langue cible
		
		nomSortie -- Chemin d'accès du fichier de sortie contenant la
		fusion des deux textes. En cas d'absence de cet argument, un chemin
		d'accès par défaut sera donné : Corpus_fast-align.txt. 
"""
import sys
import re
import os

def tab(text):
	"""
	Fonction qui permet après lecture d'un fichier d'ajouter chacune des 
	lignes de ce fichier comme élément d'une liste.
	"""
	table=[]
	for line in text:
		line=line.strip()
		table.append(line)
	return table

def propre(s):
	"""
	Fonction qui épure le texte de caractères de ponctuations non-conformes,
	comme les apostrophes différentes et les signes de ponctuation gênants
	qui seraient encore présents dans le texte.
	"""
	regex= re.compile(r"\s(\W|·)\s")
	new=regex.sub(" ",s)
	new=new.replace("ʼ","'")
	new=new.replace("ʼ ","'")
	new=new.replace("' ","'")
	new=new.replace("’ ","'")
	new=new.replace("’","'")
	
	new=new.replace("“","\"")
	new=new.replace("”","\"")
	regex= re.compile(r"^\W+",re.M)
	new=regex.sub("",new)
	return new


#On récupère le nom des fichiers à ouvrir

srcFile=sys.argv[1]
trgtFile=sys.argv[2]
print (sys.argv)
if (len(sys.argv)==4):
	sortie=sys.argv[3]
else:
	sortie="Corpus_fast-align.txt"

#On ouvre les fichiers

src = open(srcFile, "r", encoding="utf8")
trgt = open(trgtFile, "r", encoding="utf8")

#On lit les fichiers et on récupère les contenus dans la variable text
srcTab=tab(src)
trgtTab=tab(trgt)
corpus=""
regex= re.compile(r"«\W|\W»|[:?!]")
regex2=re.compile(r" · ")
	
for i in range(0,len(srcTab)):
	print ("Total number of lines : "+str(len(srcTab))+". "+str(len(srcTab)-i)+ " lines remaining.")
	srcPhrase=propre(srcTab[i])
	trgtPhrase=propre(trgtTab[i])
	if (srcPhrase!="" and trgtPhrase!=""):
		ligne=srcPhrase+" ||| "+trgtPhrase+"\n"
		ligne=regex.sub("",ligne)
		ligne=ligne.replace("  "," ")
		ligne=regex2.sub(", ",ligne)
		ligne=re.sub(r"(\w)(\.)(\w)",r"\g<1>. \g<3>",ligne)
		ligne=re.sub(r"(\s)(,|\.)(\s)",r"\g<2> \g<3>",ligne)
		ligne=ligne.replace("  "," ")
		corpus+=ligne


#On affiche (on enregistre) les résultats

fichier = open(sortie, "w", encoding="utf8")
fichier.write(corpus)
fichier.close()

#On ferme les fichiers
trgt.close()
src.close()

print("Ecriture terminée")
# ~ print("Ouverture du fichier dans fast_align.")
# ~ os.system("cd ../fast_align-master/build/")
# ~ truc=os.popen("./fast_align -i Corpus_fast-align.txt -d -o -v")
# ~ ah=truc.read()
# ~ print(ah)
# ~ print("Terminé")

