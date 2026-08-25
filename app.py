# =============================================================================
# APP: Analisador Interativo de CSV
# Bibliotecas: streamlit (interface web) + pandas (dados) + plotly (gráficos)
# Como rodar: streamlit run app.py
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------
# 1) CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------
# st.set_page_config() ajusta coisas gerais da aba do navegador: o título
# que aparece, o ícone, e se o conteúdo ocupa a tela toda (layout="wide")
# ou fica centralizado e estreito (layout padrão). Precisa ser o PRIMEIRO
# comando do Streamlit no arquivo.
st.set_page_config(page_title="Analisador de CSV", layout="wide")

# st.title() escreve um título grande no topo da página.
st.title("📊 Analisador Interativo de CSV")

# st.write() é o comando "genérico" do Streamlit -- funciona parecido com
# o print() do Python, mas desenha na página web em vez do terminal.
st.write("Envie um arquivo CSV para ver os dados e montar um gráfico interativo.")


# -----------------------------------------------------------------------
# 2) UPLOAD DO ARQUIVO
# -----------------------------------------------------------------------
# st.file_uploader() desenha uma caixinha de "arrastar e soltar" na tela.
# type="csv" restringe para o usuário só poder escolher arquivos .csv.
# O que a função devolve é guardado na variável `arquivo`:
#   - Enquanto ninguém envia nada, `arquivo` vale None.
#   - Depois que o usuário envia um CSV, `arquivo` vira um objeto de
#     arquivo que o pandas consegue ler diretamente.
arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv")

# Esse "if" é o coração do programa: só executamos o resto (mostrar
# tabela, montar gráfico) SE o usuário já tiver enviado um arquivo.
# Antes disso, `arquivo` é None e o "if" não entra.
if arquivo is not None:

    # -------------------------------------------------------------------
    # 3) LER O CSV COM PANDAS
    # -------------------------------------------------------------------
    # pd.read_csv() transforma o arquivo CSV em uma tabela (chamada de
    # "DataFrame" no pandas, guardada aqui na variável `df`). Um DataFrame
    # é como uma planilha do Excel dentro da memória do programa: tem
    # linhas, colunas e cada coluna tem um nome.
    df = pd.read_csv(arquivo)

    # st.success() mostra uma caixinha verde de confirmação -- só
    # feedback visual para o usuário saber que deu certo.
    st.success(f"Arquivo carregado com sucesso! {df.shape[0]} linhas e {df.shape[1]} colunas.")

    # -------------------------------------------------------------------
    # 4) MOSTRAR UMA PRÉVIA DA TABELA
    # -------------------------------------------------------------------
    st.subheader("Prévia dos dados")

    # st.dataframe() desenha a tabela na tela, de forma interativa: o
    # usuário pode rolar, ordenar clicando no cabeçalho da coluna, e até
    # redimensionar colunas -- tudo isso "de graça", sem você programar
    # nada disso manualmente.
    st.dataframe(df, use_container_width=True)

    # -------------------------------------------------------------------
    # 5) BARRA LATERAL: ESCOLHER AS COLUNAS DO GRÁFICO
    # -------------------------------------------------------------------
    # st.sidebar cria uma barra lateral fixa à esquerda da tela. Tudo que
    # você desenha usando "st.sidebar.algumacoisa()" aparece lá, em vez de
    # aparecer no corpo principal da página.
    st.sidebar.header("Configurações do Gráfico")

    # df.columns é a lista com os nomes de todas as colunas do CSV que foi
    # carregado. Convertendo para list(), conseguimos passar essa lista
    # para o menu suspenso (selectbox) escolher entre elas.
    colunas = list(df.columns)

    # st.sidebar.selectbox() desenha um menu suspenso na barra lateral.
    # O primeiro argumento é o texto do rótulo; o segundo é a lista de
    # opções. O valor escolhido pelo usuário fica guardado na variável.
    eixo_x = st.sidebar.selectbox("Escolha a coluna do eixo X", colunas)
    eixo_y = st.sidebar.selectbox("Escolha a coluna do eixo Y", colunas)

    # Também deixamos o usuário escolher o TIPO de gráfico, para o app
    # ficar mais flexível (funciona tanto para dados numéricos quanto
    # para comparar categorias).
    tipo_grafico = st.sidebar.selectbox(
        "Tipo de gráfico",
        ["Dispersão (pontos)", "Linha", "Barras"]
    )

    # -------------------------------------------------------------------
    # 6) MONTAR O GRÁFICO COM PLOTLY EXPRESS
    # -------------------------------------------------------------------
    # plotly.express (importado como "px") é a forma mais simples de criar
    # gráficos com o Plotly: cada tipo de gráfico é uma função (px.scatter,
    # px.line, px.bar...) que recebe o DataFrame e os nomes das colunas
    # que devem ir em cada eixo.
    #
    # A diferença do Plotly para um gráfico "estático" (como o do Excel
    # exportado como imagem) é que o gráfico gerado aqui já nasce
    # interativo: passar o mouse mostra os valores exatos (tooltip),
    # dá pra arrastar para dar zoom, clicar e arrastar para navegar, e
    # até esconder uma categoria clicando na legenda.
    if tipo_grafico == "Dispersão (pontos)":
        fig = px.scatter(df, x=eixo_x, y=eixo_y, title=f"{eixo_y} por {eixo_x}")
    elif tipo_grafico == "Linha":
        fig = px.line(df, x=eixo_x, y=eixo_y, title=f"{eixo_y} por {eixo_x}")
    else:  # "Barras"
        fig = px.bar(df, x=eixo_x, y=eixo_y, title=f"{eixo_y} por {eixo_x}")

    # -------------------------------------------------------------------
    # 7) MOSTRAR O GRÁFICO NA TELA
    # -------------------------------------------------------------------
    st.subheader("Gráfico Interativo")

    # st.plotly_chart() é a "ponte" entre o Plotly e o Streamlit: ele pega
    # a figura (`fig`) que o Plotly montou e desenha ela na página web,
    # já com todos os recursos interativos (zoom, hover, pan) funcionando
    # automaticamente -- sem precisar escrever nenhuma linha de HTML ou
    # JavaScript.
    # use_container_width=True faz o gráfico esticar e ocupar toda a
    # largura disponível na tela, em vez de ficar pequeno e fixo.
    st.plotly_chart(fig, use_container_width=True)

else:
    # Esse "else" só aparece enquanto ninguém enviou um arquivo ainda --
    # é uma mensagem de orientação para o usuário.
    st.info("⬆️ Envie um arquivo CSV acima para começar.")
