import java.util.*;

public class List {

	private ArrayList<Card> list = new ArrayList<Card>();
	private String title;
	
	public List (String title) {
		this.title = title;
	}

	//Getters and setters
	
	public ArrayList getList() {
		return list;
	}

	public String getTitle() {
		return title;
	}

	public int getSize() {
		return list.size();
	}

	public void setTitle(String title) {
		this.title = title;
	}

	//add card to list
	
	public void addCard(Card card) {
		list.add(card);
	}

	//remove card
	
	public void removeCard(Card card) {
		list.remove(card);
	}

	//searches list for card by Title
	//parameter is a string, the title you want to search for
	//returns card object if found, null if not
	//
	public Card searchByTitle(String stitle) {
		Card temp = null;

		for(Card card: list) {
			if(card.getTitle().equalsIgnoreCase(stitle)) {
				temp = card;
			}
		}

		return temp;
	}
	
	//searches list for card by number
	//parameter is the number you want to search for
	//returns card if found, null if not found
	
	public Card searchByNumber(int snum) {
		Card temp = null;

                for(Card card: list) {
                        if(card.getNumber() == snum) {
                                temp = card;
                        }
                }

                return temp;
	}

	//Sorts list by Card number
	
	private void sortByNumber() {

	}

	//Sorts list by card creation time
	
	private void sortByTime() {

	}

	//Sorts by Card title
	
	private void sortByTitle() {

	}

	public String toString() {
		String temp = title;

		for (Card card:list) {
			temp = temp+""+card.toString()+"\n";
		}

		return temp;
	}

	public boolean isEmpty() {
		return list.isEmpty();
	}

	public void removeAll() {
		list.clear();
	}
	

}
	


