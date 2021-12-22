from knowknow import *

from load_db import db as dta

top_df_02 = stats.top_decade_stratified(dta, 'c', percentile=0.02, yRange=(1930,2005), debug=False)

top_sort = top_df_02.sort_values('first_added')
top_names = list(top_sort['name'])

print( top_sort.shape[0], 'works in the top 2%' )

dead_top_02 = []

n_dead = 0
n_tot = 0

for i,r in top_sort.iterrows():
    tt = dta.trend('c', r['name'])
    B,D = tt.births_deaths(death_cutoff=0.1)
        
    n_tot += 1
    
    if len(D):
        # if they didn't die *after* they reached the top 1%, skip
        if D[-1] < r['first_added']:
            continue
        
        n_dead += 1
        dead_top_02.append(r['name'])

print(f'{n_dead / n_tot:0.1%} of these works died and {1-n_dead / n_tot:0.1%} are alive')



looking_for_recent = dta(ffa=None, fy=None).cits
rec_auths = set(looking_for_recent[ looking_for_recent.fy >= 2005 ].ffa)
print( len(rec_auths), 'authors published since 2005' )


auth_count = defaultdict(int)
auth_log = defaultdict(set)

for i,cname in enumerate(dead_top_02):
    if (i+1)%(len(dead_top_02)//10) == 0:
        print( 'Processing author ', i+1,"/",len(dead_top_02) )

    cc = dta(ffa=None, c=cname).cits
    cc = cc[cc['count']>1]
    for a in cc.ffa:
        if a not in rec_auths:
            continue
        auth_count[a] += 1
        auth_log[a].add( cname )
        

print(auth_count, 'authors have cited one of the dead at least twice.')