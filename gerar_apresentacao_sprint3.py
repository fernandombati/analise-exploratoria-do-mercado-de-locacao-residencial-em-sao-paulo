from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def criar_apresentacao():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta de Cores (Foco em Alto Contraste e Tema Dark Inspirado no Dashboard)
    COR_BG = RGBColor(18, 22, 28)          # #12161c
    COR_CARD = RGBColor(26, 33, 45)        # #1a212d
    COR_TEXTO = RGBColor(243, 244, 246)    # #f3f4f6
    COR_SUB = RGBColor(139, 148, 158)      # #8b949e
    COR_DESTAQUE = RGBColor(56, 189, 248)  # #38bdf8 (Azul Ciano)
    COR_TOPO_BG = RGBColor(35, 134, 54)    # Verde Institucional para os Tópicos Exigidos

    def aplicar_fundo(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COR_BG

    def adicionar_topo_obrigatorio(slide, topicos_texto):
        # Caixa de Destaque no Topo com os Quesitos Exigidos pela Sprint 3
        topo_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(0.6))
        tf = topo_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"📌 TÓPICOS EXIGIDOS / SPRINT 3: {topicos_texto}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COR_DESTAQUE
        p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 1: CAPA
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    aplicar_fundo(slide1)

    box_capa = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.33), Inches(4.0))
    tf1 = box_capa.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🏠 Projeto Integrador: Análise de Dados I"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COR_TEXTO

    p2 = tf1.add_paragraph()
    p2.text = "Análise Imobiliária QuintoAndar (CNAE 6822-6/00) — Dashboard Interativo"
    p2.font.size = Pt(20)
    p2.font.color.rgb = COR_DESTAQUE
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Aluno: Fernando A. de Assis | FATEC SEBRAE | Prof. Rômulo F. S. Maia"
    p3.space_before = Pt(30)
    p3.font.size = Pt(14)
    p3.font.color.rgb = COR_SUB

    # =========================================================================
    # SLIDE 2: INTRODUÇÃO E ESCOPO DO NEGÓCIO
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    aplicar_fundo(slide2)
    adicionar_topo_obrigatorio(slide2, "Seleção da Empresa, Escopo do Negócio e Enquadramento CNAE")

    box2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.5))
    tf2 = box2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "Contexto e Alinhamento Acadêmico-Empresarial"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COR_TEXTO

    conteudo_s2 = [
        ("Ecossistema QuintoAndar:", " Plataforma líder em proptech no Brasil, fundada em 2013 para desburocratizar o mercado de locação residencial (sem fiador e 100% digital)."),
        ("Enquadramento CNAE:", " 6822-6/00 — Gestão e administração de bens imobiliários por conta de terceiros."),
        ("Objetivo do Projeto:", " Utilizar engenharia de dados (Python, Streamlit, API REST e Pandas) para analisar tendências de mercado, elasticidade de preços por metro quadrado e otimizar processos decisórios no setor imobiliário.")
    ]

    for titulo, desc in conteudo_s2:
        p = tf2.add_paragraph()
        p.space_before = Pt(14)
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(16)
        run1.font.color.rgb = COR_DESTAQUE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(15)
        run2.font.color.rgb = COR_TEXTO

    # =========================================================================
    # SLIDE 3: ARQUITETURA DE DADOS E ETL (SPRINT 3)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    aplicar_fundo(slide3)
    adicionar_topo_obrigatorio(slide3, "Coleta de Dados, Ingestão via API e Concorrência (ThreadPoolExecutor)")

    box3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.5))
    tf3 = box3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "Pipeline de Ingestão e Engenharia de Dados"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COR_TEXTO

    conteudo_s3 = [
        ("Requisições Concorrentes:", " Utilização de Python `requests` com `ThreadPoolExecutor` (10 workers) consultando a API pública do QuintoAndar via quadrantes geográficos de São Paulo (Latitude/Longitude)."),
        ("Extração de Atributos:", " Captura em tempo real de metadados críticos: ID do imóvel, URL, bairro, valor de aluguel, condomínio, IPTU, metragem útil, número de quartos e comodidades (aceitação de pets e mobília)."),
        ("Resiliência (Fallback):", " O algoritmo conta com suporte automático a base local (`quinto_andar_transformed_data.csv`) caso ocorra instabilidade na API em tempo real.")
    ]

    for titulo, desc in conteudo_s3:
        p = tf3.add_paragraph()
        p.space_before = Pt(14)
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(16)
        run1.font.color.rgb = COR_DESTAQUE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(15)
        run2.font.color.rgb = COR_TEXTO

    # =========================================================================
    # SLIDE 4: TRATAMENTO E SANITIZAÇÃO (CRISP-DM)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    aplicar_fundo(slide4)
    adicionar_topo_obrigatorio(slide4, "Pré-processamento, Limpeza de Dados e Tratamento de Outliers")

    box4 = slide4.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.5))
    tf4 = box4.text_frame
    tf4.word_wrap = True

    p = tf4.paragraphs[0]
    p.text = "Sanitização e Rigor Estatístico (Metodologia CRISP-DM)"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COR_TEXTO

    conteudo_s4 = [
        ("Deduplicação Estrita:", " Remoção de registros duplicados baseada no ID numérico extraído da URL, eliminando sobreposições geográficas entre os quadrantes da API."),
        ("Filtragem de Outliers:", " Exclusão automatizada de inconsistências de mercado (imóveis com menos de 12m² ou mais de 800m²; aluguéis abaixo de R\$ 500 ou acima de R\$ 50.000)."),
        ("Variáveis Derivadas:", " Cálculo em tempo real do Preço por m² (`Aluguel / Metragem`) e do Custo Total Calculado (`Aluguel + Condomínio + IPTU`). Uso de **Medianas** para evitar distorções por valores extremos.")
    ]

    for titulo, desc in conteudo_s4:
        p = tf4.add_paragraph()
        p.space_before = Pt(14)
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(16)
        run1.font.color.rgb = COR_DESTAQUE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(15)
        run2.font.color.rgb = COR_TEXTO

    # =========================================================================
    # SLIDE 5: ANÁLISE EXPLORATÓRIA E VISUALIZAÇÕES (SPRINT 3)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    aplicar_fundo(slide5)
    adicionar_topo_obrigatorio(slide5, "Análise Exploratória, Gráficos de Dispersão e Correlação de Preços")

    box5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.5))
    tf5 = box5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "Insights do Gráfico de Dispersão e Cruzamento de Dados"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COR_TEXTO

    conteudo_s5 = [
        ("Eixo X & Y (Área vs Aluguel):", " Mapeia a elasticidade do espaço físico em relação ao preço cobrado mensalmente em Reais."),
        ("Dimensões Cruzadas (Cor e Tamanho):", " A cor da bolha indica o Preço/m² (tons mais claros refletem regiões nobres); o tamanho da bolha expressa o Custo Total."),
        ("Padrões de Mercado Revelados:", " Identifica unidades compactas de altíssimo valor em bairros centrais (Jardins, Itaim Bibi) e imóveis amplos com aluguel moderado em regiões periféricas.")
    ]

    for titulo, desc in conteudo_s5:
        p = tf5.add_paragraph()
        p.space_before = Pt(14)
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(16)
        run1.font.color.rgb = COR_DESTAQUE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(15)
        run2.font.color.rgb = COR_TEXTO

    # =========================================================================
    # SLIDE 6: ESTRATÉGIA DE NEGÓCIO E ALinhamento aos ODS (SPRINT 4)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    aplicar_fundo(slide6)
    adicionar_topo_obrigatorio(slide6, "Análise Estratégica, Prevenção de Declínio e Alinhamento com ODS da ONU")

    box6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.73), Inches(5.5))
    tf6 = box6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "Prevenção de Riscos e Impacto Sustentável"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COR_TEXTO

    conteudo_s6 = [
        ("Mitigação de Estoque Parado:", " Imóveis com preços acima da mediana regional e mais de 60 dias vagos exigem reajuste dinâmico automatizado por IA."),
        ("ODS 11 (Cidades Sustentáveis):", " Otimização do uso de imóveis urbanos e análise de densidade para habitações eficientes."),
        ("ODS 8 (Crescimento Econômico):", " Fomento à inovação tecnológica imobiliária (Proptech) e desburocratização de processos locatícios.")
    ]

    for titulo, desc in conteudo_s6:
        p = tf6.add_paragraph()
        p.space_before = Pt(14)
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(16)
        run1.font.color.rgb = COR_DESTAQUE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(15)
        run2.font.color.rgb = COR_TEXTO

    # Salvar Apresentação
    nome_arquivo = "Apresentacao_Projeto_Integrador_Sprint3.pptx"
    prs.save(nome_arquivo)
    print(f"Apresentação gerada com sucesso: {nome_arquivo}")

if __name__ == "__main__":
    criar_apresentacao()