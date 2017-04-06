package dypl_week3;

public class Rock extends Weapon{

	static String name = "rock";
	

	public Result attack(Weapon weapon) {
		return weapon.eval(this);
	}
	
	public Result eval(Rock weapon) {
			return Result.tie;
	}
	
	public Result eval(Scissors weapon) {
			return Result.lose;
	}
	
	public Result eval(Paper weapon) {
			return Result.win;
	}

	public static String getClassName() {
		return name;
	}
	
	@Override
	public String getName() {
		return name;
	}
	

}
