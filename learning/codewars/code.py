#Function Composition
add1  = lambda *a : sum(a)+1
this = lambda *a : sum(a)

#add1(1) 
#this(1)

def compose(f, g):    
    return lambda x: f(g(x))
    
compose(add1,this)(5)
compose(add1,this)(3,1)
##########################################################

#Diamonds

def diamond(n):
    if  n % 2 == 0:
        return None
    
    #n = -1
    S = ""
    levels = (n - 1)/2
    
    for l in range(levels,0,-1):
        stars = n-(l*2)    
        S += l*" " + "*" * stars +"\n"
    S +=  "*" * n + "\n"
    for l in range(1,levels+1,1):
        stars = n-(l*2)
        S +=  l*" " + "*" * stars + "\n"
    
    return S

print diamond(3)
print diamond(13)

##########################################################
##Primes

l = []
integer = 7 
for i in range (2,integer,1):
    if integer % i == 0:
        l.append(i)
if len(l) == 0:
    print str(integer) +' is prime'
else:
    print l
    

n= 7    
[i for i in xrange(2, n) if not n % i] or '%d is prime' % n
##########################################################
#Linked Lists - Push & BuildOneTwoThree
#Linked Lists - Length & Count
#Linked Lists - Get Nth Node

class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None
    
def push(head, data):
    n = Node(data)
    if head:
        n.next = head
    return n
  
def build_one_two_three():
    return push(push(push(None, 3), 2), 1)
	
   
def length(node):
  if node:
    return 1 + length(node.next)
  return 0
    
def count(node, data):
    if node == None:
        return 0  
    i = 0
    while True:
        if node.data == data:
            i+=1
        if node.next != None:
            node = node.next
        else:
            break
    return i        

	
def get_nth(node, index, i=0):
    if node is None:
        raise IndexError
    else:
        return node if index == i else get_nth(node.next, index, i + 1)
    