# XORed

## Challenge

```
I was given the following equations. Can you help me decode the flag?
Key 1 = 5dcec311ab1a88ff66b69ef46d4aba1aee814fe00a4342055c146533
Key 1 ^ Key 3 = 9a13ea39f27a12000e083a860f1bd26e4a126e68965cc48bee3fa11b
Key 2 ^ Key 3 ^ Key 5 = 557ce6335808f3b812ce31c7230ddea9fb32bbaeaf8f0d4a540b4f05
Key 1 ^ Key 4 ^ Key 5 = 7b33428eb14e4b54f2f4a3acaeab1c2733e4ab6bebc68436177128eb
Key 3 ^ Key 4 = 996e59a867c171397fc8342b5f9a61d90bda51403ff6326303cb865a
Flag ^ Key 1 ^ Key 2 ^ Key 3 ^ Key 4 ^ Key 5 = 306d34c5b6dda0f53c7a0f5a2ce4596cfea5ecb676169dd7d5931139
```

## Observations

We have:

* K1
* K1 ^ K3
* K2 ^ K3 ^ K5
* K1 ^ K4 ^ K5
* K3 ^ K4

We want:

* K1 ^ K2 ^ K3 ^ K4 ^ K5
    
(since we can use this directly to calculate the flag).

### Note about XOR

Anything XORed with itself gets cancelled out. If we have `Flag ^ K1 ^ K2 ^ K3 ^ K4 ^ K5` and we XOR it with `K1 ^ K2 ^ K3 ^ K4 ^ K5`, we will end up with only `Flag` left.

> Also: "^" is shorthand for XOR.

## Solution

If we XOR together:
* K2 ^ K3 ^ K5
* K3 ^ K4
* K1 ^ K3

Then we will get `K1 ^ K2 ^ K3 ^ K4 ^ K5`. 
> Note: There are 3 `K3`s involved here. Two of them cancel and you are left with one.

## Code

See `script.py`.

```
$ python
Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> k235=bytes.fromhex("557ce6335808f3b812ce31c7230ddea9fb32bbaeaf8f0d4a540b4f05")
>>> k34 = bytes.fromhex("996e59a867c171397fc8342b5f9a61d90bda51403ff6326303cb865a")
>>> k13=bytes.fromhex("9a13ea39f27a12000e083a860f1bd26e4a126e68965cc48bee3fa11b")
>>> xoredFlag = bytes.fromhex("306d34c5b6dda0f53c7a0f5a2ce4596cfea5ecb676169dd7d5931139")
>>>
>>> def byte_xor(ba1, ba2):
...     return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
...
>>> key=byte_xor(byte_xor(k235, k34),k13)
>>> byte_xor(xoredFlag,key)
b'flag{n0t_t00_h4rD_h0p3fully}'
```

---
Andrew Steadman