# -*- coding: utf-8 -*-
import sys
import os
import re
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django
#django.setup()

import LDAmodel # import lda_parts, News, get_words
import gensim


from feedreader.models import Entry

def get_data():
    from feedreader.models import Entry
    Entrys = Entry.objects.all()
    n = len(Entrys)
    PKs = [Entrys[i].pk for i in range(n)]
    #Links = [Entrys[i].link for i in range(n)]
    
    p = re.compile(r"<[^>]*?>")

    Titles = [p.sub("", Entrys[i].title) for i in range(n)]

    Descriptions = [p.sub("", Entrys[i].description) for i in range(n)]

    return [PKs, Titles, Descriptions]






if __name__ == '__main__':
    argvs = sys.argv
    [PKs, Titles, Descriptions] = get_data()

    filters = True
    show = False
    num_topics = 50
    no_below = 5
    no_above = 0.4
    if len(argvs) == 2 and sys.argv[1] == 'initial':

        title_lda  =  LDAmodel.lda_parts(Titles)
        title_lda.dictionary_corpus(filters = filters,show = show,save  =  ("./model/titles.dictionary"), no_below = no_below, no_above = no_above)
        print "dictionary of title made"

        title_lda.LDA_model(num_topics = num_topics,save = ("./model/titles.model"),show = show,set_matrix = False)
        print "LDA of title made"

        description_lda  =  LDAmodel.lda_parts(Descriptions)
        description_lda.dictionary_corpus(filters = filters,show = show, save  =  ("./model/descriptions.dictionary"), no_below = no_below, no_above = no_above)
        print "dictionary of description made"
        description_lda.LDA_model(num_topics = num_topics,save = ("./model/descriptions.model"),show = show,set_matrix = False)
        print "LDA of description made"

    else:


        NewsEntry = LDAmodel.News(PKs, Titles ,Descriptions, filters = True,show=False, no_below=no_below, no_above=no_above)
        NewsEntry.calculate_relevent()
        entrys = Entry.objects.all()

        for entry in entrys:

            Revelant = NewsEntry.RelevantList[entry.pk]

            if len(Revelant) == 1:
                entry.FisrtRevelant = Entry.objects.get(pk=Revelant[0])
                print 1
            elif len(Revelant) == 2:
                entry.FisrtRevelant = Entry.objects.get(pk=Revelant[0])
                entry.SecondRevelant = Entry.objects.get(pk=Revelant[1])
                print 2
            elif len(Revelant) == 3:
                entry.FisrtRevelant = Entry.objects.get(pk=Revelant[0])
                entry.SecondRevelant = Entry.objects.get(pk=Revelant[1])
                entry.ThirdRevelant = Entry.objects.get(pk=Revelant[2])
                print 3


            entry.save()
            print "save ok"


            

