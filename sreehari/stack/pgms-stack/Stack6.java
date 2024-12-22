// Java code to demonstrate search() method 
import java.util.*; 

public class Stack_Demo { 
	public static void main(String[] args) 
	{ 

		// Creating an empty Stack 
		Stack<String> STACK = new Stack<String>(); 

		// Stacking strings 
		STACK.push("Geeks"); 
		STACK.push("4"); 
		STACK.push("Geeks"); 
		STACK.push("Welcomes"); 
		STACK.push("You"); 

		// Displaying the Stack 
		System.out.println("The stack is: " + STACK); 

		// Checking for the element "4" 
		System.out.println("Does the stack contains '4'? "
									+ STACK.search("4")); 
		// Checking for the element "Hello" 
		System.out.println("Does the stack contains 'Hello'? "
									+ STACK.search("Hello")); 

		// Checking for the element "Geeks" 
		System.out.println("Does the stack contains 'Geeks'? "
									+ STACK.search("Geeks")); 
	} 
} 

