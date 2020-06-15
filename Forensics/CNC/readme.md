# CNC

## E01 Files

So E01 files as far as I can tell are better know as EWF (Expert Witness Files)
They are produced by several types of software, the one I am working with as 
stated in the challenge and from looking over it is a USB img. I installed [Autopsy](https://www.sleuthkit.org/autopsy/)
and opened the img. Inside we find some PNG's, and some files in different formates
for CNC machines. I ran different stego tools on the images till zsteg got 
1/3 of the flag. 

I then took a look at the zip files which required a password. I found it 
in the password.xmls. Which had a cheeky fake flag part in it as well :P.

Once you open the zip you will be greated with different file types, a little 
seraching will let you know they are CNC machine models. I found software to open
them and after going through them all found that one model spelt out part of the flag.

The next thing I looked over was the mp4 in the img, I normally try opening something
first which just gets you rickrolled. My next step is almost always to just throw
a few tools at it one being strings, and the flag was in the strings. That was
all the parts for this one :). 

Wish I had taken pictures of this one but did not and I cant seem to download the files anymore. 