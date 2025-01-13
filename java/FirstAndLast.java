import java.util.*;


public class FirstAndLast{


public static void main(String args[]){


String str="god is great";
char ch;
String str2="";
str=str.trim()+" ";
str2=Character.toUpperCase(str.charAt(0))+"";
for (int i=1;i<str.length();i++){

ch=str.charAt(i);
if(ch==' '&&i!=(str.length()-1))
{
str2=str2+ch;
str2=str2+Character.toUpperCase(str.charAt(i+1));
i=i+1;
}
else
str2=str2+ch;


}

System.out.println(str2);


}





}
