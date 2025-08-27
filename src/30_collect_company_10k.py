import os
from secfsdstools.e_collector.companycollecting import CompanyReportCollector

CIK = int(os.environ.get("CIK", "320193"))

collector = CompanyReportCollector.get_company_collector(ciks=[CIK], forms_filter=["10-K"])
bag = collector.collect()
print("sub_df head:\n", bag.sub_df.head())
print("pre_df.shape:", bag.pre_df.shape, "num_df.shape:", bag.num_df.shape)

joined = bag.join()
joined.pre_num_df.head(1000).to_parquet("out/company_join_sample.parquet", index=False)
