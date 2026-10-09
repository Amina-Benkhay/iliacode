"""ILIACode, séance 1 du module NLP. Du fichier aux tokens (fichier à compléter).

Chaque fonction est une étape de la chaîne
octets -> décoder -> réparer -> normaliser -> tokeniser -> mesurer.
"""
import re
#regular expression
# re module python
import unicodedata
# unicode module py
from collections import Counter
# collections  package et counter class
import ftfy
#Fixes Text For You
# ftfy bibliotheque
#for mojibakes

CHIFFRES_ARABES = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

#Cette ligne crée une table de traduction qui permet de convertir les chiffres arabo-indiens (٠١٢٣٤٥٦٧٨٩) en chiffres latins (0123456789).
# str = la classe des chaînes de caractères en Python.
# maketrans = abréviation de "make translation" ("fabriquer une table de traduction").
# C'est une méthode statique : on l'appelle sur la classe str, pas sur une instance.
# ordre compte

MOTIF = r'"[^"]*"|#.*|\d+\.\d+|!=|<=|>=|\w+|[^\w\s]'   # le cœur, à compléter à gauche par les règles de protection


def lire(chemin, regle="utf-8"):
# Elle reçoit deux paramètres :
# chemin → le chemin du fichier à lire.
# regle="utf-8" → l'encodage utilisé pour décoder le fichier. Si on ne précise rien, Python utilise UTF-8.
    """Bloc Lire. Ouvre le fichier en octets puis les décode en caractères."""
    # 1. ouvrir le fichier en mode binaire "rb" et lire ses octets
    # 2. décoder ces octets avec la règle reçue, puis renvoyer le texte
    with open(chemin, "rb") as f:
         
                # r = read → lecture
                # b = binary → mode binaire
                # Donc le fichier est ouvert pour récupérer directement ses octets.
            octets = f.read() # récupérer les octets
            return octets.decode(regle)#transformer les octets en texte


def reparer(texte):

    # Entrée : une chaîne str (possiblement corrompue).
    # Sortie : une chaîne str (corrigée).
    # reparer("cafÃ©")     # ✅ str
    # reparer(b"caf\xc3\xa9")  # ❌ bytes → ftfy ne l'accepte pas

    """Bloc Réparer. Corrige les mojibakes, laisse intact un texte sain."""
    #  _text(texte, normalization=None)
    # normalization=None, car normaliser est l'étape suivante, pas celle-ci
    return ftfy.fix_text(texte, normalization=None)
# fix_text — la fonction
# C'est la fonction principale de ftfy. Elle détecte et corrige les problèmes d'encodage.


def normaliser(texte, forme="NFKC"):
    """Bloc Normaliser. Une seule écriture par caractère."""
    # 1. unicodedata.normalize(forme, texte)
    # 2. supprimer les diacritiques arabes, de \u064B à \u065F, avec re.sub
    # 3. supprimer le tatweel \u0640 avec replace
    # 4. convertir les chiffres arabes avec translate et CHIFFRES_ARABES
    texte = unicodedata.normalize(forme, texte)
    texte = re.sub("[\u064B-\u065F]", "", texte)
# Cette ligne supprime tous les harakat (diacritiques arabes) d'une chaîne.
#intervalle harakat c'est \u064B-\u065F

    texte = texte.replace("\u0640", "")
    # ici on supprime tatweel
    texte = texte.translate(CHIFFRES_ARABES)
    return texte

def tokeniser(texte):
    """Bloc Tokeniser. Six règles, protéger d'abord, découper ensuite."""
    # 1. re.findall(MOTIF, texte) applique les règles 1 à 5
    # 2. règle 6, pour chaque token qui est un mot et contient un tiret bas,
    #    garder le token puis ajouter ses composants, token.split("_")
    tokens = []
    for token in re.findall(MOTIF, texte):
        tokens.append(token)
        if "_" in token and re.fullmatch(r"\w+", token):
         tokens.extend(c for c in token.split("_") if c)# if c non vide

        # re.match vérifie si la chaîne commence par le motif (ignore le reste), re.search cherche le 
        # motif n'importe où dans la chaîne, et re.fullmatch exige que toute la chaîne corresponde 
        # exactement au motif. Exemple avec "chat" sur "chateau" : match et search trouvent "chat",
        # mais fullmatch échoue car "chateau" n'est pas exactement "chat". Dans tokeniser(), '
        # 'on utilise fullmatch pour s'assurer qu'un token est entièrement un mot (\w+) '
        # 'avant de l'éclater, évitant ainsi les faux positifs comme "user_name!".
    
    return tokens



def mesurer(tokens):
    """Bloc Mesurer. Fréquence de chaque token distinct."""
    # une ligne, Counter(tokens)
    return Counter(tokens)
# Entrée : une liste de tokens list[str].
# Sortie : un objet Counter (dictionnaire token → nombre d'occurrences).
# Liste : ['le', 'chat', 'le', 'chien', 'le']
# Résultat : {'le': 3, 'chat': 1, 'chien': 1}

def chaine(chemin, regle="utf-8"):
    """La chaîne complète, du fichier aux tokens."""
    return tokeniser(normaliser(reparer(lire(chemin, regle))))
