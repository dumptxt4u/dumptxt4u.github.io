public class SwapName{




public static void main(String args[]){



int index,lastindex;

String str="Subash Chnadra Bose";
String str2="";


index=str.indexOf(' ');
lastindex=str.lastIndexOf(' ');


str2=str.substring(lastindex)+" ";
str2=str2+str.substring(index+1,lastindex)+" "+str.substring(0,index);
System.out.println(str2);






}








}
