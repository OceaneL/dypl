package dypl_week3;

public enum Result {
	lose ("Your opponent wins!"),
	win ("You win!"),
	tie ("It's a tie!");
	
	protected String sentence;
	
	private Result(String sentence) {
		this.sentence = sentence;
	}	
}
