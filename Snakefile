rule all:
    input:
        'filtered_vcf_df.csv'

rule extract_filtered_vcf:
    input:
        vcf_file='data/NIST.vcf',
        full_vcf='data/common_all_20180418.vcf'
    output:
        'filtered_vcf_df.csv'
    shell:
        """
        python process_vcf.py {input.vcf_file} {input.full_vcf} {output}
        """