import intake
import requests

col_url = "https://raw.githubusercontent.com/NCAR/intake-esm-datastore/master/catalogs/pangeo-cmip6.json"
col = intake.open_esm_datastore(col_url)

col.df.columns
col.df.dcpp_init_year.unique()
col.df.experiment_id.unique().shape

# %% read in hist-1950
hist_1950_pr_smalltest = col.search(experiment_id='hist-1950', variable_id='pr',
                                    source_id=['HadGEM3-GC31-LL', 'HadGEM3-GC31-HH'])
hist_1950_pr_smalltest.df.head()
hist_1950_pr_smalltest_data = hist_1950_pr_smalltest.to_dataset_dict()
# %%
print(col.df.columns)
print(col.df.experiment_id.unique().shape)

print(requests.get(col_url).json())

print(col.df.columns)
print(col.df['variable_id'].unique().shape)
print(col.unique())
col_subset = col.search(experiment_id='historical')
print(col_subset.unique())
print(col.aggregation_info)
