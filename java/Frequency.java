import java.util.*;


public class Frequency{




public static void main(String args[]){


Scanner sc=new Scanner(System.in);
char ch,ch1;
int count=9;
String str;
System.out.println("Enter the String");
str=sc.nextLine();

for (ch='a';ch<='z';ch++ )
{

count=0;
for(int i=0;i<str.length();i++)
{ch1=str.charAt(i);
if (ch==ch1)
count++;
}
if(count!=0)
System.out.println(ch+" occurs "+count +" times  ");
}






}



}
