# Traffic Lights F

The hint we are given is "Physical Vapor Deposition". Which doesn't make much sense.

However, given that the first letter of each word is capitalized, it might be "PVD".

Some googling indicates that "Pixel Value Differencing" is indeed a type of image stenography - so it seems like we are on the right track.

## Software

Poking around a bit on github, we find this open source python script for extracting PVD data from an image:

https://github.com/sepidehsayad/PVD-method-steganograpghy/blob/master/extractdata.py

Looking at it, we just have to change the name of the file it is opening - oh, and there's some print statements commented out at the bottom - let's uncomment those too.

```bash
$ python extractdata.py
Traceback (most recent call last):
  File "extractdata.py", line 66, in <module>
    di=calculate_di(pixel_value_hostimage)
  File "extractdata.py", line 11, in calculate_di
    list_of_di+=[abs(pixels_value[i]-pixels_value[i+1])]
TypeError: unsupported operand type(s) for -: 'tuple' and 'tuple'
```

Hmmm... Seems like it's reading pixel_values, but instead of only having a single value we have a tuple.

What if we convert the image to greyscale first:

```python
from PIL import Image
import math
host_image = Image.open('TrafficLightsF.png','r').convert("L") #open image
```

```
$ python extractdata.py
[3, 2, 2, 6, 2, 0, 4, 2, 3, 2, 4, 4, 2, 5, 4, 4, 2, 5, 4, 5, 2, 0, 6, 2, 2, 5, 6, 6, 1, 1, 5, 4, 3, 4, 2,
 3, 3, 5, 5, 3]
['11', '10', '10', '110', '10', '0', '100', '10', '11', '10', '100', '100', '10', '101', '100', '100', '1
0', '101', '100', '101', '10', '0', '110', '10', '10', '101', '110', '110', '1', '1', '101', '100', '11',
 '100', '10', '11', '11', '101', '101', '11']
```

Now we are getting somewhere. After looking at this sequence for a while, I couldn't get anything meaningfull out of it. However, I was convinced I was on the right track.

Thinking about it, it doesn't *really* make sense to convert to greyscale before trying to extract the message, because that would have made it very difficult to encode (proper luminance calculation is a weighted sum of linear rgb values).

What might make sense, however, is that each colour channel (R,G,B) encodes it's own information.

Let's try it.

```python
host_image = Image.open('TrafficLightsF.png','r')#.convert("L") #open image 

pixel_value_hostimage = list(host_image.getdata(0)) #0 = R, 1 = G, 2=B
```

### Red
```
$ python extractdata.py
[3, 1, 4, 6, 6, 1, 4, 1, 3, 1, 6, 7, 5, 5, 6, 7, 3, 2, 0, 3, 2, 1, 6, 4, 1, 4, 6, 7, 3, 0, 6, 3, 3, 4, 4, 5, 7, 5, 5, 0]
['11', '1', '100', '110', '110', '1', '100', '1', '11', '1', '110', '111', '101', '101', '110', '111', '11', '10', '0', '11', '10', '1', '110', '100', '1', '100', '110', '111', '11', '0', '110', '11', '11', '100', '100', '101', '111', '101', '101', '0']
```

Ok, this is a little different. What about G and B?

### Green

```
$ python extractdata.py
[3, 4, 0, 7, 0, 0, 6, 3, 3, 3, 4, 3, 1, 5, 4, 4, 2, 7, 6, 7, 2, 0, 6, 0, 2, 7, 6, 6, 1, 1, 5, 4, 3, 5, 2, 3, 1, 5, 7, 5]
['11', '100', '0', '111', '0', '0', '110', '11', '11', '11', '100', '11', '1', '101', '100', '100', '10', '111', '110', '111', '10', '0', '110', '0', '10', '111', '110', '110', '1', '1', '101', '100', '11', '101', '10', '11', '1', '101', '111', '101']
```

### Blue

```
$ python extractdata.py
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
```

## Decoding

The fact that blue is all zeros has to be intentional, and is further evidence that we are on the right track.

Let's look at the red channel first.

```
3, 1, 4, 6, 6, 1, 4, 1, 3, 1, 6, 7, 5, 5, 6, 7, 3, 2, 0, 3, 2, 1, 6, 4, 1, 4, 6, 7, 3, 0, 6, 3, 3, 4, 4, 5, 7, 5, 5, 0
```

Well, this sequence of numbers ranges from 0 to 7, which means if each of these numbers was represented with the same number of bits, we'd need at least 3 bits. So what happens if we write each of these numbers with using *exactly* 3 bits?

```
'011', '001', '100', '110', '110', '001', '100', '001', '011', '001', '110', '111', '101', '101', '110', '111', '011', '010', '000', '011', '010', '001', '110', '100', '001', '100', '110', '111', '011', '000', '110', '011', '011', '100', '100', '101', '111', '101', '101', '000'
```

Ok, now if we cram them all together into groups of 8 bits?

```
01100110 01101100 01100001 01100111 01111011 01110111 01101000 00110100 01110100 00110011 01110110 00110011 01110010 01011111 01101000
```

Well, we know from [BinaryWordSearch](../../Miscellaneous/BinaryWordSearch/readme.md) that "flag{" starts with the sequence `0110 0110 0110`, so this is looking promising.

Now, how about that green channel? Once again, it only contains the numbers 0 through 7 - so 3 bits it is.

```
'011', '100', '000', '111', '000', '000', '110', '011', '011', '011', '100', '011', '001', '101', '100', '100', '010', '111', '110', '111', '010', '000', '110', '000', '010', '111', '110', '110', '001', '001', '101', '100', '011', '101', '010', '011', '001', '101', '111', '101'
```

```
01110000 01110000 00110011 01101110 00110011 01100100 01011111 01110100 00110000 01011111 01100010 01101100 01110101 00110011 01111101
```

I think you can guess what you need to do now.

<details><summary>Spoiler (Output Includes Flag)</summary>
<p>

Putting the red and green channels together is missing exactly 1 character where the two strings meet; I'm guessing there just wasn't quite enough room in the image to encode that character. It was pretty easy to fill in manually (Thanks Malikaz for pointing out the problem).

```
flag{wh4t3v3r_h4pp3n3d_t0_blu3}
```

</p>
</details>

---
Andrew Steadman
