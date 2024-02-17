import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)  # Display all columns
 
# Read the CSV file into a DataFrame
file_path = 'Datasets/Scroll_daily_blocks_batches.csv'
df = pd.read_csv(file_path)

# Rename columns
df.rename(columns={'Month': 'month'}, inplace=True)
df.rename(columns={'Daily total blocks': 'daily_blocks'}, inplace=True)
df.rename(columns={'Daily total txs': 'daily_txs'}, inplace=True)
df.rename(columns={'Daily batches': 'daily_batches'}, inplace=True)

avg_daily_txns_scroll = 141188 # 141,188 txns/day
avg_daily_txns_zksync = 1404031 # 1,404,031 txns/day

avg_daily_blocks_scroll = 26930
# avg_daily_chunks_scroll= 6284
avg_daily_batches_scroll= 628 

# Assumptions (?)
avg_txs_per_chunk_scroll =  22.47
avg_proving_time_20 = 20 # 20 minutes
daily_prover_capacity_20 = 60/avg_proving_time_20*24
avg_proving_time_15 = 15 # 15 minutes
daily_prover_capacity_15 = 60/avg_proving_time_15*24

# daily_txs | daily_blocks | daily_chunks | daily_batches | total_daily_proofs | prover_daily_capacity | daily_prover_demand

# Calculate chunk proofs per day
df['daily_chunks'] = df['daily_txs'] / avg_txs_per_chunk_scroll
df['daily_chunks'] = df['daily_chunks'].apply(math.ceil)

# Calculate total daily proofs
df['total_daily_proofs'] = df['daily_chunks'] + df['daily_batches'] 

# Calculate daily prover demand
df['daily_prover_demand_20'] = df['total_daily_proofs'] / daily_prover_capacity_20
df['daily_prover_demand_15'] = df['total_daily_proofs'] / daily_prover_capacity_15

# Calculate daily prover demand with added noise
noise_factor = 0.2  # Adjust the noise factor as needed
noise_20 = np.random.normal(0, noise_factor * df['daily_prover_demand_20'].mean(), len(df))
noise_15 = np.random.normal(0, noise_factor * df['daily_prover_demand_15'].mean(), len(df))

df['daily_prover_demand_20_noisy'] = df['daily_prover_demand_20'] + noise_20
df['daily_prover_demand_15_noisy'] = df['daily_prover_demand_15'] + noise_15

# Reorder columns
desired_column_order = ['month', 'daily_txs', 'daily_blocks', 'daily_chunks', 'daily_batches', 'total_daily_proofs', 'daily_prover_demand_20_noisy', 'daily_prover_demand_15_noisy']




# Number of steps for incremental increase
num_steps = 10

# Create a figure with two subplots
fig, (ax1_incremental, ax2_incremental) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'hspace': 0.4})

# Plot 'daily_prover_demand' on the secondary y-axis with added noise for each step
color_demand_20_incremental = 'tab:blue'

# Initialize a legend list to collect handles and labels
legend_handles = []

for step in range(1, num_steps + 1):
    # Increase daily transactions incrementally towards 10x
    df_incremental = df.copy()
    df_incremental['daily_txs'] = df_incremental['daily_txs'] * (step / num_steps)

    # Add noise to daily transactions for incremental values
    noise_txs_incremental = np.random.normal(0, noise_factor * df_incremental['daily_txs'].mean(), len(df_incremental))
    df_incremental['daily_txs_noisy'] = df_incremental['daily_txs'] + noise_txs_incremental

    # Recalculate chunk proofs per day for incremental values
    df_incremental['daily_chunks'] = df_incremental['daily_txs_noisy'] / avg_txs_per_chunk_scroll
    df_incremental['daily_chunks'] = df_incremental['daily_chunks'].apply(math.ceil)

    # Recalculate total daily proofs for incremental values
    df_incremental['total_daily_proofs'] = df_incremental['daily_chunks'] + df_incremental['daily_batches']

    # Recalculate daily prover demand for incremental values
    df_incremental['daily_prover_demand_20'] = df_incremental['total_daily_proofs'] / daily_prover_capacity_20

    # Calculate daily prover demand with added noise for incremental values
    noise_20_incremental = np.random.normal(0, noise_factor * df_incremental['daily_prover_demand_20'].mean(), len(df_incremental))
    df_incremental['daily_prover_demand_20_noisy'] = df_incremental['daily_prover_demand_20'] + noise_20_incremental

    # Plot 'daily_txs_noisy' on the primary y-axis for incremental values with noise
    line_handle_txs = ax1_incremental.plot(df_incremental.index, df_incremental['daily_txs_noisy'], label=f'{step}x tx vol')[0]

    # Plot 'daily_prover_demand' on the secondary y-axis with added noise for incremental values
    line_handle_prover = ax2_incremental.plot(df_incremental.index, df_incremental['daily_prover_demand_20_noisy'], label=f'{step}x tx vol')[0]

# Additional plot adjustments for incremental values
ax1_incremental.set_ylabel('Daily Transactions')

ax2_incremental.set_ylabel('Daily Prover Demand')

# Create a single legend outside the plotting area
plt.legend(handles=legend_handles, labels=[f'{step}x tx vol' for step in range(1, num_steps + 1)], loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

plt.savefig('Figures/projections.png', bbox_inches='tight', dpi=300)
plt.suptitle('Scroll Daily Transactions and Daily Prover Demand', y=0.95, fontsize=16)
plt.show()
