# FTL modding: Join and Sort nameLists
For use with FTL: Faster Than Light.

Given a names.xml-formatted file, this program join all the names in all nameLists in the file into one list, regardless of gender. The names in the list are sorted alphabetically, and then outputted into a text file, ready as the names.xml file for use in a mod.

**Identical nameLists "problem"**

FTL apparently assigns each unique name one gender, which is decided by the nameList the name is in. If the name appears in more than one nameList, whichever nameList it's in is furthest down in the file, the gender that nameList has is the one the name gets.

When you see the name in-game, whichever "assigned" gender goes with the name, that gender appears, not the other. So if you had the name "Bones" and the last nameList it was in is female, "Bones" would always appear as a female human in the hangar, not male.

So... it would appear two identical nameLists is impossible because names must be unique.

**Workaround**

However, there is a workaround: make every name in one of the two nameLists have a single zero-width space at its end. This makes the game think the names in said nameList are different from the names in the other nameList, and therefore, lets both male and female humans have the same name.

Since the zero-width space is literally invisible, this works, unlike the space character, which doesn't get trimmed.

**Last thought**

Apparently, the ratio of male-to-female names within nameLists is directly reflected in-game (names.xml determines occurrence, not hardcoded 50/50 equal chance). Assumedly for non-humans, gender is ignored and the chance of any name is equal.
