/*Progrm to capitalise a string

Program number 1 */



import java.util.*;
public class UpperCase

{



public static void main(String args[]){


Scanner s=new Scanner(System.in);
String str;
System.out.println("Eter a sentence");
str=s.nextLine();

System.out.println("String before Capitalisation"+str);

System.out.println("String After Capitalised"+str.toUpperCase());

}


}
