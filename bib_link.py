from csv import DictReader

with open('G:/My Drive/2020 ORGANISATION/1. PROJECTS/qualitative analysis of literature/000 papers/2021 1 american sociologist resub/bib_to_key_map.csv') as in_f:
    rs = list(DictReader(in_f))

mp = {r['WOS']: r['BIB'] for r in rs}

from pybtex.database.input import bibtex


def bib_loop( fn ):
    #open a bibtex file
    parser = bibtex.Parser()
    bibdata = parser.parse_file(fn)

    #loop through the individual references
    for bib_id in bibdata.entries:
        b = bibdata.entries[bib_id].fields
        
        try:
            auths = bibdata.entries[bib_id].persons["author"]
            title = b["title"].replace("{","").replace("}","")
            year = int(b['year'])
            auths_last = [ x.last_names[-1] for x in bibdata.entries[bib_id].persons["author"] ]

            yield {
                'auths': auths,
                'title': title,
                'year': year,
                'auths_last': auths_last,
                'type': bibdata.entries[bib_id].type,
                'key': bib_id
            }

        # field may not exist for a reference
        except(KeyError):
            continue

bibs = {}

bfn = "G:/My Drive/2020 ORGANISATION/1. PROJECTS/qualitative analysis of literature/000 papers/2021 1 american sociologist resub/drafts 3/new_deaths.bib"

for r in bib_loop(bfn):
    bibs[ r['key'] ] = r