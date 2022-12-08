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
    if arg is None or len(arg)==1 or len(arg)==2: 
    #If input is none, default values used.  
        print("Commandline was none, defaulted to using 5.in as an input file, with implicit free list using first fit. ")
        arg = ["memoryalloc.py", "result", "--free-list=implicit", "--fit=first", "examples/5.in"]
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
    global f 
    global o
    global totalbytesheap
    global totalwords

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
    heap = ["0x00000000"]*1025
    heap[0] = "0x00000001"
    # If implicit, only worry about header and footer when initializing the heap. 
    if strategy == "implicit": 
        totalwords = len(heap) -1
        totalbytesinheap=(totalwords/2)
        heap[1] ="0x{0:0{1}X}".format(int(totalbytesinheap),8)
        heap[len(heap)-1] = "0x{0:0{1}X}".format(int(totalbytesinheap),8)
        print("last item in heap: ", heap[len(heap)-1])
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
    allocwords = int(totalbytes)/4
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
            newwords = decimalsize/4 
            # If space is allocated
            if decimalsize % 2 == 1: 
                # Move pointer forward 
                i += (newwords)
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
                    #Get the previous free block size and save it for later use. 
                    prevsize=heap[i]
                    # Make the previously free header into whatever the allocated size is, plus 1 for allocation. 
                    heap[i]="0x{0:0{1}X}".format(totalbytes+1,8)
                    #Make the new footer for the allocated block. 
                    heap[int(i+(totalbytes/4)-1)] = "0x{0:0{1}X}".format(totalbytes+1,8)  #Problem here? 
                    # If the new alloc takes up the entire previous free block, do nothing
                    if int(prevsize, 16) == (totalbytes/4): 
                        continue 
                    # If the previous free block was greater than the allocated space
                    else:
                        try: 
                            #Set a new size for the free block
                            newsizefree = int(prevsize,16)-totalbytes
                            # Go to where the new free block will be, change it to its new size. 
                            heap[int(i+(totalbytes/4))] = "0x{0:0{1}X}".format(newsizefree, 8)
                            # Also change the footer of the previous free block to the new size. 
                            try: 
                                heap[int(i + (int(prevsize,16)*2)-1)] = "0x{0:0{1}X}".format(newsizefree, 8)
                            except Exception as e: 
                                print("Something went wrong specifically when changing the footer of the prev free block.")
                                print(e) 
                        except Exception as e: 
                            print("Something went wrong when fixing new free block")
                            print(e) 
                    return i



            return 
    
    return 

def myfree(address): 
    # must lookup reference block in pointerarray
    # If already free, don't do anything
    # Check if the block's neighbors are free and coalesce them 
    # Update the header and footer of the freed block (or coalesced)
    # Update the reference/pointer in the pointerarray
    return 
    
def runlines(input,output): 
    # Run for each line in input text file
    for line in input: 
        print(line)
        theline=line.split(",")
        # If allocation, form: bytes, variable name
        if theline[0].strip()=="a": 
            #set pointerarray at index (variable name) to point to the resulting index of the alloc
            pointerarray[int(theline[2])] = myalloc(int(theline[1]))
        # If free, find the pointer, and execute the myfree function on it
        elif theline[0].strip()=="f": 
            myfree(int(theline[1]))
            continue 
        # If realloc, set new variable in the mypointer array and do the myrealloc using the previous variable and the new alloc space. 
        elif theline[0].strip()=="r": 
            pointerarray[int(theline[3])]= myrealloc(pointerarray[int(theline[2])], int(theline[1]))
            continue 

    return 

def myrealloc(prevpointer, bytes): 
    return 

def mysbrk(): 
    heap.append([0]*9000)

if __name__== "__main__": 
    heapstart(sys.argv)
    try: 
        print(heap[2])
        print(fit) 
        print(strategy)
        try: 
            runlines(f,o)
            for i in range(0,len(heap)): 
                if heap[i] != "0x00000000": 
                    print(i, heap[i])
            for every in pointerarray: 
                if every != 0: 
                    print(every) 
        except Exception as e: 
            print("could not run the lines of the input file, or something with output went wrong")
            print(e)
    except: 
        print("heap was not started correctly")