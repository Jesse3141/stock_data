```markdown

# secfsdstools E2E scaffold (free, public SEC FSD)
https://github.com/HansjoergW/sec-fincancial-statement-data-set

data saved to C:\Users\Jesse\secfsdstools\data\[parquet\quarte

Caches SEC Financial Statement Data Sets under `~/secfsdstools` (parquet + SQLite). No paid APIs.

## Quick start

### Cloud Dev Setup (GitHub Codespaces, etc.)

This repo includes a small subset of SEC data (`small_data/`) for quick development without downloading the full dataset.

**Prerequisites:**
```bash
# Install Git LFS before cloning
git lfs install
```

**Clone and setup:**
```bash
git clone <repo-url>
cd edgar_api
git lfs pull              # Download LFS-tracked data files (~1.8GB)
conda env create -f environment.yml
conda activate secfsd
```

The repo includes a `.secfsdtools.cfg` that points to `./small_data/` instead of `~/secfsdstools/`. Data is ready to use immediately - no `make update` needed!

**Available data:** 2022Q1-2025Q2 (14 quarters) for testing and development.

### Local Setup (Full Dataset)

```bash
conda env create -f environment.yml
conda activate secfsd
make update              # ~2–4+ GB on first run
make index               # demo index search & filings
CIK=320193 make single   # Apple 2022 10-K by ADSH (example inside)
CIK=320193 make company  # all Apple 10-K raw joins
CIK=320193 make present  # BS/IS/CF (current & previous period)
CIK=320193 make standard # standardized comparable BS/IS/CF
```


## how to use: see notebook 3


easily look up the cik from company name. 

get report for chosen company

a key feature is the report standardiser:
bs_standardizer = BalanceSheetStandardizer()
is_standardizer = IncomeStatementStandardizer()
cf_standardizer = CashFlowStandardizer()

income statement:
Revenues - CostOfRevenue = GrossProfit
OperatingExpenses: SG&A + other operating expenses
AllIncomeTaxExpenseBenefit: provision for taxes or taxes
NetIncomeLoss: actual income. after operating cashflows. 

Cashflow:
recall that 'accounting' costs, such as depreciation are usually added back in cashflow since no actual cash  expense was registered for the depreciation. 
also taxes - often a difference between when tax liabilty recognised to when actually paid (buffet called this an interest free loan). 
simmilarly, while giving workers stocks (sharebased compensation) is registered as a cost, it doesn't actually involve cash.
recievables: how much they are owed. means that of the profit registered, some hasn't actually been collected as cash. so when increase - a cash outlfow. 
accounts payable is the opposite: the comapny owes (registered cost) but actaully still has the cash. ditto accrued liabilaties. 


NetCashProvidedByUsedInFinancingActivitiesContinuingOperations: everythin the registered under financing activities: debt payment and issuance, stock, dividende etc




# collector 
loads data  into rawdatabag. 
it diffrentiates between the get flow, and the collect. 
during get, define what to get, and how to filter. like dask graph building, before execution.
collect gets the data according to the get plan. eg:
````
collector: SingleReportCollector = SingleReportCollector.get_report_by_adsh(adsh=apple_10k_2022_adsh, stmt_filter=['BS'])
rawdatabag = collector.collect()
```
would only load the balance sheet.
after collect, the data is in a raw data bag, with:
1. sub_df: company meta
2. pre_df (presentatio): info on the tags in the report and their meaning or human labels. 
```
                                                   tag       version              plabel
stmt                                    tag       version                     plabel
0   BS  CashAndCashEquivalentsAtCarryingValue  us-gaap/2020  Cash and cash equivalents
1   BS                  ReceivablesNetCurrent  us-gaap/2020           Receivables, net
```
3. num_df: the actual values for the tags

note, the filtering applies to pre_df, which knows which statement each value belongs to. 
raw databag has a join method which joins the num_df on the pre_df to apply filtering
can also filter by tag.

`MultiReportCollector` can colect and integrate data from multiple reports by index or adsh.

## company collector
collects data for multiple companies:
```
apple_cik = 320193
microsoft_cik = 789019
collector = CompanyReportCollector.get_company_collector(ciks=[apple_cik, microsoft_cik])
```
