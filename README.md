# VCF Report

## Introdução

Olá,

Primeiramente, gostaria de esclarecer que não sou um programador profissional, o que pode ficar evidente ao analisar este repositório. Sou formado em biotecnologia e atuo há algum tempo na área de engenharia metabólica. Sempre tive afinidade com programação e gosto muito de criar soluções. Ao longo da minha trajetória, utilizei Python em diversas situações, o que me levou a ingressar no mestrado em bioinformática na UNICAMP.

Recentemente, me deparei com este desafio e decidi encará-lo. Para um programador ou desenvolvedor web que lida com esse tipo de tarefa regularmente, pode ser algo relativamente simples. Para mim, foi um pouco mais desafiador, pois me falta um conhecimento mais profundo de computação. Já desenvolvi outras aplicações nas empresas em que trabalhei, mas sempre com o suporte de programadores que empacotavam as soluções que eu idealizava.

Dito isso, vamos à apresentação do funcionamento deste aplicativo!

## Instruções de uso

1. Para usar o aplicativo, copie este repositório no seu computador com o comando:

    ```bash
    git clone https://github.com/BatistaB/VCF_report.git
    ```

2. Após isso, recomendo instalar as dependências presentes no arquivo `requirements.txt` usando Python 3.9:

    ```bash
    pip install -r requirements.txt
    ```

3. A próxima etapa é baixar o banco de dados de SNPs para fazer a comparação. Eu utilizei o `common_all_20180418.vcf.gz`. O arquivo precisa ser descompactado na pasta `DATA` (ele possui cerca de 9 GB):

    ```bash
    wget https://ftp.ncbi.nih.gov/snp/organisms/human_9606/VCF/common_all_20180418.vcf.gz
    ```

4. Depois, execute o Snakefile. Certifique-se de estar no diretório principal `/VCF_report`. O processamento leva de 10 a 15 minutos:

    ```bash
    snakemake -c 3
    ```

5. A etapa anterior irá gerar um arquivo CSV com os dados necessários para serem apresentados em uma tabela dinâmica no Flask:

    ```bash
    python app.py
    ```

6. Entre no link local gerado e será possível filtrar os dados por profundidade (DP) e frequência TOPMED.

## Considerações finais

Foi muito interessante desenvolver este desafio, pois identifiquei vários pontos e oportunidades de melhoria, como:

- Aprender Docker e como desenvolver uma aplicação completa;
- Descobrir como trabalhar com grandes bancos de dados: seria melhor usar uma API ou armazenar esses dados de forma mais eficiente, ocupando menos memória?
- Compreender melhor os bancos de dados dbSNP. Passei bastante tempo pensando em como acessá-los diretamente, mas não consegui integrar da maneira que desejava.
- Talvez o apresentado aqui não seja suficiente para o desafio proposto, mas foi legal tetar entregar a solução para este desafio.

Obrigado pelo seu tempo,


Bruno Batista.

