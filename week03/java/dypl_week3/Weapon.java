package dypl_week3;

import java.util.Random;
import java.util.Scanner;

/**
 * @author oceane
 *
 */
public abstract class Weapon {
	
	public abstract String getName();
	
	/**
	 * Attack an other weapon
	 * @return the result of the attack
	 */
	public abstract Result attack(Weapon weapon);
	public abstract Result eval(Paper weapon);
	public abstract Result eval(Scissors weapon);
	public abstract Result eval(Rock weapon);
	
	
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.print("How many rounds ?");
		int nbRounds = -1;
		while (nbRounds < 0) {
			try{
				nbRounds = sc.nextInt();				
			}catch (java.util.InputMismatchException e) {		
			}
			sc.nextLine();
			if (nbRounds < 0){
				System.out.println("you have to put a positive number");
				
			}
		}
		
		
		System.out.println("Game started");
		Random rand = new Random();
		int nbWin = 0;
		int nbLose = 0;
		for (int i = 1; i <= nbRounds; i++){
			System.out.println("Make your choice for round "+i+": ");
			String weaponName = sc.nextLine().trim();
			Weapon weapon = null;
			Weapon weaponList[] = {new Scissors(), new Rock(), new Paper()};
			for (Weapon element : weaponList){
				if (element.getName().equals(weaponName)){
					weapon = element;
				}
					
			}
			if (weapon == null) {
				System.out.println(weaponName+ " is an incorrect weapon : choose scissors or rock or paper");
				i--;
				continue;
			}
			Weapon weapon2 = weaponList[rand.nextInt(3)];
			System.out.printf("You chose "+weapon.getName()+", your opponent chose "+weapon2.getName()+".");
			Result result= weapon.attack(weapon2);
			if (result.equals(Result.win)){
				nbWin++;
			}
			else if (result.equals(Result.lose)){
				nbLose++;
			}
			System.out.println(result.sentence);
			
		}
		System.out.print("Result: You won "+nbWin+" time, your opponent won "+nbLose+" time. ");
		Result resultFinal;
		if (nbWin > nbLose){
			resultFinal = Result.win;
		}
		else if (nbWin < nbLose){
			resultFinal = Result.lose;
		}
		else resultFinal = Result.tie;
		System.out.println(resultFinal.sentence);
		sc.close();
	}
}
