# Análise exploratória do mercado de locação residencial em São Paulo

Projeto acadêmico de análise de anúncios residenciais do QuintoAndar, desenvolvido para o Projeto Integrador da FATEC SEBRAE.

**Dashboard online:** [Abrir o dashboard](https://mercado-locacao-residencial-sp.streamlit.app/)

## O projeto

- Dashboard interativo em Streamlit com indicadores, análise territorial e gráficos.
- Estimativa de aluguel com Regressão Linear Múltipla (Scikit-Learn).
- Captura concorrente de anúncios usando `requests` e `ThreadPoolExecutor`.
- Base CSV local usada como alternativa quando a API pública não responde.
- Scripts e apresentação do Projeto Integrador Sprint 4.

## Executar localmente

Requer Python e Git instalados.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run Quintoandar.py
```

O dashboard lê `quinto_andar_transformed_data.csv` e `Logo_1_QuintoAndar.png` do diretório do projeto.

## Publicar o dashboard

1. Envie este repositório ao GitHub.
2. No [Streamlit Community Cloud](https://share.streamlit.io/), conecte sua conta do GitHub e selecione o repositório.
3. Configure `Quintoandar.py` como arquivo principal e publique o app.

O dashboard tenta consultar a API pública do QuintoAndar e usa a base CSV local como fallback. A disponibilidade e o conteúdo da API podem mudar.

## Dados e limitações

Os dados representam anúncios disponíveis no momento da coleta e podem não corresponder aos valores finais dos contratos. As estimativas do modelo são exploratórias e não substituem uma avaliação profissional. Projeto acadêmico, sem vínculo oficial com o QuintoAndar.
