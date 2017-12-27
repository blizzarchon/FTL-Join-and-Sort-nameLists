# FTL modding: Join and Sort nameLists
For use with FTL: Faster Than Light.

Given a names.xml-formatted file, this program join all the 'male' and 'female' nameLists in the file into two lists, one for each gender. The names in the nameLists are sorted alphabetically, and then outputted into a text file, ready as the names.xml file for use in a mod.

***History***

**Note:** May not be completely correct, needs more testing.

Originally, I made it so nameLists only joined together if they had the same gender (e.g. sex='male' or sex='female'). However, when combining, I found I hit a 60/40 male-to-female ratio, with many names. I thought if I made identical nameLists, I wouldn't have to deal with the mess of finding a perfect 50/50 male-to-female ratio of names, both nameLists being exactly the same. Good idea, right?

Wrong. Unfortunately, it doesn't actually work that way. FTL assigns each unique name one gender, which is decided by the nameList the name is in. If the name appears in more than one nameList, whichever nameList it's in is furthest down in the file, the gender that nameList has is the one the name gets.

When you see the name in-game, whichever "assigned" gender goes with the name, that gender appears, not the other. So if you had the name "Bones" and the last nameList it was in is female, "Bones" would always appear as a female human in the hangar, not male.
