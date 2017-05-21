### Modèle pour vos Makefile

## Compilateur C et éditeur de liens
CC      = gcc


## Options pour la compilation du C
CFLAGS  = -Wall -std=c99
#  Spécifie la version de la norme POSIX à respecter
CFLAGS += -D_XOPEN_SOURCE=500
#  Active les informations de débogage
CFLAGS += -g


## Options de l’édition de liens
LDFLAGS  = -g


## Première cible
#  « make » sans argument construit sa première cible
#  Indiquez en dépendance le ou les binaires à construire
all: prog prog2


compile: all

#exec:




## Compilation séparée
#  Le .o doit être recompilé dès que le .c ou le .h (s'il existe) change
%.o: %.c %.h
	${CC} ${CFLAGS} -c $< -lm

## Édition de liens
#  Définissez une règle par binaire que vous voulez créer
#  La commande devrait en général être identique pour chaque binaire
prog: prog.o
	${CC} ${LDFLAGS} -o $@ $^ -lm

prog2: prog2.o
	${CC} ${LDFLAGS} -o $@ $^ -lm





clean:
	rm *.o || true
	rm *~ || true

realclean: clean
	rm prog || true


## Liste des pseudo-cibles
#  Ces cibles ne correspondent pas à des fichiers que l'on veut créer,
#  juste à des séquences que l'on veut pouvoir déclencher
.PHONY: all clean realclean
