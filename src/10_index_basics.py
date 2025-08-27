from secfsdstools.c_index.searching import IndexSearch
from secfsdstools.c_index.companyindexreading import CompanyIndexReader
import pandas as pd

idx = IndexSearch.get_index_search()
hits = idx.find_company_by_name("apple")
print(">>> find_company_by_name('apple'):\n", pd.DataFrame(hits).head(10))

cik = 320193
r = CompanyIndexReader.get_company_index_reader(cik=cik)
print("\n>>> latest filing:\n", r.get_latest_company_filing())
print("\n>>> 10-K reports since 2010 (head):\n", r.get_all_company_reports_df(forms=["10-K"]).head())

pd.DataFrame(hits).to_parquet("out/index_search_apple.parquet", index=False)
