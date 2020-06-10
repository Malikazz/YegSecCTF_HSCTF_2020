# Generic Flag Checker

This one was one of the tougher challenges, but mostly spent my time wrapping my head around the assembly. In reality, the assembly code is pretty trivial and never gets too complicated, but I spent a lot of time just trying to understand what was going on.

One of the first things I did was run `strings` against memes.exe. From that output I determined it was likely that this program was packed using the UPX executable packer.

However, attempting to use upx to unpack it did not yield useful results.

A little bit of googling indicated that ASLR can interfere with unpacking UPX binaries. I also came across these instructions https://deceiveyour.team/2018/10/12/patching-a-binary-to-disable-aslr-using-python/ for patching an exe to disable ASLR. After executing the script to generate a new exe with manually disabled ASLR, I could then use upx to successfully unpack the patched binaries.

```
upx -d memes-patched.exe -o memes-unpacked.exe
```

I then opened up the unpacked exe in the free version of IDA. I'd never actually used IDA before (at least, not in 10+ years), so it was a learning experience for me.

Looking around for functions, we do see an interesting call to `strlen`.

```asm
.text:000000014000108E                 mov     rcx, rdi ; Str
.text:0000000140001091                 call    strlen
.text:0000000140001096                 mov     rbx, rax
.text:0000000140001099                 cmp     rax, 0Fh
.text:000000014000109D                 jbe     short loc_140001103
```

Some quick analysis looks like it's expecting a single command line argument, and as long as the argument is less than or equal to 15 chars long, it's moved into a dedicated buffer.

Then there's a bunch of stuff. One of the first things it does do is ignore the first 5 characters of argument string and move the rest into a different buffer. Then it iterates through that buffer and transforms it in *some* way.

Then we see see a second loop that starts by comparing the counter variable to 9:

```asm
.text:000000014000125A                 xor     edi, edi
.text:000000014000125C                 lea     rbx, unk_140003000
.text:0000000140001263                 lea     rsi, [rbp+40h+Buf2]
.text:0000000140001267                 cmp     edi, 9
.text:000000014000126A                 jb      short loc_140001281 ; jump into loop
.text:000000014000126C                 jmp     short loc_1400012C5 ; exit loop

.text:0000000140001270 loc_140001270: ; This bit runs at the "end" of every loop.
.text:0000000140001270                 mov     [rdx+rax], r9b
.text:0000000140001274                 mov     byte ptr [rdx+rax+1], 0
.text:0000000140001279                 add     edi, 1 ; increment counter
.text:000000014000127C                 cmp     edi, 9 ; compare to 9
.text:000000014000127F                 jnb     loc_1400012C5 ; exit loop

.text:0000000140001281 loc_140001281:
.text:0000000140001281                 mov     eax, edi
.text:0000000140001283                 movzx   r9d, byte ptr [rbx+rax*4] ; index into 0x140003000, offset 4 bytes ever iteration
.text:0000000140001288                 mov     rax, [rbp+40h+Size]
.text:000000014000128C                 mov     rcx, [rbp+40h+Size+8]
.text:0000000140001290                 cmp     rax, rcx
.text:0000000140001293                 jnb     short near ptr unk_1400012B0

.text:0000000140001295                 lea     rdx, [rax+1]
.text:0000000140001299                 mov     [rbp+40h+Size], rdx
.text:000000014000129D                 mov     rdx, rsi
.text:00000001400012A0                 cmp     rcx, 0Fh
.text:00000001400012A4                 jbe     short loc_140001270 ; loop start
.text:00000001400012A6                 mov     rdx, [rbp+40h+Buf2]
.text:00000001400012AA                 jmp     short loc_140001270 ; loop start

```

This loop is more interesting, because we see it reference some data at 0x140003000, but indexes that data in multiples of 4 bytes. If you remove the 3 nulls between each utilized byte, the referenced data is the string "con\i`g^k" - obscured in this way to presumably hide it from the "strings" command.

Once the loop exits, we see a call to `memcmp`. From what I can tell, the program is comparing the transformed output of the first loop with the magic string "con\i`g^k". Keeping in mind that the first loop ignores the first 5 characters of the argument.

Since "flag{" is 5 characters long, it seems likely at this point the argument is itself the flag. We need a string that when processed by the first loop results in the output "con\i`g^k".

Let's look a little closer at that loop.

Snipping away some of the cruft, the core of the loop is:

```asm
.text:0000000140001212 loc_140001212:
.text:0000000140001212                 movzx   r9d, byte ptr [rcx+rax] ; copy from buffer
.text:0000000140001217                 sub     r9b, dil ; SUBTRACT BY LOWER BYTE OF EDI (ie: the counter)
; ...
.text:00000001400011F0 loc_1400011F0:
.text:00000001400011F0                 mov     [rdx+rax], r9b ; store in new buffer
.text:00000001400011F4                 mov     byte ptr [rdx+rax+1], 0 ; append null
.text:00000001400011F9                 add     edi,1 ; increment counter
```

Basically, the loop takes the input byte, subtracts the index, and stores it in a new buffer. We now have all the information we need to re-construct the correct input string

```
InStr :  c????????
Index : -012345678
         ---------
OutStr:  con\i`g^k
```

<details><summary>Spoiler (Output Includes Flag)</summary>
<p>

```
flag{cpp_memes}
```

</p>
</details>

---
Andrew Steadman