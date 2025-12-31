import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output_dir", required=True)
    args = parser.parse_args()

    # Load Data
    df = pd.read_csv(args.input, sep='\t', index_col=0)
    
    # Sort columns by fraction (0.01, 0.10, 0.50, 1.00) so the lines look right
    df = df.reindex(sorted(df.columns), axis=1)
    
    # 1. Rarefaction Curve (Species Richness)
    richness = (df > 0).sum()
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=richness.index, y=richness.values, marker='o', color='royalblue', linewidth=2.5)
    plt.title('Species Discovery (Rarefaction)', fontsize=14)
    plt.xlabel('Subsampling Fraction', fontsize=12)
    plt.ylabel('Number of Species Detected', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(args.output_dir, "rarefaction.png"), dpi=300)
    plt.close()

    # 2. Correlation Bar Chart (Stability)
    gold_col = df.columns[-1] # Assuming 1.00 is the last column
    corrs = df.corrwith(df[gold_col], method='spearman')
    plt.figure(figsize=(8, 5))
    sns.barplot(x=corrs.index, y=corrs.values, palette='viridis')
    plt.title(f'Abundance Correlation to Full Dataset ({gold_col})', fontsize=14)
    plt.ylabel('Spearman Rho', fontsize=12)
    plt.ylim(0, 1.1)
    plt.savefig(os.path.join(args.output_dir, "correlation.png"), dpi=300)
    plt.close()

    # 3. Top 10 Species Heatmap (Visual Verification)
    top_10 = df.sort_values(by=gold_col, ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.heatmap(top_10, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title('Top 10 Most Abundant Species', fontsize=14)
    plt.savefig(os.path.join(args.output_dir, "top_species_heatmap.png"), dpi=300)
    plt.close()

    print(f"Success! 3 plots saved to {args.output_dir}")

if __name__ == "__main__":
    main()