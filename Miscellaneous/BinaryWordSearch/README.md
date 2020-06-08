# Binary Word Search

Given a 1000x1000 px png image, we need to search for the flag. We know the flag starts with "flag{", so we can search for that. We are told it may occur horizontal, vertically, or diagonally in either "forward" or "backwards" directions. We are told that "0"s are black and "1"s are white.

For this task I used "octave", which is an open-source matlab implementation. You could also use python.

## Search word

Let's define what we are searching for. "flag{" in hex is `66 6C 61 67 7B`, or:

```
01100110 01101100 01100001 01100111 01111011
```

in binary.

## Loading the image

To load the image into octave, use only the first color channel, and represent the values as floating point numbers, use the following command:

```matlab
I=imread("BinaryWordSearch.png")(:,:,1)*1.0;
```

This gives us a 1000x1000 matrix of numbers that are either `0.0` or `1.0`.

## Defining the searchword

```matlab
flag=[0 1 1 0 0 1 1 0 0 1 1 0 1 1 0 0 0 1 1 0 0 0 0 1 0 1 1 0 0 1 1 1 0 1 1 1 1 0 1 1];
```

## The task

What we need to do is search this 1000x1000 matrix for a particular sequence of bits. One way to do this is to look for the location of the peak [cross-correlation](https://en.wikipedia.org/wiki/Cross-correlation) between our searchword and our search space.

According to Wikipedia:
> [Cross-Correlation] is commonly used for searching a long signal for a shorter, known feature.


In order to maximize the cross-correlation of our signals, we need to convert their representation from unipolar (`0`s and `1`s) to bipolar (`-1`s and `1`s). We do this by multiplying both of our signals by `2` and subtracting `1` (This causes the `0`s to become `-1`).

```matlab
IB = 2*I - 1;
flag = 2*flag - 1;
```

Now, we need to define all the various ways our flag may appear: horizontal forwards, horizontal backwards, vertical downwards, vertical upwards, diagonal down-to-the-right, diagonal up-to-the-right, diagonal down-to-the-left, and diagonal up-to-the-left.

```matlab
flag_lr = flag;
flag_rl = fliplr(flag);
flag_tb = flag';
flag_bt = flipud(flag');

flag_tlbr = diag(flag);
flag_bltr = flipud(diag(flag));
flag_trbl = fliplr(diag(flag));
flag_brtl = flipud(fliplr(diag(flag)));
```

The flag (prefix) itself is 40 digits long, and consists of symbols of "unit" energy (`1` and `-1`). Therefore it's peak autocorrelation (the cross-correlation of the signal with itself) value is equal to the signal's total energy: `40`.

If we cross-correlate all of the above signals with our image and find spots where the cross-correlation is also `40`, then we can identify the regions of the image matrix that contains those exact sequence of digits.

## Cross-correlation

For discrete, real-valued, deterministic signals the cross-correlation of `f[n]` and `g[n]` is `f[-n] * g[n]` (where `*` denotes convolution). IE: convolve with a *reversed* sequence.

```matlab
ccorr2 = @(f,g) conv2(f, flipud(fliplr(g)));

X_lr = ccorr2(IB, flag_lr);
X_rl = ccorr2(IB, flag_rl);
X_tb = ccorr2(IB, flag_tb);
X_bt = ccorr2(IB, flag_bt);

X_tlbr = ccorr2(IB, flag_tlbr);
X_bltr = ccorr2(IB, flag_bltr);
X_trbl = ccorr2(IB, flag_trbl);
X_brtl = ccorr2(IB, flag_brtl);
```

> Note: Don't forget about reversing the sequence. I spent at least an hour knowing that there should be a match but iterating in the wrong direction after finding it.

Let's see if any of those correlations resulted in anything interesting:

```matlab
>> max(max(X_lr))
ans =  30
>> max(max(X_rl))
ans =  30
>> max(max(X_tb))
ans =  30
>> max(max(X_bt))
ans =  30
>> max(max(X_tlbr))
ans =  28
>> max(max(X_bltr))
ans =  40
>> max(max(X_trbl))
ans =  28
>> max(max(X_brtl))
ans =  30
```

**BOOM** Looks like we have at least one "hit" in the diagonal direction going from bottom-left up to top-right. Let's find out more about it.

```matlab
>> [r,c]=find((X_bltr==40)*1.0)
r =  838
c =  233
```

We note that there is *EXACTLY* one place where the cross-correlation is `40` - which makes things easy.

Here, `(838, 233)` is the index of the peak value of our cross-correlation matrix (which has a size of `1039x1039`). If we relate it back to our original inputs, than we could say `(838, 233)` is the position of the bottom right hand corner of the `40`x`40` submatrix where our flag matrix and image matrix overlap (See Table).

|       	    | 194 	| 195	| 196 	| (...) 	| 231 	| 232 	| 233	|   	|
|-------	    |-----	|-----	|-----	|-------	|-----	|-----	|-----	|---	|
| **799**   	|⸻  |⸻  | ⸻ | ⸻     |⸻  |⸻  | 1   	|   	|
| **800**   	| \|  	|     	|     	|       	|     	| 1   	| \|  	|   	|
| **801**   	| \|  	|     	|     	|       	| 0   	|     	| \|  	|   	|
| **(...)** 	| \|  	|     	|     	| (...) 	|     	|     	| \|  	|   	|
| **836**   	| \|  	|     	| 1   	|       	|     	|     	| \|  	|   	|
| **837**   	| \|  	| 1   	|     	|       	|     	|     	| \|  	|   	|
| **838**   	| *0*   	|⸻  |⸻  |⸻  |⸻  |⸻  | X   	|   	|


Therefore, we should expect the message to start at index `(838, 194)`, continue on `(837, 195)`, and so on and so forth.

> Note: Octave matrices and vectors are 1-indexed, not 0-indexed.

If we pull out the diagonal vector, of length `400`, starting at position `(838, 194)`, we should get enough bits to cover the entire flag message.

```matlab
>> char('0' + I(sub2ind(size(I), 838:-1:(838-400+1), 194:(194+400-1))))
ans = 0110011001101100011000010110011101111011011101000110100101101110011110010111010101110010011011000010111001100011011011110110110100101111011110010011100101100110011100110110101101111001011010000011011001111101111000001011011101000101010101110011100101000110011010011111011110001101011000110110101000000100111110011001010101111010001110010000011010011011001000000101000000001111011010110001011101101010
```

> Note: Here we've used `sub2ind` to convert rows and columns into a linear index, pulled the values of those indexes out of our image matrix `I`, added the character value `'0'`, and then created a character array.

From here, it's pretty simple to turn this binary bit array into an ASCII string.

<details><summary>Spoiler (Output Includes Flag)</summary>
<p>

```
flag{tinyurl.com/y9fskyh6}(...)
```

</p>
</details>

---

Andrew Steadman