import random

chinese = (
    ['b', 'c', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 'sh', 't', 'w', 'x', 'y', 'z', 'zh'],
    ['a', 'ai', 'an', 'ao', 'e', 'ei', 'en', 'i', 'ou', 'u', 'ua', 'ui', 'un']
)

alien = (
    ['b', 'c', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'p', 'q', 's', 'sh', 'w', 'x', 'y', 'z', 'zh', 'sl', 'zl', 'kl', 'gl', 'fl', 'sr', 'zr', 'kr', 'gr', 'fr', 'sn', 'zn', 'kn', 'gn', 'fn'],
    ['a', 'ai', 'an', 'ao', 'e', 'ei', 'ein', 'en', 'i', 'in', 'oi', 'on', 'ou', 'u', 'ua', 'ui', 'un', 'uo', 'ar', 'er', 'or', 'ur', 'ant', 'ent', 'ont', 'unt', 'al', 'el', 'ol', 'ul']
)

english = (
    ['b', 'c', 'ch', 'd', 'j', 'k', 'm', 'p', 's', 'v', 'w', 'x', 'y', 'z', 'sl', 'gl', 'fl', 'cr', 'dr', 'fr', 'pr', 'r'],
    ['al', 'an', 'ain', 'at', 'ate', 'ant', 'ash', 'en', 'ein', 'et', 'ent', 'est', 'in', 'it', 'int', 'ish', 'ist', 'ight', 'ite', 'on', 'ont', 'un', 'unt', 'ought', 'ough', 'eigh'] 
)

alphabets = (chinese, alien, english)


# Per-word construction function
def wordify_word(n, alphabet):
    front, end = alphabet
    return front[n % len(front)] + end[(n // len(front)) % len(end)]


# Converts a number to a series of words
def wordify(n, alphabet):
    front, end = alphabet
    period = len(front) * len(end)
    o = []
    while n > 0:
        o.append(wordify_word(n % period, alphabet))
        n //= period
        if (len(o) % 5) != 0:
            o.append(' ')
    if o[-1] == ' ':
        o.pop()
    return ''.join(o)


# Checks that an alphabet is parseable
def check_consistency(alphabet):
    front, back = alphabet
    for f in front:
        for b in back:
            for i in range(1, 10):
                if f[:i] == b[-i:]:
                    raise Exception("Inconsistency potential: %s %s" % (f,b))
                if f[-i:] == b[:i]:
                    raise Exception("Inconsistency potential: %s %s" % (f,b))
    return True

for alphabet in alphabets:
    check_consistency(alphabet)


# Parses
def parse(words, alphabet):
    front, back = alphabet
    string = ''.join(words.split(' '))
    o = []
    pos = 0
    while pos < len(string):
        outlen, i = 0, 0
        for f in front:
            if f == string[pos:pos+len(f)]:
                for b in back:
                    if b == string[pos+len(f):pos+len(f+b)]:
                        if len(f+b) > outlen:
                            outlen = len(f+b)
                            i = front.index(f) + len(front) * back.index(b)
        if outlen:
            o.append(i)
            pos += outlen
        else:
            raise Exception("Stuck!", pos)
    outval = 0
    for v in o[::-1]:
        outval = outval * len(front) * len(back) + v
    return outval

for i in range(100):
    for a in alphabets:
        v = random.randrange(2**100)
        assert parse(wordify(v, a), a) == v, (a, v, parse(wordify(v, a), a))
