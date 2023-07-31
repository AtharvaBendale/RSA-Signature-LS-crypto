from sage.all import *

def custom_bit_and(a, b):
    c = bin(int(a, 2) & int(b, 2))
    return str(c[2:])

def custom_bit_not(a):
    c = ""
    for i in a:
        if i == "1":
            c = c + "0"
        else:
            c = c + "1"
    return c

def custom_bin_sum(a, b, c, d):
    total = bin(int(a, 2) + int(b, 2) + int(c, 2) + int(d, 2))
    return str(total[2:])

def custom_xor_string(a, b, c):
    y = int(a, 2) ^ int(b, 2) ^ int(c, 2)
    y = '{0:b}'.format(y)
    return y

def custom_right_rotate_string(s, k):
    if not s or k == 0:
        return s

    k %= len(s)
    rotated = s[-k:] + s[:-k]
    return rotated

def custom_right_shift_string(s, k):
    if not s or k == 0:
        return s

    k %= len(s)
    rotated = "0" * k + s[:-k]
    return rotated

def str_to_bits(string):
    binary_list = []
    for char in string:
        binary_list.append(bin(ord(char))[2:].zfill(8))
    return ''.join(binary_list)

H0 = "01101010000010011110011001100111"
H1 = "10111011011001111010111010000101"
H2 = "00111100011011101111001101110010"
H3 = "10100101010011111111010100111010"
H4 = "01010001000011100101001001111111"
H5 = "10011011000001010110100010001100"
H6 = "00011111100000111101100110101011"
H7 = "01011011111000001100110100011001"
a, b, c, d, e, f, g, h = H0, H1, H2, H3, H4, H5, H6, H7
k = ["0x428a2f98", "0x71374491", "0xb5c0fbcf", "0xe9b5dba5", "0x3956c25b", "0x59f111f1", "0x923f82a4", "0xab1c5ed5",
     "0xd807aa98", "0x12835b01", "0x243185be", "0x550c7dc3", "0x72be5d74", "0x80deb1fe", "0x9bdc06a7", "0xc19bf174",
     "0xe49b69c1", "0xefbe4786", "0x0fc19dc6", "0x240ca1cc", "0x2de92c6f", "0x4a7484aa", "0x5cb0a9dc", "0x76f988da",
     "0x983e5152", "0xa831c66d", "0xb00327c8", "0xbf597fc7", "0xc6e00bf3", "0xd5a79147", "0x06ca6351", "0x14292967",
     "0x27b70a85", "0x2e1b2138", "0x4d2c6dfc", "0x53380d13", "0x650a7354", "0x766a0abb", "0x81c2c92e", "0x92722c85",
     "0xa2bfe8a1", "0xa81a664b", "0xc24b8b70", "0xc76c51a3", "0xd192e819", "0xd6990624", "0xf40e3585", "0x106aa070",
     "0x19a4c116", "0x1e376c08", "0x2748774c", "0x34b0bcb5", "0x391c0cb3", "0x4ed8aa4a", "0x5b9cca4f", "0x682e6ff3",
     "0x748f82ee", "0x78a5636f", "0x84c87814", "0x8cc70208", "0x90befffa", "0xa4506ceb", "0xbef9a3f7", "0xc67178f2"]

file_name = input("Enter your filename (without .txt): ")
text_file = open("{0}.txt".format(file_name), "r")
signature = text_file.read()
signature_bits = str_to_bits(signature)
len_bits = len(signature_bits)

append_size = len_bits % 512
if append_size > 448:
    append_size = 960 - append_size
elif append_size <= 448:
    append_size = 448 - append_size

if append_size >= 1:
    signature_bits = signature_bits + "1"
    append_size -= 1
    for i in range(append_size):
        signature_bits = signature_bits + "0"

for i in range(64 - len((bin(len_bits))[2:])):
    signature_bits = signature_bits + "0"

signature_bits = signature_bits + str(bin(len_bits))[2:]

final_digest = ""
for i in range(len(signature_bits) // 512):

    M = []
    ccd = 0
    for i in range(16):
        M.append(signature_bits[ccd:ccd + 32])
        ccd += 32
    dump = "0" * 32
    for i in range(48):
        M.append(dump)

    for i in range(16, 64):
        v1 = custom_right_rotate_string(M[i - 15], 7)
        v2 = custom_right_rotate_string(M[i - 15], 18)
        v3 = custom_right_shift_string(M[i - 15], 3)
        s0 = custom_xor_string(v1, v2, v3)

        v4 = custom_right_rotate_string(M[i - 2], 17)
        v5 = custom_right_rotate_string(M[i - 2], 19)
        v6 = custom_right_shift_string(M[i - 2], 10)
        s1 = custom_xor_string(v4, v5, v6)
        M[i] = custom_bin_sum(M[i - 16], s0, M[i - 7], s1)[-32:]

    for i in range(64):
        s1 = custom_xor_string(custom_right_rotate_string(e, 6), custom_right_rotate_string(e, 11),
                               custom_right_rotate_string(e, 25))
        ch = int(custom_bit_and(e, f), 2) ^ int(custom_bit_and(custom_bit_not(e), g), 2)
        ch = '{0:b}'.format(ch)
        temp1 = custom_bin_sum(h, s1, ch, M[i])
        k_dump = str("{0:08b}".format(int(k[i], 16)))
        temp1 = str(bin(int(temp1, 2) + int(k_dump, 2))[2:])[-32:]
        s0 = custom_xor_string(custom_right_rotate_string(a, 2), custom_right_rotate_string(a, 13),
                               custom_right_rotate_string(a, 22))
        maj = custom_xor_string(custom_bit_and(a, b), custom_bit_and(a, c), custom_bit_and(b, c))
        temp2 = bin(int(s0, 2) + int(maj, 2))
        temp2 = str(temp2[2:])[-32:]
        h = g
        g = f
        f = e
        e = bin(int(d, 2) + int(temp1, 2))
        e = str(e[2:])[-32:]
        d = c
        c = b
        b = a
        a = bin(int(temp1, 2) + int(temp2, 2))
        a = str(a[2:])[-32:]

    H0 = bin(int(H0, 2) + int(a, 2))
    H0 = str(H0[2:])[-32:]
    H1 = bin(int(H1, 2) + int(b, 2))
    H1 = str(H1[2:])[-32:]
    H2 = bin(int(H2, 2) + int(c, 2))
    H2 = str(H2[2:])[-32:]
    H3 = bin(int(H3, 2) + int(d, 2))
    H3 = str(H3[2:])[-32:]
    H4 = bin(int(H4, 2) + int(e, 2))
    H4 = str(H4[2:])[-32:]
    H5 = bin(int(H5, 2) + int(f, 2))
    H5 = str(H5[2:])[-32:]
    H6 = bin(int(H6, 2) + int(g, 2))
    H6 = str(H6[2:])[-32:]
    H7 = bin(int(H7, 2) + int(h, 2))
    H7 = str(H7[2:])[-32:]

final_digest = H0 + H1 + H2 + H3 + H4 + H5 + H6 + H7
final_digest = int(final_digest, 2)

N = int(input("N: "))
e = int(input("e: "))
S = input("Signature: ")
S = int(S, 16)
S = pow(S, e, int(N))

if S == final_digest:
    print("Accept")
else:
    print("Reject")
