# coding: utf-8
"""
	Programme qui produit l'extraction lexicale selon l'alignement de chaque 
	mot et qui enregistre chaque mot du texte et tous ses alignements 
	dans deux dictionnaires, l'un de la langue source à la langue cible, 
	l'autre dans le sens inverse.
	Les deux dictionnaires sont ensuite consultables par l'utilisateur.
	
	Usage : 
		python traitement_aligner.py nomFichierTexte nomFichierAlignement
	
	Arguments:
		
		nomFichierTexte -- Chemin d'accès au fichier contenant le texte 
		bilingue utilisé par l'aligneur
		
		nomFichierTexte -- Chemin d'accès au fichier contenant l'alignement 
		réalisé par Fast-align
"""
import sys
import re

########################################################################
###########################	ZONE DE FONCTIONS	########################
########################################################################
def best(h, clé):
	"""
	Fonction récupérant le mot le plus utilisé pour traduire le mot clé 
	recherché en inversant les couples mot/nombre d'occurences parmi les 
	valeurs du dictionnaire
	"""
	invMax={}
	for mot in h[clé]:
		invMax[h[clé][mot]]=mot
	return(invMax[max(invMax.keys())])
	
def tab(fichier):
	"""
	Fonction qui permet après lecture d'un fichier d'ajouter chacune des 
	lignes de ce fichier comme élément d'une liste.
	"""
	table=[]
	for line in fichier:
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
	new=new.replace("( ","(")
	new=new.replace(" )",")")
	new=new.replace("'","' ")
	new=new.replace("' )","')")
	return new

def coordonnees(phrase):
	"""
	Fonction qui repère les coordonées type latitudes/longitudes et 
	remplace l'espace qui les sépare par [SPACE]
	"""
	phrase=re.sub(r"(\(?(-?\d+\d*([$€£%'°]))+)(\s)((\d+\d*([$€£%'°]))+\))",r"\g<1>[SPACE]\g<5>",phrase)
	return phrase

def tri(dictionnaire):
	"""
	Cette fonction (à compléter) permettra de faire un tri dans les cas où
	on a beaucoup de correspondances de traductions pour un mot.
	"""
	dico=dictionnaire
	# ~ if len(dico)>3:
		
		# ~ for mot in dico :
			
			# ~ print("quelque chose")
	return (dico)

########################################################################
###########################	ZONE DE CODE	############################
########################################################################

#On récupère le nom des fichiers à ouvrir

srcFile=sys.argv[1]
alignement=sys.argv[2]
# ~ srcFile="Corpus_fast-align-200.txt"
# ~ alignement="forward-long.align"

#On ouvre les fichiers

src = open(srcFile, "r", encoding="utf8")
al=open(alignement, "r", encoding="utf8")

#On lit le fichier du corpus bilingue et on récupère les phrases.
#On les place respectivement dans deux tableaux : 
#"srctab" pour la langue source et "tgttab" pour la langue cible

lineTab=tab(src)
srctab=[]
tgttab=[]

for i in range(0,len(lineTab)):
	temptab=[]
	temptab=lineTab[i].split(" ||| ")
	srctab.append(propre(temptab[0]))
	tgttab.append(propre(temptab[1]))

#On récupère le contenu du fichier fast-align dans le tableau "lineAl"

lineAl=tab(al)

#On ferme les fichiers

src.close()
al.close()

#On crée deux hashages qui contiendront les mots recherchés (clés) 
#et leurs traductions possibles (valeurs)
#"fr" pour la langue source, le français, et "en" pour la cible, l'anglais. 
#(Mais cela fonctionnera peu importe le couple de langue)
fr={}
en={}

#On vérifie si la taille des deux fichiers (corpus et alignements) est identique.
#Sinon on affiche un message d'erreur.

if (len(lineTab)==len(lineAl)):
	
#Ensuite on fait défiler les éléments des tableaux pour récupérer les 
#alignements de chaque mot de la phrase en cours.

	for i in range(0,len(lineAl)):
		
#Dans "corr" (pour "correspondance") on a toutes les paires de chiffres
#séparés par des "-", le premier (corr[n].split("-")[0]) correspond à l'id
#d'un mot français dans "srctab", le second à celui d'un mot anglais dans "tgttab"

		corr=lineAl[i].split(" ")

#Ici on règle les problèmes liés à des coordonées gps dans un texte 
#(il faut compter les doordonnées comme un seul mot)
#On remplace les espaces des coordonées par [SPACE] puis on découpe la phrase
#Aux espaces restants pour ranger chaque mot dans les tableaux "frMots" et "enMots"

		frMots=coordonnees(srctab[i]).split(" ")
		enMots=coordonnees(tgttab[i]).split(" ")

#"n" représente l'indice de chaque paire de correspondance dans "corr"

		for n in range (0, len(corr)):
			key=int(corr[n].split("-")[0])
			val=int(corr[n].split("-")[1])
#"key" et "val" sont des indices correspondants aux mots présents respctivement dans frMots et enMots

			if (key==len(frMots) or val==len(enMots)):
				break
#Ce if permet de terminer la ligne si jamais le tableau frMots est plus court que que veut trouver l'indice key

#On enleve les potentielles ponctuactions collées aux mots

#Pour cela on écrit d'abord une expression régulière qui va rechercher les mots qu'on dira bien formés
			noPonctuation= re.compile(r"(\(.[^)]*\)|\d+(,|\.|\s)?\d*(\s*[$€£])*|€|\w+)",re.U)

#On remplace les [SPACE] par des espaces normaux
			for m in range (0,len(frMots)):
				frMots[m]=frMots[m].replace("[SPACE]"," ")
			for m in range (0,len(enMots)):
				enMots[m]=enMots[m].replace("[SPACE]"," ")
				
#Si le mot n'est pas "bien formé", on estime qu'il s'agit d'une ponctuation.
#Dans ce cas on le remplace par "[punct]"
			if noPonctuation.search(frMots[key]):
				fran=noPonctuation.search(frMots[key])
				fran=fran.group().casefold()
			else:
				fran="[punct]"
			if noPonctuation.search(enMots[val]):
				angl=noPonctuation.search(enMots[val])
				angl=angl.group().casefold()
			else:
				angl="[punct]"
				
#On ajoute le mot actuel au dictionnaire
			if (fran in fr.keys()): 
				if (angl not in fr[fran].keys()):
					fr[fran][angl]=1
				else :
					fr[fran][angl]=fr[fran][angl]+1
			else:
				fr[fran]={angl:1}
#Dans l'autre sens pour la langue cible
				
			if (angl in en.keys()): 
				if (fran not in en[angl].keys()):
					en[angl][fran]=1
				else :
					en[angl][fran]=en[angl][fran]+1
			else:
				en[angl]={fran:1}
#On calcule un pourcentage de ce qui a été réalisé et on l'affiche
		pourcentage=((i+1)*100)/(len(lineAl))
		
		if (pourcentage!=100):
			print ("Avancement : "+str(pourcentage)+"%.")
	print ("Terminé !")
	
else:
	print("Les deux fichiers n'ont pas le même nombre de lignes. Vérifiez que vous avez sélectionné les bons fichiers.")

#On peut enregistrer les dictionnaires dans un fichier

# ~ fichier = open("results.txt", "w", encoding="utf8")
# ~ fichier.write(fr)
# ~ fichier.close()

########################################################################
###############	ZONE DE TESTS DES RESULTATS DE FAST ALIGN	############
########################################################################

"""
Cette partie est reservée à la phase de tests sur l'alignement produit 
par Fast_Align.
Ici, on va essayer de récupérer un fichier txt contenant plusieurs 
paragraphe.

Chaque paragraphe est constitué de 5 lignes :

Ligne 1 : Le numéro de ligne.
Ligne 2 : La phrase en français.
Ligne 3 : La phrase en anglais.
Ligne 4 : La ligne correspondant dans le fichier fast align.
Ligne 5 : l'alignement mot à mot transcrit par ce script.
"""

########################################################################
###########################	ZONE INTERFACE UTILISATEUR	################
########################################################################

fini=False
while not (fini==True):
	print("Pour afficher le dictionnaire français-anglais : fr\nPour afficher le dictionnaire anglais-français : en\nPour effectuer une recherche par mot clé : r\nPour effectuer une recherche par mot clé de la traduction la plus utilisée pour un mot : r+\nPour quitter : q")
	action=str(input("Votre choix : ")).casefold()
	if (action=="r"):
		mot=str(input("Entrez le mot à chercher : ")).casefold()
		if mot in fr.keys():
			print (tri(fr[mot]))
		elif mot in en.keys():
			print (tri(en[mot]))
		else :
			print("Le mot demandé n'est pas répertorié.")
	elif (action=="r+"):
		mot=str(input("Entrez le mot à chercher : ")).casefold()
		if mot in fr.keys():
			print ("Traduction de \""+mot+"\" la plus utilisée : "+best(fr,mot))
		elif mot in en.keys():
			print ("Traduction de \""+mot+"\" la plus utilisée : "+best(en,mot))
		else :
			print("Le mot demandé n'est pas répertorié.")
	elif (action=="fr"):
		print(fr)
	elif (action=="en"):
		print(en)
	else:
		print ("L'action saisie n'est pas reconnue.")
	continuer=str(input("Appuyez sur Entrée pour continuer, ou écrivez Q puis appuyez sur Entrée pour arrêter : ")).casefold()
	if (continuer=="q"):
		fini=True
