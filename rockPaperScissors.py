import random


class Result:
    def __init__(self, value, name):
        self.value = value
        self.name = name
    def __eq__(self, other):
        return self.value == other.value

Result.LOSE = Result(1,"Your opponent wins!")
Result.WIN = Result(2,"You win!")
Result.TIE = Result(3,"It's a tie!")

class Weapon(object):
    def __str__(self):
        return self.__class__.__name__.lower

class Paper(Weapon):
    def attack(self, weapon):
        return weapon.evalPaper(self, weapon)
    def evalPaper(self, weapon):
        return Result.TIE
    def evalScissors(self, weapon):
        return Result.WIN
    def evalRock(self, weapon):
        return Result.LOSE

class Scissors(Weapon):
    def attack(self, weapon):
        return weapon.evalScissors(self, weapon)
    def evalPaper(self, weapon):
        return Result.LOSE
    def evalScissors(self, weapon):
        return Result.TIE
    def evalRock(self, weapon):
        return Result.WIN

class Rock(Weapon):
    def attack(self, weapon):
        return weapon.evalRock(self, weapon)
    def evalPaper(self, weapon):
        return Result.WIN
    def evalScissors(self, weapon):
        return Result.LOSE
    def evalRock(self, weapon):
        return Result.TIE


def main():
    Weapons = Weapon.__subclasses__()
    nbRound = -1
    while nbRound <= -1:
        try :
            nbRound = int(input("How many rounds ?"))
        except ValueError:
            print("You have to put a positive number !")
    iRound = 1
    nbWin = 0
    nbLose = 0
    while iRound <= nbRound :
        nameWeapon = ""
        while nameWeapon not in map(lambda x : x.__name__, Weapons) :
            if nameWeapon != "":
                print(nameWeapon+ " is an incorrect weapon : choose scissors or rock or paper");
            nameWeapon = input("Make your choice for round "+str(iRound)+": ")
            nameWeapon = nameWeapon.title()
        weapon1 = eval(nameWeapon)
        weapon2 = random.choice(Weapons)
        result = weapon1.attack(weapon1, weapon2)
        print("You chose ", weapon1.__name__, ", your opponent chose ", weapon2.__name__, ".");
        print(result.name)
        if result == Result.WIN :
            nbWin += 1
        elif result == Result.LOSE :
            nbLose += 1
        iRound += 1
    print("Result: You won ",nbWin," time, your opponent won ", nbLose, " time. ");
    if nbWin > nbLose :
        resultFinal = Result.WIN
    elif nbWin < nbLose :
        resultFinal = Result.LOSE
    else : resultFinal = Result.TIE;
    print(resultFinal.name);

if __name__ == '__main__':
    main()
