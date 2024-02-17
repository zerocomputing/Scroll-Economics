import pandas as pd
import matplotlib.pyplot as plt

'''
GOAL: Show that # transactions, # of batches, and gas utilization are in positive, ~linear correlation.
Datafram:
| Date | Daily txs | Daily batches | Daily gas utilization |
'''

pd.set_option('display.max_columns', None)

file_path = 'Datasets/Scroll - txs, batches, blocks.csv'
df = pd.read_csv(file_path)

drop_columns = ['Month', 'Daily total blocks', 'Daily addresses', 'Daily gas used']
df.drop(drop_columns, axis=1, inplace=True)
print(df)

# Assuming df is your DataFrame
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plotting the first set of data (Daily total txs, Daily batches)
df.plot(x='Date', y=df.columns[1:3], kind='line', marker='o', ax=ax1, logy=True)
ax1.set_xlabel('Date')
ax1.set_ylabel('Daily Txs/Batches (log scale)')


# Creating a secondary y-axis for 'Daily gas utilization' with symlog scale
ax2 = ax1.twinx()
ax2.plot(df['Date'], pd.to_numeric(df['Daily gas utilization (average gas used/gas limit)'].str.rstrip('%')), color='red', marker='o', label='Daily gas utilization (%)')
ax2.set_ylabel('Daily Gas Utilization (%)')

# Set higher maximum range for the y-axes
ax1.set_ylim(bottom=1, top=3000000)  # Adjusted upper limit
ax2.set_ylim(bottom=0, top=23)  # Adjusted upper limit

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.savefig('Figures/correlation.png', bbox_inches='tight', dpi=300)
plt.title('Line Plot with Log Scale for Columns and Secondary Y-axis for Gas Utilization')
plt.show()

