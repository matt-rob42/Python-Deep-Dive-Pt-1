# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:55:22 2020

@author: matt_
"""

####Python Deep Dive###################

###???? What variables actually are

###Video - Variables are memory references

###Think of memory as a series of slots or boxes - we can store and
### Retrive - think letters and mailboxes

###0x1000 etc. are memory addresses

###Data may use more than one slot - finite space per slot

###The collection of stored objects is the "heap" - store and retrieve are
### handled by python mem manager

my_var_1 = 10
#when we enter this, python creates an object in memory, and stores 10
#my_var_1 is just an alias for the mem addresss
#therefore mv1 is the reference to the object! (Pointer)

myvar2 = 'hello' # same storage process, mv2 is again an alias

#we can find a memory address by using the id() function!!!

#id() returns a base 10 number, convert to hex with hex()

myvar = 10 

#print(myvar)
#print(id(myvar))
#print(hex(id(myvar)))
#
#greeting = 'hello'
#
#print(greeting)
#print(hex(id(greeting)))

###### Video - Reference Counting #######

###We can track objects in memory, and what is pointing at them, 
### this is useful as more things ref each other!

othervar = myvar

# here, the *reference* of myvar is assigned to othervar! Only one
# object in memory two things now referencing the address

# this ref counting is handled by python mem manager

# How to find a ref count:

import sys
#print(sys.getrefcount(myvar)) # ! Passing in myvar makes yet another ref!

#cleaner way to do this - uses c libraries

#ctypes.c_long.from_address(address).value # this passes memory address, so no
#change to ref counts!

a = [1, 2, 3,]
#print(id(a))
#print(sys.getrefcount(a))  # always subtract one!

#import ctypes

def ref_count(address: int):
    return ctypes.c_long.from_address(address).value

#print(ref_count(id(a)))  #!!!!!!

b = a

#print(id(b))
#
#print(ref_count(id(b)))

########################## VIDEO - GARBAGE COLLECTION #####

# Whenever ref count = 0, PMM destroys the object in memory!
# Sometimes this doesn't work, esp. in the case of circ. references
# Imagine myvar points to object A, which in turn points to object B
# If we delete myvar, A's count goes to 0 (removed) and B's count goes
# to zero (also removed) so far all good - but what if B contains an instance
# var, var2 that point to object A - so when we delete myvar - 
# the ref count of A is still 1 !

# THIS is what causes a memory leak !!!

# So we need the garbage collector, which can see circ refs
# we can control the GC with gc module

# we can turn GC off, but it's a terrible idea, except...good 
# for performance 

# GC doesn't always work! The main issues are in Python 3.4 or less

import ctypes
import gc

#def object_by_id(object_id):
#    for obj in gc.get_objects():
#        if id(obj) == object_id:
#            return "Exists"
#        return "Not found"
#
## Now here are two classes that we'll use to make the circ ref
#        
#class A:
#    def __init__(self):
#        self.b = B(self)
#        print("A:self: {0}, b: {1}".format(hex(id(self)), hex(id(self.b))))
#        # The print gives us the mem address of both self and the 
#        # B reference
#class B:
#    def __init__(self, a):
#        self.a = a
#        print("B:self: {0}, a: {1}".format(hex(id(self)), hex(id(self.a))))
#    
#gc.disable()
## Creates an instance of A()
#my_var = A()
#
## my_var is pointing at a
#
##print(hex(id(my_var)))
##print(hex(id(my_var.b))) # These classes have other classes as props!
##print(hex(id(my_var.b.a)))
#
## now, we'll store the IDs
#
#a_id = id(my_var)
#
#b_id = id(my_var.b)

#print(ref_count(a_id)) # 2 
#
#print(ref_count(b_id)) # 1
#
#print(object_by_id(a_id))
#
#print(object_by_id(b_id))
#
#my_var = None # breaks reference
#
#
#print(ref_count(a_id)) # 1
#
#print(ref_count(b_id)) # 1
#
## Circ, so ref count won't help us!
#
## run GC manually
#
#gc.collect()
#
#print(ref_count(a_id)) # !!!
#
#print(ref_count(b_id))# !!!

### Dynamic Typing vs Static Typing #####

# e.g. Java - String myvar = 'hello' -> this is static typing

# this means we can't do this: myvar = 10

#python, of course is dynamically typed

# we can use type() to determine the current referenced type

# examples

#a = "hello"
#print(type(a))
#a = 10
#print(type(a)) # etc. etc.

### Variable Re-asignment ####
# Key Point - a mem object with value 10 is created, my_var is just
# a reference!
my_var = 10
# if we now do this, a NEW object at a different mem obj is created!
# my_var points at the new one
my_var = 15

# This is actually quite key

############ VIDEO - MUTABILITY ###########

        
#### VIDEO - Object mutability ####
        
# consider an object in memory - it has data, and a mem location
        # changing the data inside in object is called changing the 
        # internal state
        
#e.g. my_account refs an account object at a given mem address
        # bank account has acc num and balance properties
        #if we change balance, the data changes, but mem loc does not
        # this is unlike integers, where a new value is a new addres
        # THIS is mutability
        
# So the object was *mutated* internal state change
        # examples in python - all numbers are immutable
        # strings too, and tuples, frozen sets too (?) we can also
        # define a class to be immutable 
        ## Lists *are* mutable, so are dicts, sets, user defined classes
## Warning about mutability
        #e.g. t = (1,2,3) # immutable, and so are its components!
        #consider a =[ 1, 2]
        # b = [3, 4]
        #t = (a,b).....what happens???
#       we can change a and b, but can't change t directly
        #so we can change the state of t's object references
        
#my_list = [1,2,3]
#print(type(my_list))
#id(my_list) gives address, if we append something, address doesn't change!

### VIDEO - FN Arguments and Mutability ###

# Ex strings are immutable objects 
# e.g. my_var = 'hello' 
# Immutable objects are generally safe from side effects Example:
#def process(s):
#    s = s + 'world' 
#    return s
#
#my_var = 'hello'

# when we run this, hello is at the 'module scope' level - so 
# when we feed it into the method, my_var's *REFERENCE* is passed
# to process
# process turns s into a reference to the same mem address object as
# my_var was pointing at, but we won't modify hello in place
# so there is a new object in memory called hello world, which s starts pointing at!
# so my_var is not affected
        
#### Now what happens in a mutable var?
#def process(lst):
#    lst.append(100)
#
#my_list = [1,2,3]
# so at outset, lst and my_lst point at the same object, when we 
# append the number though, it changes BOTH my_var and lst
# This is a side effect

#Now what about our previous tuple example?

#def process(t):
#    t[0].append(3)
#my_tuple = ([1,2], 'a')
#process(my_tuple)
#print(my_tuple[0])
# Watch for this!

#def process2(s):
#    print("Initial mem address of s = {0}".format(id(s)))
#    s = s + 'world'
#    print("Final mem address of s = {0}".format(id(s)))
#    
## The above fn should return two different mem addresses - immut!
#my_var = 'hello' 
#print(id(my_var))
#process2(my_var)
## NOTE THE DIFFERENCE!!! ^^^^
#
#def modify_list(lst):
#    print("Initial mem address of lst = {0}".format(id(lst)))
#    lst.append(100)
#    print("Final mem address of lst = {0}".format(id(lst)))
#
#my_list = [1,2,3]
#print(id(my_list))
#modify_list(my_list)
### !!!! THE ADDRESSES ARE THE SAME^^^^^
################ SHARED REFS AND IMMUTABILITY #########
        
## Two vars ref'ing same meme address - 
        # a = 10, b = a, so b is referring to a's thing
#def my_func(v):
#    pass
#
#t = 20
#my_func(t) # this passes the ref to t!
#
##Now if 
#a = 10
#b = 10
## they actually ref the same mem object!!! Python automatically did this
#s ='hi'
#s = 'hi' # same thing happens - good idea? Yes - immutable!
## BUT what if the objects are mutable???
#
#a = [1,2,3]
#b = a
#b.append(100)
## This changes a and b !!!
## mem man won't make a shared ref
#a = 'hello'
#b = a
#print(hex(id(a)))
#print(hex(id(b))) # same!

#c = [1,2,3]
#d = c
#d.append(100)
#print(hex(id(c)))
#print(hex(id(d))) #address are same - this is the risk
        
####### VIDEO - VARIABLE EQUALITY #########
## How to compare? 
        #1) Compare mem address
        # 2) Internal state - eg contents of lists
# to compare mem addresses - we use "is" fn
        # eg v1 is v2
# to compare internal state we use ==
# v1 == v2 - are contents equal
# is not is the converse of is 
# != is the not equals for object values

## None object - assigned to vars to show they are not set
## (Null pointer) - but this IS a real object - and mem man
## will always create a shared ref for it
 # this means we can use a is None to eval correctly
 # None is NOT nothing

### VIDEO - EVERYTHING IS AN OBJECT ######

# Everything is an instance of a class - e.g. class is instance of 
 # a class object
 # Therefore they all have mem addresses! Incuding functions!
#def my_func(): # this is stored in a mem address!
#    pass       
#! Any object can be assigned to a var!
    # any object can be passed to a function
    #  any object can be returned from a function!
    
  ### VIDEO - OPTIMIZATION - INTERNING ####

#   if we do this:
a = 10
b = 10

## Python will create a shared reference!

## BUT if we do this:

a = 500
b = 500

## it won't ----why?
## It would be safe, but this is interning
## Reusing objects on demand
## At startup, python caches ints from -5 to 256
## any int in that range uses cached version - shared refs
## 500 is outside of the range
## Why? small ints are common - optimize
## when we write a = 10, just point at existing ref for 10!
## but a = 257, we make a new object!
#a = 10
#b = 10 # ids are same
#a = -5
#b= -5 # also have same addresses
#print(a is b)
#a = 257
#b = 257
#print(a is b) ###False!


### VIDEO STRING INTERNING ###

## some but not all strings are interned
## As python code is compiled, identifiers are interned
## Identifiers are var names, fn names, class names etc.
## SOME string literals may be auto interned - which ones?
## the ones that satisfy the rules for an identifier - i.e.
## must start with _ or letter, only contain _, nums or letters
## don't absolutely count on this
## done for speed and mem optimization
## for example, imagine:
#a = "long_string"
#b = "long_string"
### if we do 
#a == b # it compares char by char - slower
### if interned, we know a, b have same mem add, so can use a is b
### Not all strings interned we can force it though!
#import sys
#a = sys.intern("a_string")
#b = sys.intern("a_string")
## This will be fast, but only worth it with
## very large sets of text
#a = "hello"
#b = "hello" # These looks like idents, so interned
#print(id(a), id(b))
###BUT
#a = "hello world"
#b = "hello world" # will be different!
#a==b # True
#a is b # False
### Forced interning:
#import sys
#a = sys.intern("hello world")
#b = sys.intern("hello world") # will be equal


###VIDEO - PEEPHOLE OPTIMIZATIONS ####

## Occur at compile time
## Some things get optimized - like:
## constant expressions e.g. numeric calcs 24*60
## Python we precalc this!
## Safe b/c constant expression
## short sequences, less than 20 (1,1,1,1,1,1,1)

## Python also optimizes membership tests:
## e.g. if e in [1,2,3] the list is basically const
## here, so python treats as such

## !!python will treat as its immutable counterpart
## i.e. list -> tuple, set -> frozen set
## Set membership way faster than list or tup membership
## GOOD TIP - IF line repeated many times,
## use if e in {1,2,3} instead of list/tup version
## this is faster
###Some sample code
#def my_func():
#    a = 24* 60
#    b = (1,2) * 5
#    c = "abc" * 3
#    d = 'ab' * 11
#    e = "a long stringnnnnnnnnnn" * 5
#    f = ['a', 'b'] * 3
#print(my_func.__code__.co_consts) ## This is cool!
#
#def a_func():
#    if e in {1,2,3}:
#        pass
#    
#print(a_func.__code__.co_consts) ## This is a Frz set

#### SECTION ON NUMBERS #####
## 4 types int, rational numbers reped as fractions objects
## Real nums, reped as floats OR decimal
## and complex, a + bi, use complex type
## ALSO Booleans are considered numbers!!!
### T/F are just 0 and 1

### VIDEO - INT TYPE ####
## How big can an int get?
## Rep'ed as base 2
##  !!! if we want neg ints, we have to reserve a bit
## to determine the sign
## for n bits, we can encode a number 2^n - 1 large
## if we use negs, think of it more as a window -
## e.g. 8 bit, reping negs, gives us [-2^7, 2^7 - 1]
## the reason for this is that we don't really need to 
## represent 0!
### SO size of int bepends on number of bytes we
## allocate

## Some languages have specific types for dif
## number sizes (Java) python is variable / dynamic

### VIDEO - INTEGER OPERATIONS ###
## We have all the standard arithmatic stuff 
## but what is the resulting type of these ops?
## e.g. int - int = int, int * int = int etc.
## BUT division always returns a float
## x // y returns the main part (floor div)
## x % y returns remainder (modulo)
## num = denom * (num // denom) + (n % d)
## what is the "floor" of a real number?
## largest integer less than or equal to a
## eg floor(3.24) = 3
## what about negatives? 
## just think, floor(-3.1) = -4
## a // b = floor(a/b)
##  NEGATIVE MODULO - VERY INTERESTING
#print(type(1+1))
#print(type(1+1*10))
#
#print(type(2/3)) # float

#import math # to get floor
#print(math.floor(3.15))
#print(math.floor(3.999))
#
#print(math.floor(-3.00000001)) # -4 b/c it's LESS!
#a = 33
#b = 16
#print(a/b)
#print(a//b)
#print(math.floor(a/b))
#
#a = -33
#b = 16
#print(a/b)
#print(a//b)
#print(math.floor(a/b))
### INTEGERS - CONSTRUCTORS AND BASES ###

## int number is an object, of int class
## 2 constructors first, just a number, like 1,
## second, a string plus an optional param
#a = int(10) # same as
#a = 10
### and 
#a = int(-10)
#a = int(10.9) # truncates
#a = int(True) # is just 1 !!!
### we can pass decimals, fractions etc.
### Second way:
#a = int("10") # this works
### we can also spec base of number in the string!
#int("123") # this assumes base 10
### but we can do this:
#int('123', base=16) # base between 2 and 36
#### SIDE NOTE - HEX IS BASE 16, 0-9, then a-f for 10, 11 etc.
#### e.g. int("1010", base=2) = 10
#int("A12F", base = 16) #is 41263 in base 10!
#int("A", base=11) # 10
#int("B", base = 11) # value error!
#####changing from base 10 to another base
#bin() # turns int to base 2
#oct() # for base 8
#hex() # base 6 ??
### SIDE NOTE Other bases e.g. base 8 - 
### oct(10) = 0o12 the 0o IDs as octal, then one 8^1 plus 2 8^0
### How would we do bases other than 10, 8, 6?

## We'll need some custom code: 
#m = 5
#n = 232
#b = 5        
#digits  = []
#while n > 0:    # very nice alg
#    m = n % b
#    n = n // b
#    print(m,n)
#    digits.insert(0,m) # note use of insert to put at front!
#print(digits)
 ### So the above gives us the digits in spec'd base
 ### but we want an encoding for numbers higher than 9!
### char -> digits is called encoding map
## simple encoding goes like this (I got it!)
 ## digits = [....]
 ## map = '....' this is a 123....ABC string
#encoding = ''
#for d in digits:
#    encoding += map[d]
## this isn't great, b/c remember that strs are immut, so we're creating many new objects!
## Better way: the join method (more to come)


