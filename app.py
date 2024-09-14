from flask import Flask, render_template, request
import pandas as pd
import numpy as np


app = Flask(__name__)

# Carregar o arquivo CSV e converter TOPMED para float
df = pd.read_csv('filtered_vcf_df.csv', sep=',')
df['TOPMED'] = df['TOPMED'].apply(lambda x: float(x) if x != '.' else np.nan)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Obter valores únicos para CHROM e VC, adicionando a opção "ALL"
    chrom_options = ['ALL'] + df['CHROM'].unique().tolist()
    vc_options = ['ALL'] + df['VC'].unique().tolist()

    # Obter os valores do formulário
    min_dp = request.form.get('min_dp', type=int, default=0)
    selected_chrom = request.form.get('chrom', 'ALL')
    selected_vc = request.form.get('vc', 'ALL')
    min_topmed = request.form.get('min_topmed', type=float, default=0.0)
    max_topmed = request.form.get('max_topmed', type=float, default=1.0)

    # Obter o valor do checkbox para filtrar N/A
    filter_na = request.form.get('filter_na', type=bool, default=False)

    # Aplicar os filtros
    filtered_df = df[df['DP'] >= min_dp]

    if selected_chrom != 'ALL':
        filtered_df = filtered_df[filtered_df['CHROM'] == selected_chrom]

    if selected_vc != 'ALL':
        filtered_df = filtered_df[filtered_df['VC'] == selected_vc]

    # Filtro para TOPMED
    filtered_df = filtered_df[
        (filtered_df['TOPMED'].isnull()) | 
        ((filtered_df['TOPMED'] >= min_topmed) & (filtered_df['TOPMED'] <= max_topmed))
    ]

    # Aplicar filtro para remover N/A se o checkbox estiver marcado
    if filter_na:
        filtered_df = filtered_df[filtered_df['TOPMED'].notnull()]

    # Converter DataFrame filtrado para HTML com classes CSS
    table_html = filtered_df.to_html(classes='table table-striped table-hover', header=True, index=False)

    return render_template('index.html', table_html=table_html, 
                           min_dp=min_dp, chrom_options=chrom_options, 
                           vc_options=vc_options, selected_chrom=selected_chrom, 
                           selected_vc=selected_vc, min_topmed=min_topmed,
                           max_topmed=max_topmed)

if __name__ == '__main__':
    app.run(debug=True)


#22:07:17 2024 start
#22:15:39 2024