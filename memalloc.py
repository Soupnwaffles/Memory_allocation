#Need global for explicit/implicit
#Need global heap 
#Need global fit
import sys
testing = True
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
        #print("Commandline was none, defaulted to using 5.in as an input file, with implicit free list using first fit. ")
        arg = ["memoryalloc.py", "resultheap.txt", "--free-list=implicit", "--fit=best", "examples/6.in"]
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
    global totalwords
    global bestfit
    #global largestfreespace
    #global totalbytesinheap
    totalwords = len(heap)
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
    heap = [""]*1000
    heap[0] = "0x00000001"
    heap[len(heap)-1]="0x00000001"
    # If implicit, only worry about header and footer when initializing the heap. 
    if strategy == "explicit": 
        heap[2]="0x00000000"
        heap[3]="0x00000000"
    #if strategy == "implicit": 
    totalwords = len(heap)
    initial_free_words= totalwords-2
    #initial_free_bytes=(totalwords/2)-1
    initial_free_bytes = initial_free_words * 4
    heap[1] ="0x{0:0{1}X}".format(int(initial_free_bytes),8)
    heap[len(heap)-2] = "0x{0:0{1}X}".format(int(initial_free_bytes),8)
    #print("last item in heap: ", heap[len(heap)-1])
    # Above should be good unless change in variables is wanted. 
    #Pointers to heap
    pointerarray = [None]*100


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
    if len(heap)-2 < bytes/4: 
        mysbrk()
   
    paddedbytes= 8-(bytes%8)
    payloadbytes= bytes + paddedbytes
    if paddedbytes != 8: 
        total_allocated_bytes=  8 + payloadbytes
    else: 
        total_allocated_bytes= payloadbytes
    # print("at beginning, total alloced bytes is: ", total_allocated_bytes)
    total_allocated_words = int(total_allocated_bytes/4)
    address= "0x{0:0{1}X}".format(total_allocated_bytes,8)
    #First address/word is a placeholder. 
    #Firstfit
    #Find the first available free space when allocating. 
    #Go through entire heap, if no space available, call mysbrk, try again
    #If space is found, found=True
    found = False 
    foundbest=False
    bestfit= ["","0x000000F98"] # bestfit[0] is heapindex , bestfit[1] is address/size
    i = 1 
    j = 1
    if fit == "best": 
        decimalbestfit = int(bestfit[1],16)
        while j<len(heap)-4: 
            decimal_old_blockbytes = int(heap[j], 16)
            # print("when we assign it, j is ",j," decimal_old_blockbytes is: ", decimal_old_blockbytes)
            # print("and heap is: ", heap[j])
            decimal_old_numwords = decimal_old_blockbytes/4
            decimalbestfit = int(bestfit[1],16) 
            if decimal_old_blockbytes % 2 == 1: 
                # Move pointer forward 
                # Subtract 1 if allocated, move ahead by that much 
                decimal_old_blockbytes-=1
                decimal_old_numwords = (decimal_old_blockbytes)/4
                j += decimal_old_numwords
                j = int(j)
                continue 
            if decimal_old_blockbytes % 2 == 0: 
                if decimal_old_blockbytes>=total_allocated_bytes and decimalbestfit > decimal_old_blockbytes: 
                    bestfit[0] = j 
                    bestfit[1] = heap[j]
                    foundbest=True
                    continue
                else: 
                    j += decimal_old_blockbytes/4
                    j = int(j)
                    continue
        if bestfit[0]!= "" and foundbest==False: 
            j = 1
        elif bestfit[0] != "" and foundbest == True: 
            j = int(bestfit[0]) 
        else: 
            j = 1 
        #Add the bytes allocated + 1 (to indicate allocation) and return pointer. 
        #Get the previous free block size and save it for later use. 
        prevsize=heap[j]
        decimal_old_blockbytes = int(heap[j], 16)
        # Make the previously free header into whatever the allocated size is, plus 1 for allocation. 
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("At line 231, we are making heap[j] = total_allocated bytes+1")
        heap[j]="0x{0:0{1}X}".format(total_allocated_bytes+1,8)
        #print("New heap value at j, ", j, "is: , ", heap[j])
        #Make the new footer for the allocated block. 
        heap[int(j+(total_allocated_bytes/4)-1)] = "0x{0:0{1}X}".format(total_allocated_bytes+1,8)  #Problem here? 
        #printnonemptyheap()
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # If the new alloc takes up the entire previous free block, do nothing
        if int(prevsize, 16) == (total_allocated_bytes/4): 
            pass
        # If the previous free block was greater than the allocated space
        else:
            try: 
                #Set a new size for the free block
                #newsizefree = int(prevsize,16)-total_allocated_bytes
                # print("Decimal_old_blockbytes is: ", decimal_old_blockbytes)
                # print("Total allocated bytes is: ", total_allocated_bytes)
                # print("total allocated words is: ", total_allocated_words)
                # print("j is: ", j)
                newsizefree = decimal_old_blockbytes - total_allocated_bytes
                #print("newsizefree is: ", newsizefree)
                #If the free block remaining will be greater than or equal to 16
                if newsizefree != 0 and newsizefree >= 16: 
                    # Go to where the new free block will be, change it to its new size. 
                    #heap[int(i+(total_allocated_bytes/4))] = "0x{0:0{1}X}".format(newsizefree, 8)
                    heap[int(j+(total_allocated_words))] = "0x{0:0{1}X}".format(newsizefree, 8)
                    # Also change the footer of the previous free block to the new size. 
                    try: 
                        newfreewords = int(newsizefree/4)
                        heap[int(j + (total_allocated_words)+(newfreewords-1))] = "0x{0:0{1}X}".format(newsizefree, 8) 
                    except Exception as e: 
                        print("Something went wrong specifically when changing the footer of the prev free block for best fit.")
                        print(e) 
                else: # If remaining free space is less than 16, fill whole chunk.
                    heap[j] = "0x{0:0{1}X}".format(decimal_old_blockbytes+1,8)
                    heap[int(j+(decimal_old_blockbytes/4)-1)] = "0x{0:0{1}X}".format(decimal_old_blockbytes+1,8) 
                    #clear data in that chunk. 
                    for num in range(j+1,int(j+(decimal_old_blockbytes/4)-1)): 
                        heap[num] = ""
            except Exception as e: 
                print("Something went wrong when fixing new free block in best fit")
                print(e) 
        return j
            
    #########################################################
    # For implicit, firstfit. 
    if fit == "first" and strategy =="implicit":
        while (found == False):  
            # Decimal value of the bytes of the previous free block. 
            decimal_old_blockbytes = int(heap[i], 16)
            decimal_old_numwords = decimal_old_blockbytes/4 
            # If space is allocated
            if decimal_old_blockbytes % 2 == 1: 
                # Move pointer forward 
                # Subtract 1 if allocated, move ahead by that much 
                decimal_old_blockbytes-=1
                decimal_old_numwords = (decimal_old_blockbytes)/4
                i += decimal_old_numwords
                i = int(i)
                # If there is not enough space when moving to next block
                if i >=(len(heap)-(total_allocated_bytes/4)): 
                    mysbrk()
                continue
            elif decimal_old_blockbytes % 2 == 0: 
                # If it is free, but not enough space for allocation
                if  decimal_old_blockbytes < total_allocated_bytes : 
                    #Move forward certain amount of words to next block
                    i += (decimal_old_blockbytes/4)
                    #Increase heap if heapsize reached limit. 
                    if i>=(len(heap)-(total_allocated_bytes/4)): 
                        mysbrk()
                #Otherwise, if there is enough space. 
                elif decimal_old_blockbytes >= total_allocated_bytes: 
                    found = True
                    #Add the bytes allocated + 1 (to indicate allocation) and return pointer. 
                    #Get the previous free block size and save it for later use. 
                    prevsize=heap[i]
                    # Make the previously free header into whatever the allocated size is, plus 1 for allocation. 
                    
                    heap[i]="0x{0:0{1}X}".format(total_allocated_bytes+1,8)

                    #Make the new footer for the allocated block. 
                    heap[int(i+(total_allocated_bytes/4)-1)] = "0x{0:0{1}X}".format(total_allocated_bytes+1,8)  #Problem here? 
                   
                    # If the new alloc takes up the entire previous free block, do nothing
                    if int(prevsize, 16) == (total_allocated_bytes/4): 
                        continue 
                    # If the previous free block was greater than the allocated space
                    else:
                        try: 
                            #Set a new size for the free block
                            #newsizefree = int(prevsize,16)-total_allocated_bytes
                            newsizefree = decimal_old_blockbytes - total_allocated_bytes
                            
                           
                            if newsizefree != 0 and newsizefree >= 16: 
                                # Go to where the new free block will be, change it to its new size. 
                                #heap[int(i+(total_allocated_bytes/4))] = "0x{0:0{1}X}".format(newsizefree, 8)
                                heap[int(i+(total_allocated_words))] = "0x{0:0{1}X}".format(newsizefree, 8)
                                # Also change the footer of the previous free block to the new size. 
                                try: 
                                    heap[int(i + (decimal_old_numwords)-1)] = "0x{0:0{1}X}".format(newsizefree, 8) 
                                except Exception as e: 
                                    print("Something went wrong specifically when changing the footer of the prev free block.")
                                    print(e) 
                            else: # If remaining free space is less than 16, fill whole chunk.
                                heap[i] = "0x{0:0{1}X}".format(decimal_old_blockbytes+1,8)
                                heap[int(i+(decimal_old_blockbytes/4)-1)] = "0x{0:0{1}X}".format(decimal_old_blockbytes+1,8) 
                                #clear data in that chunk. 
                                for num in range(i+1,int(i+(decimal_old_blockbytes/4)-1)): 
                                    heap[num] = ""
                           
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
    if pointerarray[address]==None: 
        return 
    # First take the index of the requested free. 
    requested_free_header_index= int(pointerarray[int(address)])
    # Take the header of the block you are trying to free. Will be decimal value. Subtract 1 to get rid of allocation. 
    requested_freeblock_bytesize= int(heap[requested_free_header_index], 16) -1
    requested_freeblock_wordsize= int(requested_freeblock_bytesize/4) 
    # Take the index of the footer of the block you are currently trying to free. 
    requested_free_footer_index=int(requested_free_header_index+requested_freeblock_wordsize-1) 

    # Check the predecessor block in heap
    predecessor_footer_index = int(requested_free_header_index)-1 
    predecessor_bytesize = int(heap[predecessor_footer_index], 16)
    predecessor_header_index = 0 
    if int(heap[predecessor_footer_index],16) % 2 == 1 and predecessor_footer_index != 0: 
        predecessor_header_index = predecessor_footer_index - (((predecessor_bytesize-1)/4) -1 )
    elif predecessor_footer_index != 0: 
        predecessor_header_index = predecessor_footer_index - (predecessor_bytesize/4) -1
    
    #Check if it is the first or
    #Check if predecessor is freed or not already. 
    if predecessor_bytesize % 2 == 1 or predecessor_footer_index==0: 
        coalesce_previous=False 
    else: 
        coalesce_previous=True 
        predecessor_header_index = predecessor_footer_index+1-(int(predecessor_bytesize/4)) 
        sumfreebytes=int(requested_freeblock_bytesize+predecessor_bytesize)
    
    successor_header_index = int(requested_free_footer_index) + 1 
    successor_bytesize = int(heap[successor_header_index], 16)
    #Check successor if free or not. 
    if successor_bytesize % 2 ==1 or (successor_header_index == (len(heap)-1)): 
        coalesce_next = False
    else: 
        coalesce_next = True
        successor_footer_index = successor_header_index-1+ (int(successor_bytesize/4))
        sumfreenextbytes=int(requested_freeblock_bytesize+successor_bytesize)
    #Use this "pointer" to look for the word in the heap
    #Case 1: predecessor block and successor block are allocated
    # Or if previous word is start of heap. 
    #Simply change header and footer. 
    #Free, then coalesce lower, then higher 
    #if coalesce_previous==False and coalesce_next==False: 
    #print("requested free block byte size is: ", requested_freeblock_bytesize)
    #heap[requested_free_header_index]="0x{0:0{1}X}".format(requested_freeblock_bytesize, 8)
    #heap[requested_free_footer_index]="0x{0:0{1}X}".format(requested_freeblock_bytesize, 8)
        #if strategy=="explicit": 
        #   heap[requested_free_header_index+1] = 
    #Coalesce previous, change header, then change footer. 
    if coalesce_previous==False and coalesce_next==False: 
        heap[requested_free_header_index]="0x{0:0{1}X}".format(requested_freeblock_bytesize, 8)
        heap[requested_free_footer_index]="0x{0:0{1}X}".format(requested_freeblock_bytesize, 8)
        return 
    elif coalesce_next==False and coalesce_previous==True: 
        heap[predecessor_header_index] ="0x{0:0{1}X}".format(sumfreebytes, 8)
        heap[requested_free_footer_index]="0x{0:0{1}X}".format(sumfreebytes, 8)
        return 
    elif coalesce_next==True and coalesce_previous==False: 
        heap[requested_free_header_index] ="0x{0:0{1}X}".format(sumfreenextbytes, 8)
        heap[successor_footer_index]="0x{0:0{1}X}".format(sumfreenextbytes, 8)
        return 
    elif coalesce_next==True and coalesce_previous==True: 
        heap[predecessor_header_index] = "0x{0:0{1}X}".format(requested_freeblock_bytesize + predecessor_bytesize + successor_bytesize, 8) 
        heap[successor_footer_index] = "0x{0:0{1}X}".format(requested_freeblock_bytesize + predecessor_bytesize + successor_bytesize, 8) 
        return 

    pointerarray[address]=None
    
    
    return 
    
def runlines(input,output): 
    # Run for each line in input text file
    for line in input: 
        try: 
            # print("----------------------")
            # print(line)
            theline=line.split(",")
            # If allocation, form: bytes, variable name
            if theline[0].strip()=="a": 
                #set pointerarray at index (variable name) to point to the resulting index of the alloc
                if(int(theline[1]) > 25000): 
                    print("python3 memalloc.py: Total heap capacity reached! (100000 words)")
                    return 0 
               
                pointerarray[int(theline[2])] = myalloc(int(theline[1]))
                
            # If free, find the pointer, and execute the myfree function on it
            elif theline[0].strip()=="f": 
                # print("---------------")
                # print("We want to free, variable: ", theline[1])
                myfree(int(theline[1]))
                pointerarray[int(theline[1])]= None
                # printnonemptyheap()
                # print("end of free")
                # print("----------------")
                continue 
            # If realloc, set new variable in the mypointer array and do the myrealloc using the previous variable and the new alloc space. 
            elif theline[0].strip()=="r": 
                pointerarray[int(theline[3])]= myrealloc(pointerarray[int(theline[2])], int(theline[1]))
                # print("After realloc, heap is: ")
                # printnonemptyheap()
                continue 
        except Exception as e: 
            print("Something went wrong in runlines. ")
            print(e) 
            return 

    return 

def myrealloc(prevpointer, bytes): 
    global realloc 
    realloc = True
    if int(bytes)==0: 
        myfree(prevpointer)
        return None
    try: 
        #copyfooter=heap[pointerarray[prevpointer]]
        z = myalloc(bytes)
        
        # print("Here we go into realloc function, copying data into heap")
        previndex = int(pointerarray[prevpointer]) 
        dec_old_heapbytes = int(heap[previndex],16) -1
        dec_old_numwords = int(dec_old_heapbytes/4) 
        # print("prev index is: ", previndex, ", And dec_old_words is, ",dec_old_numwords)
        temparray=[""]*(dec_old_numwords-2)
        for w in range(0,dec_old_numwords-2): 
            temparray[w] = heap[(previndex)+1+w]
        for w in range(0,len(temparray)): 
             # print("z + 1 + w is: ",z+1+w)
            heap[(z)+1+w] = temparray[w]

        myfree(prevpointer)
        pointerarray[prevpointer]= None
        realloc  = False
        return z
    except Exception as e: 
        print("Something went wrong in realloc: ")
        print(e) 
        return 
    return z

def mysbrk(): 
    try:
        prevlen = len(heap)
        for i in range(0,302): 
            heap.append("")
        heap[len(heap)-1] = "0x00000001"
        heap[prevlen-1] = "" 
        pointerarray[100] = prevlen-1
        remainingwords=len(heap)-1000
        heap[999]= "0x{0:0{1}X}".format(int((remainingwords+1)*4), 8)
        heap[9998] = "0x{0:0{1}X}".format(int((remainingwords+1)*4), 8)
        myfree(100)
        # print("After calling sbrk, ")
        # printnonemptyheap()
        # print("returning from sbrk---------------")
        return 
    except Exception as e: 
        print("Something went wrong in mysbrk")
        print(e) 
        return 
def printevenemptyheap(o): 
    for i in range(0,len(heap)): 
        text = "{0}, {1} \n".format(i,heap[i])
        o.write(text)
    return
def printnonemptyheap(): 
    if testing==True: 
        for i in range(0,len(heap)): 
            if heap[i] != None and heap[i] != "": 
                print(i,",",heap[i])
        return 

if __name__== "__main__": 
    heapstart(sys.argv)
    try: 
        #print(heap[2])
        #print(fit) 
        #print(strategy)
        try: 
            runlines(f,o)
            printevenemptyheap(o)
            f.close()
            o.close()

        except Exception as e: 
            print("could not run the lines of the input file, or something with output went wrong")
            print(e)
    except: 
        print("heap was not started correctly")