#Need global for explicit/implicit
#Need global heap 
#Need global fit
import sys

heap = []
strategy = ""
fit = "" 
pointerarray = []
def heapstart(argv=None): 
    # Takes argv given by user.
    #print(argv)
    arg = argv
    # Argv here can have something even if nothing is put in the command, only running
    # It will default to the path of the project as argv, with a length of 1 
    if arg is None or len(arg)==1: 
    #If input is none, default values used.  
        print("Commandline was none, defaulted to using 5.in as an input file, with implicit free list using first fit. ")
        arg = ["memoryalloc.py", "result/imfirst.txt", "--free-list=implicit", "--fit=first", "examples/5.in"]
    if (len(arg)<5): 
        printusage()
        print(arg) 
        print(len(arg))
        print("Try running again with the format above. ")
        return 

    #Strategy, fit, heap and pointer array must be global variables. 
    global strategy 
    global fit 
    global heap 
    global pointerarray

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
    #print(heap[2])

    #Pointers to heap
    pointerarray = [0]*1000


    # end of heapstart
    return 1


def printusage(): 
    print("Usage: python3 heap.py [-o <output-path>] --free-list={implicit or explicit} --fit={first or best} <input file>   ")
    return 

def myalloc(bytes): 
    #4 bytes per word, add 8 by default for header and footer
    #Address must be divisible by 8
    # IF allocating 5 bytes, take 5 + (8-(5%8))
    # IF allocatin 13 bytes, take 13 + (8-(13%8)) = 16 , then +8 for head/foot
    paddedbytes= 8-(bytes%8)
    payloadbytes= bytes + paddedbytes
    totalbytes=  8 + payloadbytes
    address= "0x{0:0{1}X}".format(totalbytes,8)
    #First address/word is a placeholder. 
    #Firstfit
    #Find the first available free space when allocating. 
    #Go through entire heap, if no space available, call mysbrk, try again
    #If space is found, found=True
    found = False 
    i = 1 
    if fit == "first" and strategy =="implicit":
        while (found == False):  
            decimalsize = int(heap[i], 16)
            # If space is allocated
            if decimalsize % 2 == 1: 
                # Move pointer forward 
                i += (decimalsize/4)
                # If there is not enough space when moving to next block
                if i >=(len(heap)-(totalbytes/4)): 
                    mysbrk()
            elif decimalsize % 2 == 0: 
                # If it is free, but not enough space for allocation
                if  decimalsize < totalbytes : 
                    #Move forward certain amount of words to next block
                    i += (decimalsize/4)
                    #Increase heap if heapsize reached limit. 
                    if i>=(len(heap)-(totalbytes/4)): 
                        mysbrk()
                #Otherwise, if there is enough space. 
                elif decimalsize >= totalbytes: 
                    found = True
                    #Add the bytes allocated + 1 (to indicate allocation) and return pointer. 
                    heap[i]="0x{0:0{1}X}".format(totalbytes+1,8)
                    heap[i+(totalbytes/4)-1] = "0x{0:0{1}X}".format(totalbytes+1,8)
                    return i



            return 
    
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

def mysbrk(): 
    heap.append([0]*9000)

if __name__== "__main__": 
    heapstart(sys.argv)
    print(heap[2])
    print(fit) 
    print(strategy)