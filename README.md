# secfsdstools E2E scaffold (free, public SEC FSD)

Caches SEC Financial Statement Data Sets under `~/secfsdstools` (parquet + SQLite). No paid APIs.

## Quick start
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
