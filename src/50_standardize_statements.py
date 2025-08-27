import os
from secfsdstools.c_index.companyindexreading import CompanyIndexReader
from secfsdstools.f_standardizer.standardizing import (
    BalanceSheetStandardizer,
    IncomeStatementStandardizer,
    CashFlowStatementStandardizer,
)

CIK = int(os.environ.get("CIK", "320193"))
reader = CompanyIndexReader.get_company_index_reader(cik=CIK)
adshs = reader.get_all_company_reports_df(forms=["10-K"])["adsh"].tolist()

bs_std = BalanceSheetStandardizer.standardize(adshs=adshs)
is_std = IncomeStatementStandardizer.standardize(adshs=adshs)
cf_std = CashFlowStatementStandardizer.standardize(adshs=adshs)

print("BS standardized shape:", bs_std.shape)
print("IS standardized shape:", is_std.shape)
print("CF standardized shape:", cf_std.shape)

bs_std.to_parquet("out/standard_bs.parquet", index=False)
is_std.to_parquet("out/standard_is.parquet", index=False)
cf_std.to_parquet("out/standard_cf.parquet", index=False)
