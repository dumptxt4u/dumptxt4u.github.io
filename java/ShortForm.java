public class ShortForm{


public static void main(String args[]){



String str="Mohandas karmchand Gandhi";

String str1;
int index ,lastindex;
str1=str.charAt(0)+".";
index=str.indexOf(' ');
lastindex=str.lastIndexOf(' ');

str1=str1+str.charAt(index+1)+".";
str1=str1+str.substring(lastindex+1);
System.out.println(str1);


}




}
