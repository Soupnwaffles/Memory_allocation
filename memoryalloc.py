#Need global for explicit/implicit
#Need global heap 
#Need global fit

def heapstart(argv): 
    # Takes argv given by user.
    arg=argv.split()

    if (len(arg)<5): 
        printusage()
        return 

    outputfile=arg[1]

    strategystring= arg[2]

    fitstring = arg[3]

    inputfile = arg[4]

    #Validate the inputs
    try: 
        f = open(inputfile,"r")
    except: 
        print("Input file not opening. ")
        printusage()
        return 

    #Validate output file and open it for writing
    try: 
        o = open(outputfile, "w")
    except: 
        print("Output file opening not working. ")
        printusage()
        return 
    
    #Verify if fit is best or first fit
    if (fitstring.find("best") != -1): 
        fit = "best"
    elif (fitstring.find("first") != -1): 
        fit = "first" 
    else: 
        print("Could not find fit")
        printusage()
        return
    
    #Verify if strategy is implicit or explicit free list
    if (strategystring.find("implicit") != -1):
        strategy = "implicit"
    elif (strategystring.find("explicit") != -1): 
        strategy = "explicit"
    else: 
        print("Could not find if strategy was implicit or explicit.")
        printusage()
        return 

    #Create the heap
    heap = [0]*1000

    #Pointers to heap
    pointerarray = [0]*1000


    # end of heapstart
    return 1


def printusage(): 
    print("Usage: python3 heap.py [-o <output-path>] --free-list=\{implicit or explicit\} --fit=\{first or best\} <input file>   ")
    return 

def myalloc(heap, strategy, fit, bytes): 
    #4 bytes per word, add 8 by default for header and footer
    #Address must be divisible by 8
    # IF allocating 5 bytes, take 5 + (8-(5%8))
    # IF allocatin 13 bytes, take 13 + (8-(13%8)) = 16 , then +8 for head/foot
    paddedbytes= 8-(bytes%8)
    payloadbytes= bytes + paddedbytes
    totalbytes=  8 + payloadbytes
    address= "0x{0:0{1}X}".format(totalbytes,8)
    
    return 

def myfree(heap, address): 
    # must lookup reference block in pointerarray
    # If already free, don't do anything
    # Check if the block's neighbors are free and coalesce them 
    # Update the header and footer of the freed block (or coalesced)
    # Update the reference/pointer in the pointerarray
    return 

def myrealloc(heap, strategy, fit, address, bytes): 
    return 

def mysbrk(heap): 
    heap.append([0]*99000)