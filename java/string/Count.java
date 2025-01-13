import java.util.*;
public class Count{


public static void main(String args[]){

Scanner sc=new Scanner(System.in);
int i,count=0;;
String str;
System.out.println("Enter the string");

str=sc.nextLine();
if (str.charAt(0)=='a')
count=1;
for(i=1;i<str.length();i++)
if(  (str.charAt(i)==' ' &&str.charAt(i+1)=='a'))
//System.out.println("Car ia a nice car");
count=count+1;

System.out.println("Number of words starting with a is "+count);


}



}
