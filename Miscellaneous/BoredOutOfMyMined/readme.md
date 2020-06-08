# Bored Out of My Mined

## We are given the following description: 
This top Notch challenge will craft some difficulty for some.

DM @JC01010 on discord if you have issues concatenating the flag.

You do not need the the game for this challenge

## We are given the following hint:
Part 1 should lead to 2, 2 to 3, 3 to 4.

What's an NBT viewer?

## The Challenge

For this challenge we had to use an NBTViewer to view the contents of a minecraft world file. The flag was broken up in to parts that was hidden/encoded in various parts of the file. Since whenever there is an issue, step 1 is to check the logs, we opted to check the log file. The first part of the flag was located in the logfile, and said by a user:

<details>
Note: Found inside log file by searching for "flag"
[2:16:52] [Server thread/INFO]: <Herobrine> pt 1: flag{d0_5
  
[2:16:52] [Server thread/INFO]: <Herobrine> Tell me about myself!
flag{d0_5
</details>

Now that we have the hint for the next part "Tell me about myself!", we should investigate the user files of the person who said this. In this case, we found it under the player file in the recipes area.
<details>
minecraft:tell me about the icon!
  
minecraft:7@R5_R (pt 2)
</details>

Since the hint from the last step says "tell me about the icon!", we should look at icon.png. I opened the file but nothing looked out of the ordinary. Next step was to exiftool the file. There was some gibberish in some of the fields, and the description field looked like BASE64, so we opted to decode this and found the next part of the flag.
<details>
Finally, tell me about the level - perhaps, the command length?
  
pt 3: 0Tat3?_ 
</details>
Finally, we found the maxCommandChainLength under GameRules in the level.dat file. It's binary, but we had trouble decoding it. It turns out we needed to break up the characters individually and "guess" a few. We are given the string <details>11211652581215153161125</details> and after breaking it up we get <details>112 116 52 58 121 51 53 161 125</details> which decodes to the last part of the flag. 
<details>
pt4:y35¡}
</details>

## Answer 
Putting each part together, we get the following. 
<details><summary>Spoiler (Output Includes Flag)</summary>
<p>
```
flag{d0_57@R5_R0Tat3?_y35¡}
```

</p>
</details>
