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