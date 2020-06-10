### legend
`c = 0, c# = 1, d = 2, d# = 3, e = 4, f = 5, f# = 6, g = 7, g# = 8, a = 9, a# = a, b = b`

### Melody notes
`g#f#, ac, g#c#, g#g, a#d#, a#c#, ec, aa, bg, e, af#, ed#, bg, aa#, ed#, af#, a#c#, bg, ac# aa, ag, ec#, g#d#,e ac, a#f`

What should happen to the single notes? They only appear in the message as an `e` (aka `4`)? *Let's ignore those for now*.

The remaining pairs could appear in either order. IE: `g#f#` could be `6 8` or it could be `8 6`.

There are 12 symbols here - which leads us to believe this is likely a message encoded in base 12.

This is the array of symbols in one possible order order:

`68 09 18 78 3a 1a 40 99 7b 4 69 34 7b a9 34 69 1a 7b 19 99 79 14 38 4 09 5a`

And here it is with the order of each symbol flipped:

`86 90 81 87 a3 a1 04 99 b7 4 96 43 b7 9a 43 96 a1 b7 91 99 97 41 83 4 90 a5`

We know in hex that ascii string "flag{" is `66 6C 61 67 7B`. Doing some math manually, `86` in base12 is `8*12 + 6 = 102`. 102 is `6*16 + 6`, ie: `0x66` in hex.

The letter 'a' in base12 is `81`, the number '0' is `40`, and the symbol '_' is `7B`. So we likely want to choose the ordering where the numbers are either `>81`, `>40`, or `=7B`

Likely symbol order (again, ignoring the 4's):

`86 90 81 87 A3 A1 40 99 7B 4 96 43 7B 9A 43 96 A1 7B 91 99 97 41 83 4 90 A5`

We can now use the `bc` command to turn this base12 sequence into hex (base16):

```bash
$ echo "obase=16;ibase=12;86;90;81;87;A3;A1;40;99;7B;4;96;43;7B;9A;43;96;A1;7B;91;99;97;41;83;4;90;A5" | bc
66
6C
61
67
7B
79
30
75
5F
4
72
33
5F
76
33
72
79
5F
6D
75
73
31
63
4
6C
7D
```

This is now (for the most part) a simple ascii encoded string represented in hex.

<details><summary>Spoiler (Output Includes Flag)</summary>
<p>

It's now pretty obvious that the `4`s that we didn't know what to do with should be literally the number `4` in the final string (0x34).

```
flag{y0u_4r3_v3ry_mus1c4l}
```

</p>
</details>

---
Andrew Steadman