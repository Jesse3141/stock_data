import os
from secfsdstools.e_collector.reportcollecting import SingleReportCollector

ADSH = os.environ.get("ADSH", "0000320193-22-000108")  # Apple 2022 10-K
col = SingleReportCollector.get_report_by_adsh(adsh=ADSH)
bag = col.collect()

print("sub_df head:\n", bag.sub_df.head())
print("pre_df.shape:", bag.pre_df.shape, "num_df.shape:", bag.num_df.shape)

bag.save("out/single_report_raw")  # writes sub/pre/num as parquet under out/
