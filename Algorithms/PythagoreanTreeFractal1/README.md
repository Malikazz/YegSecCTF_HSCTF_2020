# Pythagorean Tree Fractal 1

## Observations

Stage 1: 1 rectangle

Stage 2: 1 + 2 = 3 rectangles (*NOT SHOWN*)

Stage 3: 1 + 2 + 4 = 7 rectangles

Stage 50: ? rectangles

## Pattern

For stage `n`, we have `2^n - 1` rectangles. So, for `n=50` there are `2^50 - 1` rectangles.

<details><summary>Spoiler (Output Includes Flag)</summary>
<p>

It's now pretty obvious that the `4`s that we didn't know what to do with should be literally the number `4` in the final string (0x34).

```
flag{1125899906842623}
```

</p>
</details>