str=input("Enter the string")
print(len(str))
k=0
for ch in str:
	
	if ch=='a':
		print(" "+str[k+1].upper(),end="")
		
		
	else:
		print(str[k],end="")
	k=k+1
				







