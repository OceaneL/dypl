package dypl_week3;

public class Scissors extends Weapon {
	
	static String name = "scissors";
	
	public Result attack(Weapon weapon) {
		return weapon.eval(this);
	}
	
	public Result eval(Rock weapon) {
			return Result.win;
	}
	
	public Result eval(Scissors weapon) {
			return Result.tie;
	}
	
	public Result eval(Paper weapon) {
			return Result.lose;
	}

	public static String getClassName() {
		return name;
	}
	
	@Override
	public String getName() {
		return name;
	}
	
}
