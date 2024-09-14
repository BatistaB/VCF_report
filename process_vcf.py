import pandas as pd
import sys
import numpy as np


def extract_topmed(info):
    if 'TOPMED=' in info:
        return info.split('TOPMED=')[1].split(';')[0]
    else:
        return 0


def extract_geneinfo(info):
    if 'GENEINFO=' in info:
        return info.split('GENEINFO=')[1].split(';')[0]
    else:
        return 0


def extract_vc(info):
    if 'VC=' in info:
        return info.split('VC=')[1].split(';')[0]
    else:
        return 0


def extract_dp(info):
    if 'DP=' in info:
        return info.split('DP=')[1].split(';')[0]
    else:
        return None


def process_vcf_with_filter(vcf_file, ids_from_vcf, chunk_size=50000):
    filtered_data = []
    with open(vcf_file, 'r', encoding='utf-8') as f:
        for l in f:
            if not l.startswith('#'):
                columns = l.strip().split('\t')
                if columns[2] in ids_from_vcf:
                    filtered_data.append(columns)
            if len(filtered_data) >= chunk_size:
                vcf_filtered_df = pd.DataFrame(filtered_data, columns=[
                    "CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"])
                filtered_data = []
        if filtered_data:
            vcf_filtered_df = pd.DataFrame(filtered_data, columns=[
                "CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"])
    return vcf_filtered_df


def main(vcf_file, full_vcf, output_file):
    # Abrir o arquivo e localizar a linha do cabeçalho
    with open(vcf_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if line.startswith('#CHROM'):
                header_line = i
                break

    # Ler o arquivo a partir da linha do cabeçalho
    vcf_df = pd.read_csv(vcf_file, sep='\t', skiprows=header_line)

    # Filtrar apenas os PASS e aqueles que possuem ID
    vcf_df = vcf_df.loc[vcf_df.FILTER == 'PASS']
    vcf_df = vcf_df[vcf_df.ID != '.']

    # Pegando todos os IDs do vcf
    ids_from_vcf = set(vcf_df.ID.tolist())

    # Processar o arquivo VCF com os IDs filtrados
    filtered_vcf_df = process_vcf_with_filter(
        full_vcf, ids_from_vcf, chunk_size=50000)

    # Aplicar as funções na coluna INFO
    filtered_vcf_df['TOPMED'] = filtered_vcf_df['INFO'].apply(
        lambda x: extract_topmed(x))
    filtered_vcf_df['GENEINFO'] = filtered_vcf_df['INFO'].apply(
        lambda x: extract_geneinfo(x))
    filtered_vcf_df['VC'] = filtered_vcf_df['INFO'].apply(
        lambda x: extract_vc(x))

    # Remover as colunas QUAL, FILTER e INFO
    filtered_vcf_df = filtered_vcf_df.drop(columns=['QUAL', 'FILTER', 'INFO'])

    # Aplicar a função para extrair DP
    vcf_df['DP'] = vcf_df['INFO'].apply(lambda x: extract_dp(x))

    # Merging dos DataFrames
    filtered_vcf_df = filtered_vcf_df.merge(
        vcf_df[['ID', 'DP']], on='ID', how='left')

    def format_topmed(topmed_str):
        if pd.isnull(topmed_str):
            return ""
        topmed_str = str(topmed_str)
        topmed_list = topmed_str.split(',')
        formatted_list = [s[0:4] for s in topmed_list]
        return ','.join(formatted_list)

    
    
    freq_data = {}

    for a, b, c, d in zip(filtered_vcf_df['ID'], filtered_vcf_df['REF'], filtered_vcf_df['ALT'], filtered_vcf_df['TOPMED']):

        bases = b
        c = c.split(',')

        for e in c:
            bases = bases + ' ' + e

        bases = bases.split()
        k = d.split(',')

        TOPMED_freq_dic = {}

        for base, freq in zip(bases, k):
            TOPMED_freq_dic[base] = freq

        freq_data[a] = TOPMED_freq_dic

    # dentro do meu dicionario o PRIMEIRO é o REF e depois são os ALT
    # Definindo a função para atualizar a coluna TOPMED

    def update_topmed(row, freq_data):
        id = row['ID']
        alt = row['ALT']

        try:
            # Tenta acessar o valor correspondente
            freq = freq_data[id][alt]
        except KeyError:
            # Caso não encontre a chave, define um valor padrão
            freq = '.'

        # Retorna o valor formatado
        return freq

    # Aplicar a função para atualizar a coluna TOPMED com base na FREQ ALT do NIST
    filtered_vcf_df['TOPMED'] = filtered_vcf_df.apply(
        lambda row: update_topmed(row, freq_data), axis=1)

    # Função para converter os valores

    def convert_to_float(value):
        return float(value) if value != '.' else np.nan

    # Aplicando a conversão à coluna TOPMED
    filtered_vcf_df['TOPMED'] = filtered_vcf_df['TOPMED'].apply(
        convert_to_float)

    # Função para extrair os símbolos dos genes da coluna GENEINFO
    def extract_symbols(geneinfo):
        symbols = []
        geneinfo = str(geneinfo)
        # Separando por '|' quando houver mais de um gene
        for gene in geneinfo.split('|'):
            symbol = gene.split(':')[0]  # Pegando o símbolo antes de ':'
            symbols.append(symbol)
        return symbols

    # Aplicar a função na coluna GENEINFO para extrair os símbolos
    filtered_vcf_df['GENES'] = filtered_vcf_df['GENEINFO'].apply(
        extract_symbols)

    # Função para buscar o nome correspondente ao símbolo no df_genes
    def get_gene_names(symbols):
        names = []
        for symbol in symbols:
            # Procurar o nome no df_genes usando o símbolo
            name = df_genes[df_genes['Symbol'] == symbol]['Name'].values
            if len(name) > 0:
                names.append(name[0])  # Adicionar o nome correspondente
            else:
                # Caso o símbolo não seja encontrado, adicionar 'NaN'
                names.append('NaN')
        # Retornar nomes separados por '|', se houver mais de um
        return '|'.join(names)

    # Leia o arquivo ncbi_human_sapiens_genes.tsv em um DataFrame
    df_genes = pd.read_csv('data/ncbi_human_sapiens_genes.tsv', sep='\t')

    # Aplicar a função para obter os nomes e criar a nova coluna 'Gene Names'
    filtered_vcf_df['GENE NAMES'] = filtered_vcf_df['GENES'].apply(
        get_gene_names)

    # Excluir a coluna GENEINFO para melhor formatação.
    filtered_vcf_df.drop(columns=['GENEINFO'], inplace=True)

    # Salvar o DataFrame final
    filtered_vcf_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
