#
#  11 ciphertexts, encrypted with the same one time pad key 
#  task: decrypt the last ciphertext in the below list
#  
#  Author: Matjaž Madon




#string of the ciphertexts, in hexadecimal representation
ciphers = ["7218eb424325d04c7c266b20b9a790ba64da75998854b357d7aa9e0b34173cbb4b42b2873534be574120eef459ee6197","6e15a2540d26cc156e265133a8a58ab674d63b9ac750b60a","6915ae074421cc5c7c727e36f8b08cb273937892cd5db44d99afdf082d0668e24d59e0d33e3df1464520a6f157f22ccd6614abe6bab6abbb1584f41ddec1a709f84034bf872cc2","7412a94849369f5960707e21f8a5c4a36ed43b89cd5da84d99afdf0b31023bef4b4ff9dd","6d15ae490d27da1567677f72acabc4a36ed07597cb1cb54ad7bc970278102dfa4144bed33534be455526f6e945e460c02e01fef9ffbceaa11e84fa1c91caf305ef5b62a68c249c18476259c4ea3d41662a","6915ae07452edb5b28723b3ab9a0c4bb62c13b9ddd4cfa4b91e89c083e142dfe0e0cf39d3971ea5d4120a6eb57e569997a19e2e3b8bcabae16c8b306d9c0a71ae55b31b3c7","7214bf07402a9f4266727372a1ab91a127c37e8a884fb24585a3de","6e15ae074a3dca536926743ebce489b26993689fdc1cb34ad7bc9702781029f8490cfd957d25f6500036e7ef42a17fd16101abeaadbae6ad16cdfd1591d1e84de2402fa58c278a5443360a8ce9725d616be1da9eced29444b3a65ebe0ec4e4b93e247934be0c73249663420134","6e0fbe53456fd65b2f677f24bdb690ba74da7599885db440d7ac9609370129ee505fb2843425f615533fe7f253e363d87c15f8adb7aefdaa5ac9e611d985ee03aa4a2dbb8424825a","6d18eb4f4c39da1576696e3cbfe48fba63c03b89c053fa4b91bc9a09780529f7490cfb9d293ebe5a5526a6f459ee61996f05abe3b6a8e3bb5ac2fc0091d3e61fe34637a5c9398915512a4497ac3b406168fbce92c495db52abe948f01585e3b378257d71f1093f3c8a745b5c","7b0eeb4f486fc85466727e36f8a28ba127c7739b884fb24b80ad8d472c1d68ec435effdf7d39fb154e3bf2ef55e468997a19eaf9ffa7eeef19cbe61ed585ef08eb5b62a1883f890602264285e2354b2270ebc78bcf809a45b2f45ab0"]

#First I convert the ciphertexts from hex to iso-latin character representation 
#You have to first find out how were the strings encoded (could also be utf-8)
cp = []
for c in ciphers:
  cp.append(bytes.fromhex(c).decode("ISO-8859-1"))


#the function for xor-ing two strings
def strxor(a, b): 
 if len(a) > len(b):
  return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
 else:
  return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


#First method for breaking the ciphertexts, the method of xor-ing 
#all pairs of ciphertexts, and considering the fact, that when 
#xor-ing a space with a lowercase letter, we obtain an uppercase letter
spaces = []
crib = []
for i in range(11):
 spaces.append([])
 crib.append("")


for i in range(11):
 for j in range(48): 
  spaces[i].append(0)
#creating a list of numbers with which i will count the 
# number of occurances of capitalised letters, for the 

for i in range(11): 
 for j in range(11): 
   if i != j: 
    for k in range(20): 
      if(ord(strxor(cp[i],cp[j])[k]) < 91 and ord(strxor(cp[i],cp[j])[k]) > 64):
       spaces[i][k] += 1
#counting the number of capital letters in the xors for each letter in the line


#note: we can change the tolerance in proportion to the # of strings
tolerance = 5
for i in range(11):
  for j in range(48): 
      if(spaces[i][j] > tolerance ):
        crib[i] = crib[i] + " "
      else:
        crib[i] = crib[i] + "."
#if the occurance of capital letters in a particular place
#is greater than 5, it is almost certain that there will 
# be a whitespace

for i in range(11): 
  print(crib[i] + " : " + str(i))
#printing out the results of the first method, we can suspect then, the 
#lengths of words


#After looking at the output of first method, guess some word at the 
#beginning of a sentence, and use it as a crib

#look at the shortest lengths of words as those are gonna be the easiest 
#to guess, we can look up the most frequent words of length 2, 3 .. and so on
# and try using them as cribs in the first try, once we recover even a little from
# a pair of ciphertexts, the excercise becomes almost trivial, since 
# we only need create a corresponding key to the ciphertext, and 
# use the key against other ciphertexts 

cr = "We "
print(strxor(strxor(cp[0],cp[9]),cr))

#after some tries, i get that the word "As " is a 
#working crib (xoring it also with other lines)
#so i will proceed by creating a key on the 10th line and 
#trying to expand from there 

crib = "We have young kids who often walk into our room at night for various reasons including clowning "
#we dont yet know if the crib corresponds to PT in cp[0] or cp[9], so we try both, in the guess var
guess = cp[9]
key = strxor(guess,crib)
for i in range(11):
  print(strxor(cp[i],key) + "  :" + str(i))


#i can see from the printed list, that the 4th line starts
#with "Whe", and I assume that is the word "When", I can 
#also add a whitespace since from the previous method it 
#should be a 4 letter word in the beginning as seen from 
#the print of the previous method 
#So i change the key to strxor(cp[4], "When ") and proceed
#from here on, the procedure is the same, 
#for example the third index, starts with "Nobod", and I
#can assume that it starts with "Nobody" and a 
#whitespace (as seen from the previous method also the #length matches)

#From here on, the procedure remains the same, I keep 
#changing the key, and look to expand the key more and
#more, untill i finish the sentence. 

#The last key i had to use was:
#strxor(cp[9],"We have young kids who often walk into #our room at night for various reasons including #clowning ")
#After this one, I know for sure I recovered the whole 
#eleventh sentence since it is shorter than the 
#9th sentence, this finishes the excercise.
  








