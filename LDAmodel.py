# -*- coding: utf-8 -*-
import MeCab
import pandas as pd
import gensim
import numpy
import re

# process in mecab 

def get_words(contents):
    ret = []
    for content in contents:
        ret.append(get_words_main(content))
    return ret

def get_words_main(content):
    return tokenlize(content)

def tokenlize(text):
    #mecab = MeCab.Tagger("-Owakati")
    #node = mecab.parse(text.encode('utf-8'))
    #return node
    text=text.encode('utf-8')
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text)#.encode('utf-8'))
    keywords = []

    while node:
        # if len(node.surface) > 1:
        #     keywords.append(node.surface)
        # node = node.next
        if node.feature.split(",")[0] ==  '名詞':
            #yield node.surface
            if len(node.surface) > 1:
                keywords.append(node.surface)
        node = node.next
    return keywords




#process in LDA model

class lda_parts(object):
    '''docstring for lda_parts'''

    def __init__(self,sentencelist):
        #self.sentencelist = sentencelist
        self.wordslist = get_words(sentencelist)

    def dictionary_corpus(self, filters = True, load = None ,save = None, show=False,no_below=5, no_above=0.75):
        if load == None:
            dictionary = gensim.corpora.Dictionary(self.wordslist)
        if load == None and filters == True: 
            dictionary.filter_extremes(no_below,no_above)
        else:
            dictionary = gensim.corpora.Dictionary.load(load)
        self.dictionary = dictionary
        if save != None:
            self.dictionary.save(save)
        
        self.corpus = [self.dictionary.doc2bow(words) for words in self.wordslist]
        


    def LDA_model(self,num_topics=150,save=None,load=None,show=False,set_matrix = True):
        if load == None:
            self.lda = gensim.models.LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=num_topics)    
            self.lda.save(save)
        else:
            self.lda = gensim.models.LdaModel.load(load)

        if show == True:
            for topic in self.lda.show_topics(-1):
                print topic
        if set_matrix:
            self.similarity_matrix()

    def similarity_matrix(self):
        self.matrix = gensim.similarities.MatrixSimilarity(self.lda[self.corpus])

    def similarity_vector(self,p_sentence):
        p_corpus = self.dictionary.doc2bow(tokenlize(p_sentence))
        return self.matrix[self.lda[p_corpus]]





class News(object):
    def __init__(self, PKs, titles , descriptions, filters = True,show=False, no_below=5, no_above=0.75):
        self.n = len(PKs)
        self.PKs = PKs
        self.titles = titles
        self.descriptions = descriptions
        self.RelevantList = {}

        self.title_lda = lda_parts(titles)
        self.title_lda.dictionary_corpus(filters=filters,load = ("./model/titles.dictionary"), show=show, no_below=no_below, no_above=no_above)
        self.title_lda.LDA_model(load=("./model/titles.model"),show=show)
        self.title_lda.similarity_matrix()
        #self.titile_similarMatrix = self.title_lda.matrix

        self.description_lda = lda_parts(descriptions)
        self.description_lda.dictionary_corpus(filters=filters,load = ("./model/descriptions.dictionary"), show=show,no_below=no_below, no_above=no_above)

        self.description_lda.LDA_model(load=("./model/descriptions.model"),show=show) 
        self.description_lda.similarity_matrix()
        #self.description_similarMatrix = self.description_lda.matrix
        self.p = re.compile(r"<[^>]*?>")

    def calculate_relevent(self):
        for k in range(self.n):
            sim_title = numpy.array(self.title_lda.similarity_vector(self.titles[k]))
            sim_description = numpy.array(self.description_lda.similarity_vector(self.descriptions[k]))

            sort_title = numpy.argsort(sim_title)
            sort_description = numpy.argsort(sim_description)

            resultTitle  = [(sort_title[self.n-1-x],sim_title[sort_title[self.n-1-x]]) for x in range(self.n) if sort_title[self.n-1-x] != k and 0.1 < sim_title[sort_title[self.n-1-x]] < 1.0] 
            resultDescription  = [(sort_description[self.n-1-x],sim_description[sort_title[self.n-1-x]]) for x in range(self.n)if sort_description[self.n-1-x] != k and 0.1 < sim_title[sort_description[self.n-1-x]] < 1.0] 
            mostRelevant = []

            print k
            print resultTitle,resultDescription
            print len(self.PKs)
            while len(mostRelevant) <= 3:
                if len(resultTitle) == 0 and len(resultDescription) == 0:
                    break

                if len(resultTitle) == 0:
                    mostRelevant.append(resultDescription[0][0])
                    del resultDescription[0]


                if len(resultDescription) == 0:
                    mostRelevant.append(resultTitle[0][0])
                    del resultTitle[0]



                if resultTitle[0][1] >= resultDescription[0][1]:
                    if resultTitle[0][0] not in mostRelevant:
                        mostRelevant.append(resultTitle[0][0])
                        del resultTitle[0]
                    else:
                        del resultTitle[0]
                else:
                    if resultDescription[0][0] not in mostRelevant:
                        mostRelevant.append(resultDescription[0][0])
                        del resultDescription[0]
                    else:
                        del resultDescription[0]
            print mostRelevant
            self.RelevantList[self.PKs[k]] = [self.PKs[i] for i in mostRelevant]
        print 'calculate_relevent over'
        return 0
