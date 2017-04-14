package dypl_week3;

public class Paper extends Weapon {
	
	static String name = "paper";
	
	public Result attack(Weapon weapon) {
		return weapon.eval(this);
	}
	
	public Result eval(Rock weapon) {
			return Result.lose;
	}
	
	public Result eval(Scissors weapon) {
			return Result.win;
	}
	
	public Result eval(Paper weapon) {
			return Result.tie;
	}

	public static String getClassName() {
		return name;
	}
	
	@Override
	public String getName() {
		return name;
	}
	
	

}
