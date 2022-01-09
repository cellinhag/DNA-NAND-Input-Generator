#!/usr/bin/env python
# Author: Marcella Grillo
# Date:   29/08/2018
# Filename: init.py
# Last modified by:   marcella
# Last modified time: 09/01/2022
# License: BSD



import math
import random


# Find matches
class findMatches(object):
    def __init__(self):

        # default is False, set to True to turn on debug
        self.debug = False

        # Binding rules:
        # 0 <---> 1
        # A <---> T
        #     or
        # 2 <---> 3
        # C <---> G

        self.nucleotides = [0,1,2,3]
        ask_sequence= input("Please enter your sequence: ")
        sequence = self.translator(ask_sequence)
        self.bumbling(sequence)

    # detect sequence length
    def getLength(self, seq):
        r = len(seq)
        if r < 6:
            print("Too short! Minimum sequence length is 6")
            return None
        else:
            pass
        
        if self.debug:
            print("Debug: sequence length is " + str(r))
            return r
        else:
            return r

    # calculate required CG match (33%)
    def getCGCount(self, sequence):
        c = self.getLength(sequence)
        if c < 9:
            c = 2
        elif c == 9:
            c = 3
        else:
            c = c * 0.33
        c = int(c)
        if self.debug:
            print("Debug: required CG matches is " + str(c))
            return c
        else:
            return c

    # calculate required mismatch (25%)
    def getLeft(self, sequence):
        c = self.getLength(sequence)
        if c <= 9:
            c = 2
        else:
            c = c * 0.25
        c = math.ceil(c)
        if self.debug:
            print("Debug: required CG matches is " + str(c))
            return c
        else:
            return c

    # generate matches
    def bumbling(self, sequence):
        sLen = self.getLength(sequence)
        lp = sLen - 1
        maxCG = self.getCGCount(sequence)
        maxLeft = self.getLeft(sequence)
        n = self.nucleotides
        if self.debug:
            print("sLen: " + str(sLen))
            print("maxCG: " + str(maxCG))
            print("maxLeft: " + str(maxLeft))

        #counters
        counter = 0      # general counts
        mismatch = 0     # mismatch counts
        CGcount = 0      # count CG
        caution = 0

        matches = []

        for i in range(2):
            # beginning match
            if i == 0:
                tmp_match = ""
                buff = ""
                for p in range(sLen):
                    if self.debug:
                        print("start analyzing and generating beginning mismatch pair")
                      
                    if p == 0:
                        r = self.swipeLeft(sequence[0])
                        tmp_match += r
                        mismatch += 1
                        buff += self.swipeLeft(sequence[lp])
                    elif (p == lp):
                        r = self.swipeRight(sequence[p])
                        tmp_match += r
                    elif (p != 0) and (CGcount < maxCG) and (caution == 0):
                        if sequence[p] in ['2', '3']:
                            r = self.swipeRight(sequence[p])
                            tmp_match += r
                            CGcount += 1
                            caution = 1
                        elif mismatch < maxLeft:
                            r = self.swipeLeft(sequence[p])
                            tmp_match += r
                            mismatch += 1
                        else:
                            r = self.swipeRight(sequence[p])
                            tmp_match += r
                    elif (p != 0) and (CGcount < maxCG) and (caution == 1):
                        if sequence[p] in ['2', '3']:
                            r = self.swipeLeft(sequence[p])
                            tmp_match += r
                            mismatch += 1
                            caution = 0
                        else:
                            r = self.swipeRight(sequence[p])
                            tmp_match += r
                    else:
                        r = self.swipeRight(sequence[p])
                        tmp_match += r
                tmp_match = self.translator(tmp_match)
                print(tmp_match)
                         
            # ending match
            elif i == 1:
                tmp_match = ""
                buff = ""
                for p in range(sLen):
                    if self.debug:
                        print("start analyzing and generating beginning mismatch pair")
                      
                    if p == 0:
                        r = self.swipeRight(sequence[p])
                        tmp_match += r
                    elif (p == lp):
                        r = self.swipeLeft(sequence[0])
                        tmp_match += r
                        mismatch += 1
                        buff += self.swipeLeft(sequence[lp])
                    elif (p != 0) and (CGcount < maxCG) and (caution == 0):
                        if sequence[p] in ['2', '3']:
                            r = self.swipeRight(sequence[p])
                            tmp_match += r
                            CGcount += 1
                            caution = 1
                        elif mismatch < maxLeft:
                            r = self.swipeLeft(sequence[p])
                            tmp_match += r
                            mismatch += 1
                        else:
                            r = self.swipeRight(sequence[p])
                            tmp_match += r
                    elif (p != 0) and (CGcount < maxCG) and (caution == 1):
                        if sequence[p] in ['2', '3']:
                            r = self.swipeLeft(sequence[p])
                            tmp_match += r
                            mismatch += 1
                            caution = 0
                        else:
                            r = self.swipeRight(sequence[p])
                            tmp_match += r
                    else:
                        r = self.swipeRight(sequence[p])
                        tmp_match += r
                tmp_match = self.translator(tmp_match)
                print(tmp_match)
    
    def swipeLeft(self, n):
        at = ['1', '0']
        gc = ['2', '3']
        if n in at:
            gc += n
            r = random.choice(gc)
        elif n in gc:
            at += n
            r = random.choice(at)
        return r
    
    def swipeRight(self, n):
        if n == '0':
            r = '1'
        elif n == '1':
            r = '0'
        elif n == '2':
            r = '3'
        elif n == '3':
            r = '2'
        return r

    def translator(self, string):
        r = self.getLength(string)
        result = ""
        if '0' in string:
            for i in range(r):
                result += self.numToChar(string[i])
        elif 'A' in string:
            for i in range(r):
                result += self.charToNum(string[i])
        else:
            print("Invalid!")

        if self.debug:
            print("Debug: Result is " + result)
        return result

    def numToChar(self, i):
        if i == '0':
            return 'A'
        elif i == '1':
            return 'T'
        elif i == '2':
            return 'C'
        elif i == '3':
            return 'G'
        else:
            print("======= INVALID INPUT! ==========")
            return None

    def charToNum(self, i):
        i = i.upper()
        if i == 'A':
            return '0'
        elif i == 'T':
            return '1'
        elif i == 'C':
            return '2'
        elif i == 'G':
            return '3'
        else:
            print("======= INVALID INPUT! ==========")
            return None



findMatches()











