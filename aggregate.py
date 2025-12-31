import pandas as pd
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("input", nargs="+")
    args = parser.parse_args()

    all_dfs = []

    for f in args.input:
        # Get filename like 'SRR1805151_0.10'
        base = os.path.basename(f).replace(".species.bracken", "")
        
        # Extract just the fraction (the part after the underscore)
        # This helps the plotter sort columns numerically
        fraction = base.split('_')[-1] 
        
        df = pd.read_csv(f, sep='\t')
        
        # We only need the name and the abundance count
        df = df[['name', 'new_est_reads']]
        df.columns = ['Species', fraction]
        df.set_index('Species', inplace=True)
        all_dfs.append(df)

    # Combine all columns into one table
    # axis=1 means "match by Species name (rows)"
    master = pd.concat(all_dfs, axis=1).fillna(0)
    
    # Save as a Tab-Separated file
    master.to_csv(args.output, sep='\t')
    print(f"Combined {len(all_dfs)} samples into {args.output}")

if __name__ == "__main__":
    main()