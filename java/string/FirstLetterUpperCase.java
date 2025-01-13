import java.util.*;
public class FirstLetterUpperCase
{


public static void main(String args[]){

char ch;


String str,str1="";
Scanner sc=new Scanner(System.in);
System.out.println("Enter the string");

str=sc.nextLine();
for(int i=0;i<str.length();i++)
{

ch=str.charAt(i);
if(ch==' ')
{
i=i+1;
ch=str.charAt(i);
if (ch=='a')
str1=str1+" "+Character.toUpperCase(ch);
else
str1=str1+" "+ch;
}
else
str1=str1+str.charAt(i);

}
System.out.println(str1);



}

}
