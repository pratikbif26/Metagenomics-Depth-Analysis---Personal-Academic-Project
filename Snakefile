import os

# 1. Load configuration
configfile: "config.yaml"

SAMPLES = config["SAMPLES"]
FRACTIONS = config["FRACTIONS"]

# 2. Final Target Rule
rule all:
    input:
        # Final Bracken reports for every fraction
        expand("results/bracken/{sample}_{fraction}.species.bracken", 
               sample=SAMPLES, fraction=FRACTIONS),
        # Final analysis plots
        "results/plots/alpha_diversity.png",
        "results/plots/abundance_correlation.png"


# 3. Rule: Subsample Reads
rule subsample:
    input:
        r1 = os.path.join(config["RAW_DATA_DIR"], "{sample}_R1.fastq.gz"),
        r2 = os.path.join(config["RAW_DATA_DIR"], "{sample}_R2.fastq.gz")
    output:
        r1 = "results/subsampled/{sample}_{fraction}_R1.fq.gz",
        r2 = "results/subsampled/{sample}_{fraction}_R2.fq.gz"
    params:
        fraction = "{fraction}",
        seed = config["SEED"]
    shell:
        """
        if [ "{params.fraction}" = "1.00" ]; then
            cp {input.r1} {output.r1}
            cp {input.r2} {output.r2}
        else
            seqtk sample -s {params.seed} {input.r1} {params.fraction} | gzip > {output.r1}
            seqtk sample -s {params.seed} {input.r2} {params.fraction} | gzip > {output.r2}
        fi
        """

# 4. Rule: Quality Control
rule fastp_qc:
    input:
        r1 = "results/subsampled/{sample}_{fraction}_R1.fq.gz",
        r2 = "results/subsampled/{sample}_{fraction}_R2.fq.gz"
    output:
        r1 = "results/qc/{sample}_{fraction}_R1.clean.fq.gz",
        r2 = "results/qc/{sample}_{fraction}_R2.clean.fq.gz",
        html = "results/qc/reports/{sample}_{fraction}.html"
    threads: 4
    shell:
        "fastp -i {input.r1} -I {input.r2} -o {output.r1} -O {output.r2} -h {output.html} -w {threads}"

# 5. Rule: Taxonomic Classification
rule kraken2:
    input:
        r1 = "results/qc/{sample}_{fraction}_R1.clean.fq.gz",
        r2 = "results/qc/{sample}_{fraction}_R2.clean.fq.gz"
    output:
        report = "results/kraken2/{sample}_{fraction}.kreport"
    params:
        db = config["KRAKEN_DB"]
    threads: 8
    shell:
        """
        kraken2 --db {params.db} --paired --threads {threads} \
                --report {output.report} {input.r1} {input.r2} > /dev/null
        """

# 6. Rule: Abundance Estimation
rule bracken:
    input:
        report = "results/kraken2/{sample}_{fraction}.kreport"
    output:
        species = "results/bracken/{sample}_{fraction}.species.bracken"
    params:
        db = config["KRAKEN_DB"],
        level = config["TAX_LEVEL"]
    shell:
        "bracken -d {params.db} -i {input.report} -o {output.species} -l {params.level}"

# 7. Rule: Aggregate Results
rule aggregate_results:
    input:
        expand("results/bracken/{sample}_{fraction}.species.bracken", 
               sample=SAMPLES, fraction=FRACTIONS)
    output:
        "results/analysis/master_abundance_table.tsv"
    shell:
        "python scripts/aggregate.py -o {output} {input}"

# 8. Rule: Visualization
rule plot_results:
    input:
        "results/analysis/master_abundance_table.tsv"
    output:
        "results/plots/alpha_diversity.png",
        "results/plots/abundance_correlation.png"
    shell:

        "python scripts/plot.py -i {input} -o results/plots/"
