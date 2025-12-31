import pandas as pd
import sys

try:
    # Load the result table
    df = pd.read_csv("results/analysis/master_abundance_table.tsv", sep='\t')

    # Sort by the 100% depth column
    # We use 'depth_1.00' which was created by our aggregate.py script
    top_5 = df.sort_values(by='depth_1.00', ascending=False).head(5)

    print("\n" + "="*50)
    print("TOP 5 MOST ABUNDANT SPECIES (SRR1805151)")
    print("="*50)
    print(top_5[['name', 'depth_1.00']].to_string(index=False))
    print("="*50 + "\n")

except FileNotFoundError:
    print("Error: 'master_abundance_table.tsv' not found. Did the Snakemake pipeline finish?")