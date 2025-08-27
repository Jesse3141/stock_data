import os
import pandas as pd
from secfsdstools.c_index.companyindexreading import CompanyIndexReader
from secfsdstools.e_collector.reportcollecting import SingleReportCollector
from secfsdstools.e_filters.rawfilingsfilters import (
    ReportPeriodAndPreviousPeriodRawFilter,
    USDOnlyRawFilter,
    NoSegmentInfoRawFilter,
)
from secfsdstools.e_presenter.presenting import StandardStatementPresenter

CIK = int(os.environ.get("CIK", "320193"))
reader = CompanyIndexReader.get_company_index_reader(cik=CIK)
df_10k = reader.get_all_company_reports_df(forms=["10-K"]).sort_values("filed")
adsh = df_10k.iloc[-1]["adsh"]

collector = SingleReportCollector.get_report_by_adsh(adsh=adsh, stmt_filter=["BS","IS","CF"])
bag = collector.collect()

bag = bag.filter(USDOnlyRawFilter()).filter(NoSegmentInfoRawFilter()).filter(ReportPeriodAndPreviousPeriodRawFilter())

presenter = StandardStatementPresenter()
bs = bag.join().present(presenter, stmt="BS")
is_ = bag.join().present(presenter, stmt="IS")
cf = bag.join().present(presenter, stmt="CF")

print("\n=== Balance Sheet (curr & prev) ===\n", bs.head(30))
print("\n=== Income Statement (curr & prev) ===\n", is_.head(30))
print("\n=== Cash Flow (curr & prev) ===\n", cf.head(30))

bs.to_parquet("out/present_bs.parquet", index=False)
is_.to_parquet("out/present_is.parquet", index=False)
cf.to_parquet("out/present_cf.parquet", index=False)
