import java.util.*;
public class TestDriver
{

	public static void main(String args[])
	{
	   Scanner keyb = new Scanner(System.in);
	   
	   List list = new List("Test");
	   boolean running = true;	  

	   while(running)
	   {
	      menu();
	      System.out.print("Enter your selection now: ");
	      int option = keyb.nextInt();
	      keyb.nextLine();

	      switch(option)
	      {
		case 8:
		   System.out.println("Exiting program...Good Bye");
		   running = false;
		   break;
		case 1:
		   System.out.println("You are now inserting a Card  into the list.");
		   System.out.print("\t Enter Card title: ");
		   String title = keyb.nextLine();
		   System.out.print("\t Enter Card number: ");
		   int num = keyb.nextInt();
		   System.out.println("\t Enter Card dificulty: ");
		   int dificulty = keyb.nextInt();
		   System.out.println("\t Enter Card Priority: ");
		   int priority = keyb.nextInt();
		   keyb.nextLine();
		   Card temp = new Card(title, num, priority, dificulty);
		   list.addCard(temp);
		   System.out.println("Card Added: "+temp.toString());
		   
		   break;
		case 2:
		if (list.isEmpty())
		{
		   System.out.println("The list is empty");
		}
		else
		{
		   System.out.print("\t Enter Title of card you want to remove: ");
	 	   String remTitle = keyb.nextLine();
		   keyb.nextLine();
		   Card temp1 = list.searchByTitle(remTitle);
		if(temp1 == null)
		{
		   System.out.println("Card Not found!");
		}
		else
		{
		   System.out.println("Card "+temp1.toString()+" removed from list.");
		   list.removeCard(temp1);
		}
		}
		   break;
		case 3:
		   if (list.isEmpty()) {
			   System.out.println("List is empty.");
		   } else {
		   	System.out.print("\t Enter Card Number to remove: ");
		   	int remNum = keyb.nextInt();
		   	keyb.nextLine();
			Card temp2 = list.searchByNumber(remNum);
	 	if (temp2 == null)
		{
		   System.out.println("Card not found!");
		} 
		else
		{
		  System.out.println("Card "+temp2.toString()+" removed from list..");
		  list.removeCard(temp2);
		}
		   }	
		  break;
		case 4:
		   list.removeAll();
		   break;
		case 5:
		if (list.isEmpty())
		{
		   System.out.println("List is empty.");
		}
		else
		{
		   String output = list.toString();
		   System.out.println("\t"+output);
		   System.out.println(list.getTitle()+" has "+list.getSize()+" cards");
		}
		   break;
		case 6:
		   if(list.isEmpty()) {
			   System.out.println("List is empty!");
		   } else {
			System.out.print("\t Enter Title of card you want to find: ");
                   	String fTitle = keyb.nextLine();
                   	keyb.nextLine();
                   	Card temp3 = list.searchByTitle(fTitle);
		  if(temp3 == null)
                  {
                        System.out.println("Card Not found!");
                  }
                  else
                  {
                        System.out.println("Card "+temp3.toString()+" found.");
                  }
                }
                   break;
		case 7:
		     if(list.isEmpty()) {
                           System.out.println("List is empty!");
                   } else {
                        System.out.print("\t Enter Number of card you want to find: ");
                        int fNum = keyb.nextInt();
                        keyb.nextLine();
                        Card temp4 = list.searchByNumber(fNum);
                  if(temp4 == null)
                  {
                        System.out.println("Card Not found!");
                  }
                  else
                  {
                        System.out.println("Card "+temp4.toString()+" found.");
                  }
                }

         }
	   }
	}

	private static void menu()
	{
	   System.out.println();
	   System.out.println("Select from the following menu:");
	   System.out.println("\t 1. Insert Card to list.");
	   System.out.println("\t 2. Remove Card by Title");
	   System.out.println("\t 3. Remove Card by number");
	   System.out.println("\t 4. Clear list.");
	   System.out.println("\t 5. Print size and content of list.");
	   System.out.println("\t 6. Search by Title.");
	   System.out.println("\t 7. Search by Number.");
	   System.out.println("\t 8. Exit program.");
	}





}
