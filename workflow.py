"""
note: recommendations at the bottom if you want to skip the details
Objectives of this file
Data collection -> read in raw data
Data Cleanup -> if necessary
Data Exploration -> find patterns/relationships & underlying trends
Data Visualization -> show findings, paint the picture you see in the numbers
"""

#setup
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#DATA COLLECTION
#reading in the data and creating additional columns
pL = pd.read_csv('sample_pnl_statement.csv')
pL['date'] = pd.to_datetime(pL['date'])
pL.set_index('date', inplace=True)

#DATA CLEANUP
#deriving useful indicators 
pL['Gross Profit'] = pL['revenue'] - pL['cogs']
pL['Net Profit'] = pL['revenue'] - (pL['cogs']+ pL['marketing_expense']+pL['operating_expenses']+pL['other_expenses']+pL['salaries'])
pL['Profit Margin'] = pL['Net Profit']/pL['revenue']
pL['cogs_pct']=(pL['cogs']/pL['revenue'])*100
pL['marketing_pct']=(pL['marketing_expense']/pL['revenue'])*100
pL['opExp_pct']=(pL['operating_expenses']/pL['revenue'])*100
pL['salaries_pct']=(pL['salaries']/pL['revenue'])*100
pL['other_expenses_pct']=(pL['other_expenses']/pL['revenue'])*100
#check for empty and duplicate values
print(pL.isnull().sum())
print(pL.duplicated().sum())

#grouping data by quarter
pL['quarter'] = pL.index.to_period('Q')


#DATA EXPLORATION
"""
broken into several questions we're here to answer
Revenue -> trends over time/seasonality patterns?
Costs -> costs as a % of rev/ are some costs increasing faster than others(and rev?)
profitability -> Margin trends over time
"""
#Revenue
#quarterly revenue
quarterly_revenue = pL.groupby('quarter')['revenue'].sum()
quarterly_revenue_change = quarterly_revenue.diff()
quarterly_revenue_changePct=quarterly_revenue.pct_change()*100
quarterly_revenue_df = quarterly_revenue.to_frame(name='revenue')
quarterly_revenue_df['qoq_change'] = quarterly_revenue_df['revenue'].diff()
quarterly_revenue_df['qoq_pct_change'] = quarterly_revenue_df['revenue'].pct_change() * 100

#Costs
#quarterly costs
quarterly_cogs = pL.groupby('quarter')['cogs'].sum()
quarterly_cogs_changePct = quarterly_cogs.pct_change()*100

quarterly_marketingExp = pL.groupby('quarter')['marketing_expense'].sum()
quarterly_marketingExp_changePct = quarterly_marketingExp.pct_change()*100

quarterly_operatingExp = pL.groupby('quarter')['operating_expenses'].sum()
quarterly_operatingExp_changePct = quarterly_operatingExp.pct_change()*100

quarterly_salaries = pL.groupby('quarter')['salaries'].sum()
quarterly_salaries_changePct = quarterly_salaries.pct_change()*100

quarterly_otherExpenses = pL.groupby('quarter')['other_expenses'].sum()
quarterly_otherExpenses_changePct = quarterly_otherExpenses.pct_change()*100

quarterly_exp_df=quarterly_revenue_changePct.to_frame(name='revenue pct')
quarterly_exp_df['cogs_pct']=quarterly_cogs_changePct
quarterly_exp_df['opExp_pct']=quarterly_operatingExp_changePct
quarterly_exp_df['marketing_pct']=quarterly_marketingExp_changePct
quarterly_exp_df['salaries_pct']=quarterly_salaries_changePct
quarterly_exp_df['otherExp_pct']=quarterly_otherExpenses_changePct
print(pL)


#Profitability
#quarterly margins
quarterly_net_profit = pL.groupby('quarter')['Net Profit'].sum()
quarterly_margins = quarterly_net_profit/quarterly_revenue
qoq_mar_change = quarterly_margins.diff()
qoq_mar_pct_change=quarterly_margins.pct_change()*100


#export to new csv
pL.to_csv("cleaned_pnl.csv",index=True)
#DATA VISUALIZATION
#taking a look at the data and prepping key findings
print(quarterly_revenue_df)
print(pL)
print(pL.describe().round(2))

pL.hist(bins=25)

quarterly_exp_df.plot(title='QOQ expenses & revenue Growth (%)')
plt.show()


pL['revenue'].plot(title='Revenue Over Time')
plt.show()
quarterly_revenue.plot(title='Revenue per Quarter')
plt.show()
#revenue growth is steady and seasonal, consistent boost from Q2-Q3 - trend could be forecasted for better inventory preparedness

quarterly_revenue_df['qoq_pct_change'].plot(title='Quarter-over-Quarter Sales Growth (%)')
plt.axhline(0, color='black', linewidth=1)
plt.show()


quarterly_margins.plot(title='margins per quarter')
plt.show()
#again seasonal trends showing strong performance from q2-q3

pL.plot(y=['cogs_pct','opExp_pct','marketing_pct','salaries_pct','other_expenses_pct'],title="costs as a perc of rev")
plt.show()
#cogs remain the biggest cost driver - over 50% year on year - most leverage on margin should we find efficiencies - bulk deals, alternative distributors etc.
#marketing costs are rising faster than revenue - needs to be looked into
#cogs remains steady as revenue grows - strong pricing power/supply chain management
#operating expenses & salaries shrinking as revenue grows - efficiencies developing!
#other expenses are also slowly declining while remaining a small less significant portion of costs (<5%)
print("EXECUTIVE SUMMARY")
print("-----------------")
print(f"Total Revenue: ${pL['revenue'].sum():,.0f}")
print(f"Average Profit Margin: {pL['Profit Margin'].mean()*100:.2f}%")
print(f"Highest Revenue Quarter: {quarterly_revenue.idxmax()}")
"""
Key recommendations:
1. Revisit marketing spending as costs are rising faster than sales
2. Revenue is growing steady and seasonal, prepare sufficient resources for q2-q3 sales boost
3. Operational efficiency initiatives are proving successful and should be continued
4. COGS remain consistent as revenue grows, as our main cost driver (~50%) we 
should seek options for efficiencies/savings for the most effective margin gains.
"""
