def main(): 
    i = 16
    h = hex(i)
    c = int(h,16) + int(hex(16),16) + 1
    h = hex(c + 1)[2:]

    # { Format identifier
    # 0: First parameter
    # # use 0x prefix 
    # 0 fill with 0's 
    # {1} to a length of n characters (including 0x), defined by 2nd parameter
    # X hexadecimal number, using uppercase letters for a-f
    # } End of format identifier

    myhex="{0:#0{1}X}".format(c,10)
    w = 127
    myother = "{0:#0{1}X}".format(w,10)
    totalbytes=127
    #address is 0x format w/ lowercase x and Uppercase hexadecimal a-f
    address= '0x{0:0{1}X}'.format(totalbytes,8)
    print(myhex)
    print(myother)
    print(address)
    # Need to figure out how to fill the 0's after the "0x" for hex
    print(c)
    print(h)
    return
main()