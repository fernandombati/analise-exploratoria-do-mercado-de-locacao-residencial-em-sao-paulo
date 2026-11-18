from pathlib import Path

import pandas as pd
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
ARQUIVO_BASE = ROOT / "quinto_andar_transformed_data.csv"
ARQUIVO_SAIDA = ROOT / "Apresentacao_Projeto_Integrador_Sprint4_Tarefas_14a18.pptx"

BG = RGBColor(18, 22, 28)
CARD = RGBColor(26, 33, 45)
CARD_ALT = RGBColor(31, 41, 55)
TEXT = RGBColor(243, 244, 246)
MUTED = RGBColor(156, 163, 175)
CYAN = RGBColor(56, 189, 248)
GREEN = RGBColor(52, 211, 153)
AMBER = RGBColor(251, 191, 36)
ROSE = RGBColor(251, 113, 133)
WHITE = RGBColor(255, 255, 255)


def carregar_metricas():
    df = pd.read_csv(ARQUIVO_BASE, encoding="utf-8-sig")
    ids = df["url"].astype(str).str.extract(r"imovel/(\d+)")[0]
    df["id_imovel"] = ids.fillna(pd.Series(df.index.astype(str), index=df.index))
    recebidos = len(df)
    df = df.drop_duplicates(subset=["id_imovel"])
    unicos = len(df)
    df = df[df["metragem"].between(12, 800) & df["aluguel"].between(500, 50000)].copy()
    df["preco_m2"] = df["aluguel"] / df["metragem"]
    df["custo_total"] = df["aluguel"] + df["condominio"] + df["iptu"]

    por_bairro = df.groupby("bairro").size().sort_values(ascending=False)
    por_quartos = (
        df[df["quarto"].between(1, 4)]
        .groupby("quarto")["aluguel"]
        .median()
        .sort_index()
    )
    return {
        "recebidos": recebidos,
        "unicos": unicos,
        "duplicados": recebidos - unicos,
        "validos": len(df),
        "bairros": df["bairro"].nunique(),
        "aluguel_mediano": df["aluguel"].median(),
        "custo_mediano": df["custo_total"].median(),
        "area_mediana": df["metragem"].median(),
        "preco_m2_mediano": df["preco_m2"].median(),
        "pet_pct": df["aceita_pet"].mean() * 100,
        "mobilia_pct": df["mobilia"].mean() * 100,
        "por_bairro": por_bairro.head(5).to_dict(),
        "por_quartos": por_quartos.to_dict(),
    }


def moeda(valor):
    return f"R$ {valor:,.0f}".replace(",", ".")


def moeda_com_centavos(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def numero(valor):
    return f"{valor:,.0f}".replace(",", ".")


def adicionar_caixa(slide, x, y, w, h, cor=CARD, arredondado=True):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if arredondado else MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = cor
    shape.line.fill.background()
    return shape


def adicionar_texto(
    slide,
    texto,
    x,
    y,
    w,
    h,
    tamanho=16,
    cor=TEXT,
    negrito=False,
    alinhamento=PP_ALIGN.LEFT,
    vertical=MSO_ANCHOR.TOP,
):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = vertical
    p = tf.paragraphs[0]
    p.text = texto
    p.alignment = alinhamento
    p.font.name = "Aptos"
    p.font.size = Pt(tamanho)
    p.font.bold = negrito
    p.font.color.rgb = cor
    return box


def adicionar_lista(slide, itens, x, y, w, h, tamanho=16, espacamento=10):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.03)
    for i, item in enumerate(itens):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {item}"
        p.space_after = Pt(espacamento)
        p.font.name = "Aptos"
        p.font.size = Pt(tamanho)
        p.font.color.rgb = TEXT
    return box


def nova_pagina(prs, numero_slide, topico, titulo, subtitulo=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG
    adicionar_texto(
        slide,
        topico.upper(),
        0.65,
        0.28,
        12.0,
        0.35,
        tamanho=11,
        cor=CYAN,
        negrito=True,
    )
    adicionar_texto(slide, titulo, 0.65, 0.72, 12.0, 0.58, tamanho=26, negrito=True)
    if subtitulo:
        adicionar_texto(slide, subtitulo, 0.68, 1.31, 11.9, 0.45, tamanho=12, cor=MUTED)
    adicionar_texto(
        slide,
        f"Projeto Integrador • FATEC SEBRAE                                      {numero_slide:02d}",
        0.68,
        7.12,
        12.0,
        0.2,
        tamanho=9,
        cor=MUTED,
    )
    return slide


def adicionar_kpi(slide, x, y, w, rotulo, valor, detalhe, cor=CYAN):
    adicionar_caixa(slide, x, y, w, 1.42)
    adicionar_texto(slide, rotulo.upper(), x + 0.2, y + 0.16, w - 0.4, 0.24, 10, MUTED, True)
    adicionar_texto(slide, valor, x + 0.2, y + 0.48, w - 0.4, 0.45, 25, cor, True)
    adicionar_texto(slide, detalhe, x + 0.2, y + 1.03, w - 0.4, 0.25, 10, MUTED)


def adicionar_barra(slide, x, y, w, label, value, max_value, suffix="", cor=CYAN):
    adicionar_texto(slide, label, x, y, w * 0.45, 0.27, 12, TEXT, True)
    adicionar_texto(
        slide,
        f"{moeda(value) if suffix == 'R$' else numero(value)}{suffix if suffix != 'R$' else ''}",
        x + w * 0.72,
        y,
        w * 0.28,
        0.27,
        12,
        TEXT,
        True,
        PP_ALIGN.RIGHT,
    )
    adicionar_caixa(slide, x, y + 0.36, w, 0.15, CARD_ALT)
    preenchimento = max(0.03, w * value / max_value) if max_value else 0.03
    adicionar_caixa(slide, x, y + 0.36, min(preenchimento, w), 0.15, cor)


def gerar():
    m = carregar_metricas()
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # Capa
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG
    adicionar_caixa(slide, 0, 0, 0.16, 7.5, CYAN, False)
    adicionar_texto(slide, "SPRINT 4 + FINAL  •  TAREFAS 14–18", 0.9, 0.75, 11.5, 0.35, 13, CYAN, True)
    adicionar_texto(slide, "PROJETO INTEGRADOR  •  ANÁLISE DE DADOS", 0.9, 1.35, 11.5, 0.35, 13, CYAN, True)
    adicionar_texto(slide, "Sprint 4 | Revisão final", 0.9, 2.0, 11.5, 0.85, 34, TEXT, True)
    adicionar_texto(
        slide,
        "Análise imobiliária QuintoAndar: resultados, entrega e retrospectiva",
        0.95,
        3.0,
        11.2,
        0.7,
        20,
        MUTED,
    )
    adicionar_caixa(slide, 0.95, 4.25, 11.3, 1.18, CARD)
    adicionar_texto(
        slide,
        "Fernando Aparecido de Assis  •  FATEC SEBRAE\nProf. Rômulo F. S. Maia  •  2026",
        1.2,
        4.53,
        10.8,
        0.65,
        15,
        TEXT,
    )
    adicionar_texto(slide, "Apresentação de revisão e entrega", 0.95, 6.85, 8, 0.3, 11, MUTED)

    # Destaque para as tarefas 14 a 18
    slide = nova_pagina(prs, 2, "SPRINT 4 • TAREFAS 14–18 — VISÃO GERAL", "Roteiro de revisão e encerramento")
    tarefas = [
        ("14", "Revisão Google Forms, entrega e retrospectiva (erros + backlog)", CYAN),
        ("15", "Aplicação do instrumento de pesquisa", GREEN),
        ("16", "Planejamento, Product Backlog e análise dos resultados", AMBER),
        ("17", "Preparação do relatório final", ROSE),
        ("18", "Revisão final, entrega e retrospectiva: erros e itens faltantes", CYAN),
    ]
    for i, (numero_tarefa, descricao, cor) in enumerate(tarefas):
        y = 1.82 + i * 0.9
        adicionar_caixa(slide, 0.82, y, 11.62, 0.72, CARD if i % 2 == 0 else CARD_ALT)
        adicionar_texto(slide, numero_tarefa, 1.05, y + 0.13, 0.8, 0.4, 20, cor, True)
        adicionar_texto(slide, descricao, 2.0, y + 0.16, 9.95, 0.38, 15, TEXT, True)
    adicionar_texto(
        slide,
        "Objetivo: transformar a análise de anúncios do QuintoAndar em evidências, recomendações de negócio e uma entrega acadêmica rastreável.",
        0.98,
        6.48,
        11.35,
        0.38,
        12,
        MUTED,
    )

    # Revisão da Sprint 4: evidência Google Forms
    slide = nova_pagina(prs, 3, "SPRINT 4 • TAREFA 14 — REVISÃO / GOOGLE FORMS", "Revisão da Sprint: resultados do Google Forms")
    adicionar_caixa(slide, 0.82, 1.86, 5.6, 4.55)
    adicionar_texto(slide, "Evidência localizada no projeto", 1.12, 2.16, 4.95, 0.4, 18, AMBER, True)
    adicionar_texto(
        slide,
        "Não há exportação, planilha de respostas ou resumo do Google Forms entre os arquivos disponíveis na pasta do projeto.",
        1.12,
        2.82,
        4.9,
        1.15,
        16,
        TEXT,
    )
    adicionar_texto(
        slide,
        "Para apresentar resultados reais: inserir número de respostas válidas, período da coleta, perfil agregado e principais respostas por pergunta.",
        1.12,
        4.25,
        4.9,
        1.15,
        13,
        MUTED,
    )
    adicionar_caixa(slide, 6.78, 1.86, 5.56, 4.55)
    adicionar_texto(slide, "Não confundir as duas fontes", 7.08, 2.16, 4.95, 0.4, 18, CYAN, True)
    adicionar_lista(
        slide,
        [
            "Google Forms: pesquisa com participantes; precisa da exportação original para calcular resultados.",
            "API do QuintoAndar / CSV: anúncios imobiliários; informa preços, área, bairro e comodidades.",
            "Os indicadores dos próximos slides descrevem a oferta anunciada, não opiniões ou preferências declaradas por usuários.",
        ],
        7.08,
        2.82,
        4.95,
        2.7,
        14,
        12,
    )
    adicionar_texto(
        slide,
        "A pesquisa pode validar estas oportunidades, mas seus resultados não devem ser substituídos pelos dados de anúncios.",
        0.98,
        6.56,
        11.35,
        0.34,
        12,
        AMBER,
        True,
    )

    # Evidências e fonte de dados do algoritmo
    slide = nova_pagina(
        prs,
        4,
        "SPRINT 4 • TAREFA 15 — APLICAÇÃO DO INSTRUMENTO / COLETA VIA API",
        "Fonte primária: API do próprio QuintoAndar",
        "O dashboard tenta consultar a API; o CSV local entra automaticamente como fallback se a coleta online não retornar dados.",
    )
    adicionar_caixa(slide, 0.78, 1.92, 5.65, 4.15)
    adicionar_texto(slide, "API de busca do QuintoAndar", 1.08, 2.2, 5.0, 0.4, 18, CYAN, True)
    adicionar_texto(
        slide,
        "Endpoint usado no Quintoandar.py:\n"
        "quintoandar.com.br/api/yellow-pages/v2/search\n\n"
        "Requisições POST por quadrantes geográficos de São Paulo; até 7 quadrantes × 4 páginas, página de 40 itens e 10 workers concorrentes.",
        1.08,
        2.82,
        5.0,
        1.85,
        14,
        TEXT,
    )
    adicionar_texto(
        slide,
        "Campos: preço do aluguel, condomínio, IPTU, área, quartos, bairro, URL, aceitação de pets e mobília.",
        1.08,
        5.05,
        5.0,
        0.65,
        12,
        MUTED,
    )
    adicionar_caixa(slide, 6.78, 1.92, 5.57, 4.15)
    adicionar_texto(slide, "Evidências do CSV (fallback)", 7.08, 2.2, 4.95, 0.4, 18, GREEN, True)
    adicionar_lista(
        slide,
        [
            f"Arquivo: quinto_andar_transformed_data.csv ({numero(m['recebidos'])} registros).",
            f"{numero(m['validos'])} anúncios válidos; {numero(m['duplicados'])} duplicatas removidas; {numero(m['bairros'])} bairros.",
            f"Aluguel mediano: {moeda(m['aluguel_mediano'])}/mês; custo total mediano: {moeda_com_centavos(m['custo_mediano'])}.",
            f"Área mediana: {m['area_mediana']:.0f} m²; aceitam pets: {m['pet_pct']:.1f}%; mobiliados: {m['mobilia_pct']:.1f}%.",
            "Snapshot local de contingência; números podem diferir da consulta online atual.",
        ],
        7.08,
        2.82,
        4.95,
        2.85,
        12,
        7,
    )
    adicionar_texto(
        slide,
        "O arquivo de fallback contém anúncios imobiliários; ele não é a base de respostas do Google Forms.",
        0.98,
        6.38,
        11.35,
        0.4,
        12,
        AMBER,
        True,
    )

    # Planejamento e backlog
    slide = nova_pagina(prs, 5, "SPRINT 4 • TAREFA 16 — PLANEJAMENTO / PRODUCT BACKLOG", "Planejamento da Sprint e Product Backlog")
    headers = [("Etapa", 0.9, 2.1), ("Atividade / entrega", 3.15, 5.5), ("Evidência esperada", 8.95, 3.3)]
    for texto, x, w in headers:
        adicionar_texto(slide, texto.upper(), x, 1.82, w, 0.3, 10, CYAN, True)
    linhas = [
        ("15 • Sprint 4", "Aplicação do instrumento de pesquisa", "Formulário e respostas exportadas"),
        ("16 • Sprint 4", "Planejamento, Product Backlog e análise", "Achados e prioridades documentados"),
        ("17 • Sprint 4", "Preparação do relatório final", "Método, resultados e limitações"),
        ("18 • Sprint 4 / Final", "Revisão, entrega e retrospectiva/backlog", "PPTX, relatório e itens faltantes"),
    ]
    for i, (etapa, atividade, evidencia) in enumerate(linhas):
        y = 2.22 + i * 0.94
        adicionar_caixa(slide, 0.75, y, 11.85, 0.78, CARD if i % 2 == 0 else CARD_ALT)
        adicionar_texto(slide, etapa, 0.95, y + 0.19, 2.0, 0.35, 12, GREEN, True)
        adicionar_texto(slide, atividade, 3.15, y + 0.15, 5.5, 0.48, 13, TEXT, True)
        adicionar_texto(slide, evidencia, 8.95, y + 0.15, 3.3, 0.48, 11, MUTED)
    adicionar_texto(
        slide,
        "Critério de aceite: cada item deve ter responsável, evidência de conclusão e vínculo com a entrega final.",
        0.95,
        6.3,
        11.5,
        0.42,
        12,
        AMBER,
        True,
    )

    # Algoritmo
    slide = nova_pagina(prs, 6, "SPRINT 4 • TAREFAS 15–16 — COLETA E MÉTODO", "Algoritmo e fluxo de análise", "Pipeline implementado no dashboard Python / Streamlit.")
    etapas = [
        ("01", "Captura", "API de busca por quadrantes; até 7 regiões × 4 páginas, com 10 workers."),
        ("02", "Fallback", "Se a API não retorna dados, carrega a base CSV local."),
        ("03", "Qualidade", "Deduplica pelo ID; filtra área de 12–800 m² e aluguel de R$ 500–50.000."),
        ("04", "Indicadores", "Calcula preço/m² e custo total; usa medianas para reduzir efeito de extremos."),
    ]
    for i, (n, nome, desc) in enumerate(etapas):
        x = 0.78 + (i % 2) * 6.0
        y = 1.95 + (i // 2) * 2.15
        adicionar_caixa(slide, x, y, 5.65, 1.72)
        adicionar_texto(slide, n, x + 0.22, y + 0.22, 0.6, 0.42, 21, CYAN, True)
        adicionar_texto(slide, nome, x + 0.95, y + 0.22, 4.3, 0.4, 18, TEXT, True)
        adicionar_texto(slide, desc, x + 0.95, y + 0.75, 4.3, 0.72, 12, MUTED)
    adicionar_texto(
        slide,
        "Limite importante: captura pontual de anúncios públicos não mede vacância, conversão, demanda efetiva ou evolução histórica.",
        0.95,
        6.48,
        11.4,
        0.38,
        12,
        AMBER,
        True,
    )

    # Resultados da base
    slide = nova_pagina(
        prs,
        7,
        "SPRINT 4 • TAREFA 16 — ANÁLISE DOS RESULTADOS",
        "Leitura do snapshot CSV de contingência",
        "Estatísticas reproduzidas do arquivo local; a resposta da API online pode variar conforme disponibilidade e momento da consulta.",
    )
    adicionar_kpi(slide, 0.78, 1.95, 2.75, "Registros no CSV", numero(m["recebidos"]), "antes da limpeza")
    adicionar_kpi(slide, 3.72, 1.95, 2.75, "Anúncios válidos", numero(m["validos"]), "após deduplicação e filtros", GREEN)
    adicionar_kpi(slide, 6.66, 1.95, 2.75, "Aluguel mediano", moeda(m["aluguel_mediano"]), "por mês", CYAN)
    adicionar_kpi(slide, 9.6, 1.95, 2.75, "Bairros", numero(m["bairros"]), "com anúncios na amostra", AMBER)
    adicionar_caixa(slide, 0.78, 3.75, 11.57, 2.4)
    adicionar_texto(slide, "Leitura rápida", 1.08, 4.02, 4.7, 0.4, 19, CYAN, True)
    adicionar_lista(
        slide,
        [
            f"{numero(m['duplicados'])} registros repetidos removidos pelo ID do imóvel.",
            f"Área mediana de {m['area_mediana']:.0f} m²; custo mensal mediano estimado (aluguel + condomínio + IPTU) de {moeda(m['custo_mediano'])}.",
            f"Mediana de preço por área: {moeda(m['preco_m2_mediano'])}/m²; {m['pet_pct']:.1f}% aceitam pets e {m['mobilia_pct']:.1f}% estão mobiliados.",
        ],
        1.08,
        4.58,
        10.8,
        1.38,
        13,
        8,
    )
    adicionar_texto(slide, "Fonte destes números: quinto_andar_transformed_data.csv, usado como snapshot de fallback.", 0.95, 6.45, 11.5, 0.32, 10, MUTED)

    # Análises por tipologia e bairro
    slide = nova_pagina(prs, 8, "SPRINT 4 • TAREFA 16 — ANÁLISE DE MERCADO", "Padrões por tipologia e região")
    adicionar_caixa(slide, 0.78, 1.87, 5.7, 4.85)
    adicionar_texto(slide, "Aluguel mediano por dormitórios", 1.08, 2.15, 5.0, 0.42, 17, TEXT, True)
    max_rent = max(m["por_quartos"].values())
    for i, (quartos, valor) in enumerate(m["por_quartos"].items()):
        adicionar_barra(
            slide,
            1.1,
            2.85 + i * 0.78,
            4.95,
            f"{int(quartos)} quarto{'s' if quartos > 1 else ''}",
            valor,
            max_rent,
            "R$",
            CYAN if i < 2 else GREEN,
        )
    adicionar_caixa(slide, 6.78, 1.87, 5.55, 4.85)
    adicionar_texto(slide, "Maior volume de anúncios", 7.08, 2.15, 4.9, 0.42, 17, TEXT, True)
    max_count = max(m["por_bairro"].values())
    for i, (bairro, valor) in enumerate(m["por_bairro"].items()):
        adicionar_barra(
            slide,
            7.1,
            2.85 + i * 0.68,
            4.85,
            bairro,
            valor,
            max_count,
            "",
            GREEN if i == 0 else CYAN,
        )
    adicionar_texto(
        slide,
        "Interpretação: maior aluguel mediano em tipologias com mais quartos; maior volume observado em Consolação e Jardim Paulista. Oferta anunciada não equivale a demanda ou liquidez.",
        0.95,
        6.48,
        11.4,
        0.38,
        11,
        AMBER,
        True,
    )

    # Oportunidades de negócio
    slide = nova_pagina(prs, 9, "SPRINT 4 • TAREFA 16 — RESULTADOS / NOVOS NEGÓCIOS", "Oportunidades a validar no mercado")
    recomendacoes = [
        ("Moradia mobiliada", f"Somente {m['mobilia_pct']:.1f}% do snapshot está mobiliado: testar parceria de mobília modular e pacote de locação pronta.", CYAN),
        ("Serviços pet-friendly", f"{m['pet_pct']:.1f}% dos anúncios aceitam pets: explorar busca especializada e parcerias com serviços para tutores.", GREEN),
        ("Inteligência para proprietários", "Oferecer relatório pago de comparação por bairro, tipologia e custo total; validar disposição a pagar antes de escalar.", AMBER),
        ("Preço e ocupação", "Pilotar recomendações de preço apenas após coletar histórico de preço e dias anunciado; a base atual não mede vacância.", ROSE),
    ]
    for i, (titulo, desc, cor) in enumerate(recomendacoes):
        y = 1.92 + i * 1.12
        adicionar_caixa(slide, 0.82, y, 11.65, 0.93)
        adicionar_caixa(slide, 0.82, y, 0.12, 0.93, cor, False)
        adicionar_texto(slide, titulo, 1.15, y + 0.16, 3.2, 0.35, 15, cor, True)
        adicionar_texto(slide, desc, 4.25, y + 0.14, 7.7, 0.6, 13, TEXT)
    adicionar_texto(
        slide,
        "Hipóteses de negócio derivadas dos anúncios; entrevistar usuários e proprietários (Google Forms/entrevistas) antes de assumir demanda.",
        0.95,
        6.48,
        11.4,
        0.38,
        11,
        AMBER,
        True,
    )

    # ODS
    slide = nova_pagina(prs, 10, "SPRINT 4 • TAREFA 16 — ANÁLISE / ODS", "Contribuições possíveis aos Objetivos de Desenvolvimento Sustentável")
    ods = [
        ("ODS 11", "Cidades e comunidades sustentáveis", "Comparar custos e oferta por região pode apoiar decisões de moradia e planejamento. A análise não mede acesso habitacional diretamente.", CYAN),
        ("ODS 8", "Trabalho decente e crescimento econômico", "Dados e automação podem apoiar inovação em serviços imobiliários e novos negócios, com validação de viabilidade e qualidade do trabalho.", GREEN),
        ("ODS 12", "Consumo e produção responsáveis", "Reaproveitar imóveis existentes e facilitar sua ocupação é uma oportunidade; o impacto ambiental precisa ser medido antes de ser afirmado.", AMBER),
    ]
    for i, (sigla, nome, descricao, cor) in enumerate(ods):
        x = 0.82 + i * 4.0
        adicionar_caixa(slide, x, 2.0, 3.7, 3.95)
        adicionar_texto(slide, sigla, x + 0.25, 2.35, 3.2, 0.55, 25, cor, True)
        adicionar_texto(slide, nome, x + 0.25, 3.1, 3.2, 0.8, 17, TEXT, True)
        adicionar_texto(slide, descricao, x + 0.25, 4.15, 3.15, 1.35, 13, MUTED)
    adicionar_texto(
        slide,
        "Alinhamento potencial: apresentar como contribuição pretendida, não como impacto comprovado pelo conjunto de dados.",
        0.95,
        6.38,
        11.4,
        0.4,
        12,
        AMBER,
        True,
    )

    # Relatório final e entrega
    slide = nova_pagina(prs, 11, "SPRINT 4 • TAREFAS 17–18 — RELATÓRIO / ENTREGA", "Preparação do relatório final e entrega")
    adicionar_caixa(slide, 0.8, 1.9, 5.65, 2.95)
    adicionar_texto(slide, "Estrutura recomendada", 1.1, 2.15, 5.0, 0.4, 18, CYAN, True)
    adicionar_lista(
        slide,
        [
            "Problema, objetivo e contexto do negócio.",
            "Método: fonte, captura, filtros e variáveis derivadas.",
            "Resultados quantitativos e resultados do Forms (após anexar a exportação).",
            "Discussão, limitações, recomendações e referências.",
        ],
        1.1,
        2.65,
        4.95,
        1.9,
        12,
        6,
    )
    adicionar_caixa(slide, 6.78, 1.9, 5.55, 2.95)
    adicionar_texto(slide, "Checklist da entrega", 7.08, 2.15, 4.9, 0.4, 18, GREEN, True)
    adicionar_lista(
        slide,
        [
            "Apresentação final revisada.",
            "Relatório final com fontes e limitações.",
            "CSV / algoritmo / dashboard identificados como artefatos distintos.",
            "Resultados do Forms conferidos com a exportação original.",
            "Backlog atualizado: concluído, pendente e responsável.",
        ],
        7.08,
        2.65,
        4.9,
        1.95,
        12,
        6,
    )
    adicionar_caixa(slide, 0.8, 5.15, 11.53, 1.35, CARD_ALT)
    adicionar_texto(slide, "Oportunidade de negócio destacada na entrega", 1.08, 5.34, 10.9, 0.34, 16, AMBER, True)
    adicionar_texto(
        slide,
        f"No CSV, {m['pet_pct']:.1f}% dos anúncios aceitam pets e {m['mobilia_pct']:.1f}% são mobiliados: testar serviço/parceria pet-friendly e pacote de mobília para locação. Validar demanda com respostas do Forms e piloto antes de investir.",
        1.08,
        5.78,
        10.9,
        0.56,
        12,
        TEXT,
    )

    # Retrospectiva
    slide = nova_pagina(prs, 12, "SPRINT 4 + FINAL • TAREFAS 14 E 18 — RETROSPECTIVA / BACKLOG", "O que erramos e o que faltou no Product Backlog")
    adicionar_caixa(slide, 0.8, 1.9, 5.65, 4.7)
    adicionar_texto(slide, "Pontos a melhorar", 1.1, 2.2, 5.0, 0.4, 19, ROSE, True)
    adicionar_lista(
        slide,
        [
            "A evidência da pesquisa com usuários não está junto ao código e à base.",
            "Sem coleta longitudinal, não se pode concluir tendência ou vacância.",
            "A API pode falhar; documentar data, cobertura e uso do fallback.",
            "A revisão final precisa validar consistência entre slides, dashboard e relatório.",
        ],
        1.1,
        2.82,
        4.95,
        3.2,
        14,
        12,
    )
    adicionar_caixa(slide, 6.78, 1.9, 5.55, 4.7)
    adicionar_texto(slide, "Product Backlog — próximos itens", 7.08, 2.2, 4.9, 0.4, 19, CYAN, True)
    adicionar_lista(
        slide,
        [
            "P0 • Anexar exportação do Forms e calcular frequências reais.",
            "P0 • Finalizar relatório e validar a apresentação com a equipe.",
            "P1 • Registrar data da coleta e sinalizar origem API vs. CSV.",
            "P1 • Automatizar testes das regras de limpeza e indicadores.",
            "P2 • Avaliar série histórica para análise de variação de preços.",
        ],
        7.08,
        2.82,
        4.9,
        3.35,
        13,
        10,
    )

    # Encerramento
    slide = nova_pagina(prs, 13, "SPRINT 4 + FINAL • TAREFAS 14 E 18 — ENTREGA", "Conclusão e próximos passos")
    adicionar_texto(
        slide,
        "O projeto demonstra um fluxo funcional de coleta, tratamento e exploração de anúncios imobiliários, com indicadores que apoiam comparações por região e tipologia.",
        1.05,
        2.05,
        11.1,
        1.1,
        21,
        TEXT,
        True,
    )
    adicionar_caixa(slide, 1.05, 3.55, 11.1, 1.55)
    adicionar_texto(
        slide,
        "Para fechar a entrega acadêmica: incorporar os resultados reais do Google Forms, concluir o relatório e registrar no backlog o que foi concluído e o que permanece pendente.",
        1.38,
        3.9,
        10.4,
        0.85,
        17,
        CYAN,
        True,
    )
    adicionar_texto(
        slide,
        "Obrigado(a)!  •  Perguntas e discussão",
        1.05,
        5.85,
        11.1,
        0.55,
        20,
        MUTED,
        False,
        PP_ALIGN.CENTER,
    )

    prs.save(ARQUIVO_SAIDA)
    print(f"Apresentação gerada: {ARQUIVO_SAIDA}")
    print(f"Slides: {len(prs.slides)} | Registros válidos analisados: {m['validos']}")


if __name__ == "__main__":
    gerar()
