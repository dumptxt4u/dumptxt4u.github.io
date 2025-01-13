import string
str=input("Wnter the string")
for ch in string.ascii_lowercase:
	count=0
	for c in str:
		
		if ch==c:
			count=count+1
	if count !=0:
		print(c," occurs ",count ," times ")
