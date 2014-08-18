import httplib
import json
from random import randint


#how to generate a haiku:

#start with an array of words
#download info on each word including syllable count
#store in dict by syllable count
#randomly generate 3 strings of ints that add up to 5 7 5 using only ints that have an value in the dict
#pick from the syllable sorted dict to fill in the randomly created template


#summarized in haiku form:

#Generate vocab,
#sort by syllabic value,
#select to fit form.


class SomeWords(object):
    #start with an array of words
    initial = [
    "a","an","I","he","she","we","were","will","can","might","not","do","have","been","blazes","rage","destruction","life","animocity","smoke","gunshot","siren","sirens","epihony","hamburger","scientific", "religious", "butterfly","beach", "tranquil","sunshine"]

    syllables = {}

    #download info on each word including syllable count
    def download_info(self, get_rhymes=True):
        print "INITIAL WORDS"
        self.deliniate(self.initial)
        for word in self.initial:
            if get_rhymes:
                response = self.request("rhymebrain.com/talk?function=getRhymes&word="+word)
            else:
                response = self.request("rhymebrain.com/talk?function=getWordInfo&word="+word)
            self.parse_rhymebrain(response)
            #store in dict by syllable count

    def parse_rhymebrain(self, response):
        rhyming_words = json.loads(response)
        for w in rhyming_words:
            syllable_count = int(w["syllables"])
            if self.syllables.has_key(syllable_count):
                self.syllables[syllable_count].append(w)
            else:
                self.syllables.__setitem__(syllable_count, [])

    def deliniate(self, array):
        output =  ', '.join(array)
        print output
        return output

    def request(self, url):
        host = url.split('/')[0]
        #if urls do contain 'http://' -->  host = url.split('/')[2].replace('http://','')
        req = url[url.find(host)+len(host):]
        conn = httplib.HTTPConnection(host)
        conn.request("GET","/"+req)
        response = conn.getresponse()
        return response.read()

    def write_line_with_this_many_syllables(self, syllable_count):
        #pick from the syllable sorted dict to fill in the randomly created template
        sequence = self.get_syllabic_sequence(syllable_count)
        line = ""
        for s in sequence:
            line+= random.choice(self.syllables[s])["word"]+" "
        return line


    def get_syllabic_sequence(self, syllable_count):
        available = self.syllables.keys()
        sequence = []
        max_tries = 100
        tries = 0
        while sum(sequence) < syllable_count:
            sequence.append(random.choice(available))
            if sum(sequence) > syllable_count:
                sequence.pop()
            tries += 1
            if tries > max_tries:
                sequence = []
                tries = 0

        print sequence
        return sequence

    def write_haiku(self):
        #randomly generate 3 strings of ints that add up to 5 7 5 using only ints that have an value in the dict
        output = ""
        output += words.write_line_with_this_many_syllables(5)+","
        output +=  words.write_line_with_this_many_syllables(7)+","
        output +=  words.write_line_with_this_many_syllables(5)+"."
        return output


#the final execution is itself a haiku if read aloud

words = SomeWords()
words.download_rhyme_info()
words.write_haiku()