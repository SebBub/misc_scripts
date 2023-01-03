from pyesgf.search import SearchConnection
conn = SearchConnection('http://esgf-index1.ceda.ac.uk/esg-search',
                        distrib=False)

#%%
ctx = conn.new_context(project='CORDEX', query='temperature')
print('Hits:', ctx.hit_count)
print('Institute:')
ctx.facet_counts['institute']
#%%
from pyesgf.logon import LogonManager
lm = LogonManager()
lm.logoff()
lm.is_logged_on()