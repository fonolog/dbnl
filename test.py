from sonnetten import poems as sonnetten
import json, string
from collections import OrderedDict

rhymewords = {}

vowel = lambda x: x in "aeiouy"

def rhymes(m):
    for number, letter in enumerate(m):
        if vowel(letter):
            yield m[number:]
        # take care of some spelling variation (final devoicing)
        if m[-1] == 'd':
            yield m[number:-1]+'t'
        if m[-1] == 'b':
            yield m[number:-1]+'p'
        if m[-1] == 'v':
            yield m[number:-1]+'f'
        if m[-1] == 'z':
            yield m[number:-1]+'s'
        #ou = au
        if m[number] == 'o' and len(m) < number+1 and m[number+1]== 'u':
            yield m[:number]+'a'+m[number+1:]
        #ei = ij
        if m[number] == 'i' and len(m) < number+1 and m[number+1]== 'i':
            yield m[:number]+'ij'+m[number+2:]
       


def rijmschema(m,n, my_rhymewords={}):
    potential_rhymeword  = '', None
    if m!=n:
        for x in my_rhymewords[m]:
            for y in my_rhymewords[n]:
                if x == y and len(x) > len(potential_rhymeword[0]):
                    potential_rhymeword = x, n           
    return potential_rhymeword

def rhyming_pairs(sonnet):
        my_rhymewords = {line.strip(string.punctuation+'-_–*').split()[-1]: list(rhymes(line.strip(string.punctuation+'-_–*').split()[-1]))  for line in sonnet['ascii text poem'].split('\n') if len(line.strip(string.punctuation+'-_–*').split())>0 }
        rhymescheme = OrderedDict()
        for m in my_rhymewords:
            potential_rhymeword = '', None
            for n in my_rhymewords:
                    our_rhyme = rijmschema(m, n, my_rhymewords)
                    if len(our_rhyme[0]) > len(potential_rhymeword[0]):
                        potential_rhymeword = our_rhyme
            rhymescheme[m] = potential_rhymeword[1]

        return (rhymescheme)

def abstract_scheme (rhymescheme):
        letter = 'a'
        abstract =  ['' for r in rhymescheme]
        for a in range(len(abstract)):
            if abstract[a] == '':
                abstract[a]=letter
                for b in range(a, len(abstract)):
                    if list(rhymescheme.values())[b] == list(rhymescheme)[a]:
                        abstract[b]=letter
                letter = chr(ord(letter)+1)

        return abstract            



rhyme_schemes = {}
returnstring = ''

for s in sonnetten:

    if (len([l for l in sonnetten[s]['poem']['lg']['l'] if l])) == 14:
        #which words rhyme with each other?
        rhymescheme = rhyming_pairs(sonnetten[s])

        #create rhymescheme 
        key = "".join(abstract_scheme(rhymescheme))
        if key == "abbaabbaccdeed":
            returnstring += str(sonnetten[s]['author'])+'\n'+str(sonnetten[s]['appeared in'])+'\n'+sonnetten[s]['dbnl file']+'\n'+sonnetten[s]['ascii text poem']+'\n\n'
    

        if key in rhyme_schemes:
                rhyme_schemes[key] += [s]
        else: rhyme_schemes[key] = [s]

if __name__ == '__main__':

    for r in sorted(rhyme_schemes):
        if len(rhyme_schemes[r])> 10:
            print (r, len(rhyme_schemes[r]))

    print (returnstring, file=open("canoniekesonnetten.txt", "w"))

