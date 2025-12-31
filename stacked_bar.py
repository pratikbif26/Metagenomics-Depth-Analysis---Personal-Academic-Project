import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # 1. Load the master table
    input_file = "results/analysis/master_abundance_table.tsv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    df = pd.read_csv(input_file, sep='\t')
    df = df.set_index('name')

    # 2. Identify Top 5 species based on the 100% depth
    top_5_names = df.sort_values(by='depth_1.00', ascending=False).head(5).index
    
    # 3. Filter for Top 5 and group everything else as "Others"
    top_df = df.loc[top_5_names]
    others_df = df.drop(top_5_names).sum().to_frame(name='Others').T
    
    # Combine them
    plot_df = pd.concat([top_df, others_df])

    # 4. Convert to Relative Abundance (Percentages)
    # This makes the bars equal in height so we can compare proportions
    plot_df_percent = plot_df.div(plot_df.sum(axis=0), axis=1) * 100

    # 5. Transpose for plotting (Fractions on X-axis)
    plot_df_percent = plot_df_percent.T

    # 6. Generate the Plot
    plt.figure(figsize=(12, 7))
    plot_df_percent.plot(kind='bar', stacked=True, colormap='Spectral', width=0.8)

    plt.title("Effect of Subsampling on Taxonomic Relative Abundance", fontsize=14)
    plt.xlabel("Subsampling Depth (Fraction)", fontsize=12)
    plt.ylabel("Relative Abundance (%)", fontsize=12)
    plt.legend(title="Species", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the plot
    output_path = "results/plots/taxonomic_stacked_bar.png"
    plt.savefig(output_path, dpi=300)
    print(f"Stacked bar plot saved to {output_path}")

if __name__ == "__main__":
    main()