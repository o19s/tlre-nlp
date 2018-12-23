import sys
import pandas
import pickle
import pysolr
import spacy
from tmdbMovies import indexableMovies 

nlp = spacy.load('en')
#nlp = spacy.load('en_core_web_md')
#nlp = spacy.load('en_core_web_lg')

def extract_location_entities(text):
    #debug here:
    # https://explosion.ai/demos/displacy?text=Kevin%20McAllister%20in%20New%20York%20NY&model=en_core_web_lg&cpu=1&cph=1

    #merge entities and noun chunks into one token
    doc = nlp(text)
    spans = list(doc.ents)# + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for gpe in filter(lambda w: w.ent_type_ in ['GPE'], doc):
        if gpe.dep_ in ('attr', 'dobj'):
            subject = [w for w in gpe.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append(gpe.text)
        elif gpe.dep_ == 'pobj' and gpe.head.dep_ == 'prep':
            relations.append(gpe.text)
        else:
            relations.append(gpe.text)

    return relations


def enrichMovies():
    total_docs = 0
    total_enriched = 0
    enrichments = []
    for movie in indexableMovies():
        text = movie["title"]
        locations = extract_location_entities(text)
        total_docs += 1
        if locations:
            enrichments.append({"id":movie["id"],"title":text,"locations":locations})
            total_enriched += 1
    return total_docs,total_enriched,enrichments


def doEnrichment():
    t_docs,t_enr,enrichments = enrichMovies()
    print("Total documents:",t_docs)
    print("Total enriched:",t_enr)
    with open("location_enrichments.pickle",'wb') as outfile:
        pickle.dump({ "enrichments": enrichments }, outfile, protocol=pickle.HIGHEST_PROTOCOL)


def generateBlankTestData():
    ids = []
    texts = []
    annotations = []
    notes = []
    for movie in indexableMovies():
        ids.append(movie["id"])
        texts.append(movie["title"])
        annotations.append(None)
        notes.append(None)
    df = pandas.DataFrame({ 'id': ids, 'text' : texts, 'annotation': annotations, 'note': notes }).set_index('id')
    df.to_csv('test_titles_blank.csv')


#solr = pysolr.Solr('http://localhost:8983/solr/tmdb', timeout=100)
#solr.add(indexableMovies())


#doEnrichment times:
    # Small Model:
    #Total documents: 27760
    #Total enriched: 1970 (7.1%)
    #real   2m52.110s
    #user   11m14.734s
    #sys    0m1.718s

    # Medium Model:
    #Total documents: 27760
    #Total enriched: 1546 (5.5%)
    #real   2m48.141s
    #user   10m20.899s
    #sys    0m1.895s

    # Large Model:
    #Total documents: 27760
    #Total enriched: 1363 (4.9%)
    #real   2m56.602s
    #user   10m54.645s
    #sys    0m4.119s