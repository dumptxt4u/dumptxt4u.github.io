import java.util.*;
public class PigLatin{

public static String piglatin(String str){
{
char ch;
for(int i=0;i<str.length();i++)
{
ch=str.charAt(i);
if(ch=='a'||ch=='i'||ch=='e'||ch=='o'||ch=='u')
return str.substring(i)+str.substring(0,i)+"ay";
}
}
return "";
}

public static void main(String args[]){



char ch;
String word="";
String str="xaeiou xaeiou haeiou";
str=str+" ";
for (int i=0;i<str.length();i++)
{

ch=str.charAt(i);
if (ch==' ')
{

System.out.println(piglatin(word));
word="";
}
else
word=word+ch;

}



}



}
