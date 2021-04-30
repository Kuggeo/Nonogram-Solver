# Logic.py - Sofiane DJERBI & Salem HAFTARI
""" CONVENTIONS
 | Notations :
 | a + b + (-cd) := NNGFormula([[1], [2], [-3, 4]])
 | En théorie nous manipulons des listes, c'est donc plus pratique et simple
 | qu'utiliser *args. Même si cela ne rend pas très "simple" en exemple.
 |
 | /!\ Cette implémentation n'est pas une implémentation complète de la logique
 | Nous traitons uniquement des FND / FNC
"""
import pickle
import os
import threading
from itertools import product


class NNGFormula:
    """ OBJET FORMULE LOGIQUE (adapté pour les nonogrammes)
    Variables:
        - list: Liste des sous formules, conjonctions ou disjonctions.
    """
    def __init__(self, l=[]):
        """ INITIALISATION
        Paramètres:
            - l: Liste des sous termes.
        """
        self.name = f"TMP_{os.getpid()}.ngf"
        self.file = open(self.name, 'wb+') # Binary pour aller plus vite

    #def __str__(self): # !!! DEPRECATED !!!
    #    """ AFFICHAGE DIMACS """
    #    return " 0\n".join(" ".join(str(e) for e in x) for x in self.file) + " 0"

    def append(self, l):
        """ AJOUTE DES ELEMENTS DANS LA LISTE
        Paramètres:
            - l: Sous liste (FNC)
        """
        l = [str(i) for i in l]
        txt = " ".join(l) + "\n"
        txt = txt.encode('ascii')
        self.file.write(txt)

    def solve(self, engine):
        """ RESOUDRE UNE FORMULE
        Paramètres:
            - engine: Classe Algorithme/Solveur SAT (Classe et non objet!)
        Retourne:
            - None si la formule n'admet pas de modèle
            - Une liste si la formule admet un modèle
        """
        self.file.close() # On ferme le fichier
        file = open(self.name, "rb") # On l'ouvre en mode lecture
        instance = engine() # Une instance de l'engine pour pas le modifier
        for clause in file:
            clause = clause.decode('ascii')
            clause = [int(i) for i in clause[:-1].split(' ')] # On enlève l'espace + le 0
            instance.add_clause(clause) # On enlève le \n
        file.close()
        threading.Thread(target=os.remove, args=[self.name]).start() # Supression dans un thread différent
        if instance.solve():
            return instance.get_model()
        return None # Sinon pas obligatoire car le if retourne


if __name__ == "__main__": # DEBUG !
    from pysat.solvers import Glucose4
    a = NNGFormula([[1,2,3,10], [4,5], [6,7,8]])
    #print(a) # FND
    #a.linearize() # FND -> FNC
    #print(a) # FNC
    # CryptoMiniSat: "v 1 2 3 -4 -5 -6 -7 -8 -9 -10 -11 0"
    #a.save("test", "./")
    #b = NNGFormula()
    #b.load("test.ngf")
    #print(b) # Fonctionnel
    # Maintenant on va solver a
    a = NNGFormula([[1,2,3,10], [4,5], [6,7,8]])
    print(a.solve(Glucose4)) #Fonctionnel!
