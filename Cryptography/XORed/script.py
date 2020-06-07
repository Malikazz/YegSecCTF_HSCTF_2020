#!/usr/bin/env python

def byte_xor(ba1, ba2):
  return bytearray([_a ^ _b for _a, _b in zip(ba1, ba2)])

k_235=bytearray.fromhex("557ce6335808f3b812ce31c7230ddea9fb32bbaeaf8f0d4a540b4f05")
k_34=bytearray.fromhex("996e59a867c171397fc8342b5f9a61d90bda51403ff6326303cb865a")
k_13=bytearray.fromhex("9a13ea39f27a12000e083a860f1bd26e4a126e68965cc48bee3fa11b")
xored_flag = bytearray.fromhex("306d34c5b6dda0f53c7a0f5a2ce4596cfea5ecb676169dd7d5931139")

key=byte_xor(byte_xor(k_235, k_34),k_13)
print(byte_xor(xored_flag,key))
