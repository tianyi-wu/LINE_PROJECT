import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django
django.setup()



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
