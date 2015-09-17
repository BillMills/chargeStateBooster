import json, numpy

raw = open('raw.dat', 'r').read()
munged = open('masses.json', 'w')

# get rid of garbage characters
cleaning = raw.translate(None, '$massesarray();')
cleaning = cleaning.split('\n')
clean = ''
for line in cleaning:
	clean += line.split('=')[1] + '\n'

# an element symbol appears in lieu of Z in one place...?
elements = json.loads('{"Ru": {"Z": "44"}, "Re": {"Z": "75"}, "Rf": {"Z": "104"}, "Ra": {"Z": "88"}, "Rb": {"Z": "37"}, "Rn": {"Z": "86"}, "Rh": {"Z": "45"}, "Be": {"Z": "4"}, "Ba": {"Z": "56"}, "Bh": {"Z": "107"}, "Bi": {"Z": "83"}, "Bk": {"Z": "97"}, "Br": {"Z": "35"}, "H": {"Z": "1"}, "P": {"Z": "15"}, "Os": {"Z": "76"}, "Hg": {"Z": "80"}, "Ge": {"Z": "32"}, "Gd": {"Z": "64"}, "Ga": {"Z": "31"}, "Uub": {"Z": "112"}, "Pr": {"Z": "59"}, "Pt": {"Z": "78"}, "Pu": {"Z": "94"}, "C": {"Z": "6"}, "Pb": {"Z": "82"}, "Pa": {"Z": "91"}, "Pd": {"Z": "46"}, "Xe": {"Z": "54"}, "Po": {"Z": "84"}, "Pm": {"Z": "61"}, "Uuu": {"Z": "111"}, "Hs": {"Z": "108"}, "Uun": {"Z": "110"}, "Ho": {"Z": "67"}, "Hf": {"Z": "72"}, "Mo": {"Z": "42"}, "He": {"Z": "2"}, "Md": {"Z": "101"}, "Mg": {"Z": "12"}, "K": {"Z": "19"}, "Mn": {"Z": "25"}, "O": {"Z": "8"}, "Mt": {"Z": "109"}, "S": {"Z": "16"}, "W": {"Z": "74"}, "Zn": {"Z": "30"}, "Eu": {"Z": "63"}, "Es": {"Z": "99"}, "Er": {"Z": "68"}, "Ni": {"Z": "28"}, "No": {"Z": "102"}, "Na": {"Z": "11"}, "Nb": {"Z": "41"}, "Nd": {"Z": "60"}, "Ne": {"Z": "10"}, "Np": {"Z": "93"}, "Fr": {"Z": "87"}, "Fe": {"Z": "26"}, "Fm": {"Z": "100"}, "B": {"Z": "5"}, "F": {"Z": "9"}, "Sr": {"Z": "38"}, "N": {"Z": "7"}, "Kr": {"Z": "36"}, "Si": {"Z": "14"}, "Sn": {"Z": "50"}, "Sm": {"Z": "62"}, "V": {"Z": "23"}, "Sc": {"Z": "21"}, "Sb": {"Z": "51"}, "Sg": {"Z": "106"}, "Se": {"Z": "34"}, "Co": {"Z": "27"}, "Cm": {"Z": "96"}, "Cl": {"Z": "17"}, "Ca": {"Z": "20"}, "Cf": {"Z": "98"}, "Ce": {"Z": "58"}, "Cd": {"Z": "48"}, "Tm": {"Z": "69"}, "Cs": {"Z": "55"}, "Cr": {"Z": "24"}, "Cu": {"Z": "29"}, "La": {"Z": "57"}, "Li": {"Z": "3"}, "Tl": {"Z": "81"}, "Lu": {"Z": "71"}, "Lr": {"Z": "103"}, "Th": {"Z": "90"}, "Ti": {"Z": "22"}, "Te": {"Z": "52"}, "Tb": {"Z": "65"}, "Tc": {"Z": "43"}, "Ta": {"Z": "73"}, "Yb": {"Z": "70"}, "Db": {"Z": "105"}, "Zr": {"Z": "40"}, "Dy": {"Z": "66"}, "I": {"Z": "53"}, "U": {"Z": "92"}, "Y": {"Z": "39"}, "Ac": {"Z": "89"}, "Ag": {"Z": "47"}, "Ir": {"Z": "77"}, "Am": {"Z": "95"}, "Al": {"Z": "13"}, "As": {"Z": "33"}, "Ar": {"Z": "18"}, "Au": {"Z": "79"}, "At": {"Z": "85"}, "In": {"Z": "49"}}')
for elt in elements.keys():
	clean = clean.replace(elt, elements[elt]['Z'])

# drop newlines, need to replace with , or numbers get mushed together:
clean = clean.replace('\n', ',')

#drop whitespace
clean = clean.replace(' ', '')

# break numbers up into iterable list
rawlist = clean.split(',')
# break list up into associated tuples
masses = []
for i in range(len(rawlist)/3):
	masses.append( (rawlist[3*i], rawlist[3*i+1], rawlist[3*i+2]) );

#determine highest Z:
maxZ = 0
for species in masses:
	if int(species[1]) > maxZ:
		maxZ = int(species[1])

# sort tuples in list indexed by Z, of dictionaries keyed by A
table = numpy.empty(maxZ+1, dtype=dict)

for species in masses:

	A = species[0]
	Z = int(species[1])
	m = species[2]

	if table[Z] is None:
		table[Z] = {}

 	table[Z][A] = m

# replace the neutron with an empty dict
table[0] = {}

elts = []
# extract dictionaries into a simple list for serialization:
for element in table:
	elts.append(element)

munged.write(json.dumps(elts))