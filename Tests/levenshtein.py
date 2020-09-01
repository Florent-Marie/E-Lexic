# coding: utf-8
import Levenshtein as lev

def levCalclulate(str1, str2,n1,n2):
	Distance = lev.distance(str1, str2)
	Ratio = lev.ratio(str1, str2)
	print("Levenshtein entre {0} et {1} :".format(n1, n2))
	print("> Distance: {0}\n> Ratio: {1}\n".format(Distance, Ratio))

nom1="forward-reduit.align"
nom2="forward-long.align"
al1=open(nom1, "r", encoding="utf8")
al2=open(nom2, "r", encoding="utf8")
align1=""
align2=""
for line in al1:
	line=line.strip()
	align1+=line+"\n"
for line in al2:
	line=line.strip()
	align2+=line+"\n"


levCalclulate(align1, align2, nom1, nom2)
