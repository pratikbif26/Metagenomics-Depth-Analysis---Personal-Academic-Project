Metagenomic-Depth-Analysis
An Automated Snakemake Workflow for Assessing Subsampling Effects on Taxonomic Abundance

📌 Project Overview
How much sequencing is "enough"? This project provides a reproducible framework to answer that question. It automates the process of subsampling large metagenomic datasets to various depths (10% to 100%) to quantify how sequencing effort impacts the detection of species and the stability of community profiles.

🔬 Key Research Questions:
Diversity: How does sequencing depth affect Alpha Diversity (Species Richness)?

Stability: At what depth does the relative abundance of dominant species stabilize?

Efficiency: What is the point of diminishing returns for rare species discovery?

🛠 Tech Stack & Tools
Workflow Management: Snakemake

Taxonomic Profiling: Kraken2 & Bracken

Data Manipulation: seqtk, fastp

Analysis & Visualization: Python (Pandas, Matplotlib, Seaborn)

Environment: Conda / Mamba

🚀 Pipeline Architecture
The pipeline follows a modular "Fan-Out, Fan-In" logic:

Subsample: Stochastic read selection using seqtk.

QC: Quality filtering and adapter trimming via fastp.

Classify: K-mer based taxonomic assignment using Kraken2.

Estimate: Bayesian abundance estimation with Bracken.

Aggregate: Integration of multiple depths into a single master abundance matrix.

Analyze: Generation of Rarefaction and Correlation plots.

📁 Repository Structure
Plaintext

.
├── Snakefile               # Core workflow logic
├── config.yaml             # Global parameters and sample IDs
├── scripts/
│   ├── aggregate.py        # Merges Bracken reports into a TSV
│   ├── plot.py             # Generates Rarefaction/Correlation curves
│   └── stacked_bar.py      # Visualizes taxonomic shifts
├── data/
│   └── raw/                # Place raw .fastq.gz files here
└── results/                # Automatically generated outputs
📈 Example Results
The workflow generates several key visualizations to interpret the sequencing effort:

Rarefaction Curves: Visualizing the saturation of species discovery.

Taxonomic Stacked Bar Plots: Demonstrating the stability of core microbes across depths.

⚙️ Installation & Usage
1. Clone the Repository
Bash

git clone https://github.com/yourusername/Metagenomic-Depth-Analysis.git
cd Metagenomic-Depth-Analysis
2. Set Up Environment
Bash

mamba create -n metagenomics_env snakemake kraken2 bracken seqtk fastp pandas matplotlib seaborn -c bioconda -c conda-forge
conda activate metagenomics_env
3. Run the Pipeline
Bash

# Perform a dry run to verify logic
snakemake -np

# Execute with 4 cores
snakemake --cores 4
🧬 Biological Insight
Using sample SRR1805151 (Human Stool), this analysis revealed that dominant taxa like Bacteroides vulgatus are accurately represented at just 25% depth (Spearman ρ > 0.9), while rare species discovery remains highly sensitive to sequencing saturation, highlighting the need for deep sequencing in pathogen discovery vs. core community profiling.
