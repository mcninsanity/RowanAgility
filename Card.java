import java.time.*;
public class Card {

	private String title;
	private int number;
	private int priority;
	private int dificulty;
	private LocalTime time;

	public Card(String title, int number, int priority, int dificulty) {
		this.title = title;
		this.number = number;
		this.priority = priority;
		this.dificulty = dificulty;
		time = time.now();

	}

	//Getters and setters for each field
	public String getTitle() {
		return title;
	}

	public int getNumber() {
		return number;
	}

	public int getPriority() {
		return priority;
	}

	public int getDificulty() {
		return dificulty;
	}

	public LocalTime getTime() {
		return time;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public void setNumber(int number) {
		this.number = number;
	}

	public void setPriority(int priority) {
		this.priority = priority;
	}

	public void setDificulty(int dificulty) {
		this.dificulty = dificulty;
	}
	
	public String toString() {
		return ("Title: "+title+", Number: "+number+", Priority: "+priority+", Dificulty: "+dificulty+", Time: "+time.toString());
	}
}

