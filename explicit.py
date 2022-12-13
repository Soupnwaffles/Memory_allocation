import memalloc 

class expfreeblock(): 
    def __init__(self, sizebytes =None, np=None,pp=None,hi=None,fi=None):
        self.sizebytes = sizebytes
        self.next = np
        self.prev = pp 
        self.headerindex = hi
        self.footerindex = fi
        pass

def explicit_heapinit():
     global explicit_heap 
     global free_linked 
     explicit_heap = [""]*1000 
     explicit_heap[999] = "0x00000001"
     explicit_heap[0] = "0x00000001"
     root = expfreeblock((998*4), "0x00000000", "0x00000000", 1, 998) 
     explicit_heap[root.headerindex]="0x{0:0{1}X}".format(root.sizebytes,8)
     explicit_heap[root.footerindex]="0x{0:0{1}X}".format(root.sizebytes,8)

def mealloc(sizebytes): 
    
