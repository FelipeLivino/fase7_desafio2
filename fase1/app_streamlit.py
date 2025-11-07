
import streamlit as st
import subprocess
import pandas as pd
import math
import json
import time

# Constantes
LOAD_FILENAME = "storage.json"
LARGURA_RUA = 1

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Plantio",
    page_icon="🌱",
    layout="wide"
)

# ================ FUNÇÕES DO ENGINE ================

def save_json(obj):
    """Saves a Python object as a JSON file."""
    try:
        with open(LOAD_FILENAME, 'w', encoding='utf-8') as file:
            json.dump(obj, file, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar arquivo: {e}")

def load_json():
    """Loads a JSON file into a Python object."""
    try:
        with open(LOAD_FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON de {LOAD_FILENAME}")
        return []
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return []

def calcular_area(cultura, dimensoes):
    """Calcula área conforme a cultura"""
    if cultura == "soja":
        return dimensoes[0] * dimensoes[1]  # Retângulo (largura * comprimento)
    elif cultura == "milho":
        return math.pi * (dimensoes[0] ** 2)  # Círculo (pi * raio²)
    else:
        return None

def calcular_ruas(cultura, dimensoes):
    """Calcula quantidade e área das ruas"""
    if cultura == "soja":
        maior_dimensao = dimensoes[0]
        menor_dimensao = dimensoes[1]
        if dimensoes[1] > dimensoes[0]:
            maior_dimensao = dimensoes[1]
            menor_dimensao = dimensoes[0]
        
        quantidade_ruas = menor_dimensao / 5
        area_ruas = quantidade_ruas * maior_dimensao * LARGURA_RUA
        return quantidade_ruas, area_ruas
    elif cultura == "milho":
        quantidade_ruas = 2  # Fixo para milho
        area_ruas = dimensoes[0] * quantidade_ruas * LARGURA_RUA  # raio * 2 * largura_rua
        return quantidade_ruas, area_ruas
    else:
        return None, None

def calcular_insumos(quantidade_por_metro, total_metros):
    """Calcula insumos necessários"""
    return quantidade_por_metro * total_metros

def convert_ml_to_l(ml):
    """Converte ml para litros"""
    return ml / 1000

def get_form_plantio_streamlit(cultura, dimensoes, produto, quantidade_por_metro):
    """Versão Streamlit da função get_form_plantio"""
    area_total = calcular_area(cultura, dimensoes)
    quantidade_ruas, area_rua = calcular_ruas(cultura, dimensoes)
    area_util = area_total - area_rua
    insumos = calcular_insumos(convert_ml_to_l(quantidade_por_metro), area_util)
    
    plantio_obj = {
        "cultura": cultura,
        "area_total": area_total,
        "produto": produto,
        "insumos": insumos,
        "quantidade_ruas": quantidade_ruas,
        "area_rua": area_rua,
        "area_util": area_util
    }
    return plantio_obj

# ================ INICIALIZAÇÃO ================

if 'dados_plantio' not in st.session_state:
    try:
        loaded_data = load_json()
        st.session_state.dados_plantio = loaded_data if loaded_data else []
    except:
        st.session_state.dados_plantio = []

# Inicializar variáveis de feedback
if 'show_success_feedback' not in st.session_state:
    st.session_state.show_success_feedback = False
if 'ultimo_dado_adicionado' not in st.session_state:
    st.session_state.ultimo_dado_adicionado = None

# ================ INTERFACE PRINCIPAL ================

def main():
    st.title("🌱 Sistema de Gestão de Plantio")
    st.markdown("---")
    
    # Sidebar para navegação
    st.sidebar.title("Menu Principal")
    opcao = st.sidebar.selectbox(
        "Escolha uma opção:",
        [
            "📊 Dashboard",
            "➕ Adicionar Dados de Plantio",
            "📋 Visualizar Dados",
            "✏️ Atualizar Dados",
            "🗑️ Excluir Dados",
            "📈 Estatísticas (R)",
            "🌤️ Dados Climáticos"
        ]
    )
    
    if opcao == "📊 Dashboard":
        mostrar_dashboard()
    elif opcao == "➕ Adicionar Dados de Plantio":
        adicionar_dados()
    elif opcao == "📋 Visualizar Dados":
        visualizar_dados()
    elif opcao == "✏️ Atualizar Dados":
        atualizar_dados()
    elif opcao == "🗑️ Excluir Dados":
        excluir_dados()
    elif opcao == "📈 Estatísticas (R)":
        executar_estatisticas()
    elif opcao == "🌤️ Dados Climáticos":
        dados_climaticos()

def mostrar_feedback_sucesso():
    """Exibe feedback visual de sucesso"""
    if st.session_state.show_success_feedback and st.session_state.ultimo_dado_adicionado:
        
        # Container especial para feedback
        feedback_container = st.container()
        
        with feedback_container:
            
            # Mensagem de sucesso destacada
            st.success("🎉 **DADOS ADICIONADOS COM SUCESSO!** 🎉")
            
            # Card com resumo do que foi adicionado
            dado = st.session_state.ultimo_dado_adicionado
            icon = "🌾" if dado['cultura'] == 'soja' else "🌽"
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(90deg, #4CAF50, #45a049);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            ">
                <h3 style="margin: 0; color: white;">
                    {icon} Registro Adicionado - {dado['cultura'].title()}
                </h3>
                <div style="margin-top: 15px; display: flex; justify-content: space-around;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold;">📐</div>
                        <div>Área Total</div>
                        <div style="font-size: 18px; font-weight: bold;">{dado['area_total']:.2f} m²</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold;">🎯</div>
                        <div>Área Útil</div>
                        <div style="font-size: 18px; font-weight: bold;">{dado['area_util']:.2f} m²</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold;">💧</div>
                        <div>Insumos</div>
                        <div style="font-size: 18px; font-weight: bold;">{dado['insumos']:.2f} L</div>
                    </div>
                </div>
                <div style="margin-top: 15px; text-align: center;">
                    <div style="font-size: 16px;">
                        🧪 Produto: <strong>{dado['produto']}</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Estatísticas atualizadas
            total_registros = len(st.session_state.dados_plantio)
            area_total_sistema = sum(d['area_total'] for d in st.session_state.dados_plantio)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "📈 Total de Registros", 
                    total_registros,
                    delta=1,
                    delta_color="normal"
                )
            
            with col2:
                st.metric(
                    "📐 Área Total Sistema", 
                    f"{area_total_sistema:.2f} m²",
                    delta=f"+{dado['area_total']:.2f} m²",
                    delta_color="normal"
                )
            
            with col3:
                insumos_total = sum(d['insumos'] for d in st.session_state.dados_plantio)
                st.metric(
                    "💧 Insumos Total", 
                    f"{insumos_total:.2f} L",
                    delta=f"+{dado['insumos']:.2f} L",
                    delta_color="normal"
                )
            
            # Progress bar animado
            st.subheader("📊 Processamento Concluído")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(101):
                progress_bar.progress(i)
                if i < 30:
                    status_text.text(f'🔄 Validando dados... {i}%')
                elif i < 60:
                    status_text.text(f'💾 Salvando no sistema... {i}%')
                elif i < 90:
                    status_text.text(f'📊 Atualizando estatísticas... {i}%')
                else:
                    status_text.text(f'✅ Finalizado! {i}%')
                time.sleep(0.01)
            
            status_text.text('🎉 Dados salvos com sucesso!')
            
            # Botões de ação
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("➕ Adicionar Outro", type="primary", use_container_width=True):
                    st.session_state.show_success_feedback = False
                    st.session_state.ultimo_dado_adicionado = None
                    st.rerun()
            
            with col2:
                if st.button("📋 Ver Todos os Dados", use_container_width=True):
                    st.session_state.show_success_feedback = False
                    st.session_state.ultimo_dado_adicionado = None
                    st.rerun()
            
            with col3:
                if st.button("📊 Ver Dashboard", use_container_width=True):
                    st.session_state.show_success_feedback = False
                    st.session_state.ultimo_dado_adicionado = None
                    st.rerun()

def mostrar_dashboard():
    st.header("📊 Dashboard Geral")
    
    if not st.session_state.dados_plantio:
        st.info("🌾 Nenhum dado de plantio cadastrado. Use o menu lateral para adicionar dados.")
        return
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    total_registros = len(st.session_state.dados_plantio)
    area_total = sum(dado['area_total'] for dado in st.session_state.dados_plantio)
    area_util_total = sum(dado['area_util'] for dado in st.session_state.dados_plantio)
    insumos_total = sum(dado['insumos'] for dado in st.session_state.dados_plantio)
    
    with col1:
        st.metric("📈 Total de Registros", total_registros)
    with col2:
        st.metric("📐 Área Total", f"{area_total:.2f} m²")
    with col3:
        st.metric("🎯 Área Útil Total", f"{area_util_total:.2f} m²")
    with col4:
        st.metric("🧪 Insumos Total", f"{insumos_total:.2f} L")
    
    # Análise por cultura
    st.subheader("📊 Análise por Cultura")
    
    culturas_count = {}
    areas_por_cultura = {}
    
    for dado in st.session_state.dados_plantio:
        cultura = dado['cultura'].title()
        culturas_count[cultura] = culturas_count.get(cultura, 0) + 1
        areas_por_cultura[cultura] = areas_por_cultura.get(cultura, 0) + dado['area_total']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Quantidade por Cultura:**")
        for cultura, count in culturas_count.items():
            icon = "🌾" if cultura == "Soja" else "🌽"
            st.write(f"{icon} {cultura}: {count} registro(s)")
    
    with col2:
        st.write("**Área por Cultura:**")
        for cultura, area in areas_por_cultura.items():
            icon = "🌾" if cultura == "Soja" else "🌽"
            st.write(f"{icon} {cultura}: {area:.2f} m²")
    
    # Tabela resumo
    st.subheader("📋 Resumo dos Dados")
    df = pd.DataFrame(st.session_state.dados_plantio)
    
    # Formatação das colunas numéricas
    numeric_cols = ['area_total', 'area_util', 'area_rua', 'insumos', 'quantidade_ruas']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].round(2)
    
    st.dataframe(df, use_container_width=True)

def adicionar_dados():
    st.header("➕ Adicionar Dados de Plantio")
    
    # Mostrar feedback de sucesso se aplicável
    if st.session_state.show_success_feedback:
        mostrar_feedback_sucesso()
        return
    
    # Inicializar session state para controlar a cultura selecionada
    if 'cultura_selecionada' not in st.session_state:
        st.session_state.cultura_selecionada = "soja"
    
    # Seleção da cultura FORA do formulário para atualização dinâmica
    st.subheader("🌾 Seleção da Cultura")
    cultura_nova = st.selectbox(
        "Escolha o tipo de cultura:",
        ["soja", "milho"],
        index=0 if st.session_state.cultura_selecionada == "soja" else 1,
        help="Selecione o tipo de cultura para plantio",
        key="select_cultura_add"
    )
    
    # Atualizar session state quando cultura muda
    if cultura_nova != st.session_state.cultura_selecionada:
        st.session_state.cultura_selecionada = cultura_nova
        st.rerun()
    
    # Formulário com campos específicos baseados na cultura selecionada
    with st.form("form_plantio", clear_on_submit=True):
        st.subheader(f"📊 Informações - {cultura_nova.title()}")
        
        # Campos específicos por cultura com keys únicos
        if cultura_nova == "soja":
            st.info("🌾 **Soja**: Área retangular - informe largura e comprimento em metros")
            
            col1, col2 = st.columns(2)
            with col1:
                largura = st.number_input(
                    "Largura da área (metros):", 
                    min_value=0.1, 
                    step=0.1, 
                    value=10.0,
                    help="Largura do terreno em metros",
                    key="largura_soja"
                )
            with col2:
                comprimento = st.number_input(
                    "Comprimento da área (metros):", 
                    min_value=0.1, 
                    step=0.1, 
                    value=10.0,
                    help="Comprimento do terreno em metros",
                    key="comprimento_soja"
                )
            
            dimensoes = (largura, comprimento)
            
            # Calcular e mostrar prévia da área para soja
            area_preview = largura * comprimento
            ruas_preview = min(largura, comprimento) / 5
            area_ruas_preview = ruas_preview * max(largura, comprimento) * LARGURA_RUA
            area_util_preview = area_preview - area_ruas_preview
            
            st.success(f"📊 **Cálculos para Soja (Área Retangular):**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Largura", f"{largura:.1f} m")
            with col2:
                st.metric("Comprimento", f"{comprimento:.1f} m")
            with col3:
                st.metric("Área Total", f"{area_preview:.2f} m²")
            with col4:
                st.metric("Área Útil", f"{area_util_preview:.2f} m²")
            
        else:  # milho
            st.info("🌽 **Milho**: Área circular - informe apenas o raio em metros")
            
            raio = st.number_input(
                "Raio da área circular (metros):", 
                min_value=0.1, 
                step=0.1, 
                value=5.0,
                help="Raio da área circular em metros",
                key="raio_milho"
            )
            
            dimensoes = (raio,)  # Tupla com apenas o raio
            
            # Calcular e mostrar prévia da área para milho
            area_preview = math.pi * (raio ** 2)
            ruas_preview = 2  # Fixo para milho
            area_ruas_preview = raio * ruas_preview * LARGURA_RUA
            area_util_preview = area_preview - area_ruas_preview
            
            st.success(f"📊 **Cálculos para Milho (Área Circular):**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Raio", f"{raio:.1f} m")
            with col2:
                st.metric("Área Total (π×r²)", f"{area_preview:.2f} m²")
            with col3:
                st.metric("Número de Ruas", f"{ruas_preview}")
            with col4:
                st.metric("Área Útil", f"{area_util_preview:.2f} m²")
        
        st.markdown("---")
        st.subheader("🧪 Informações do Produto")
        
        produto = st.text_input(
            "Nome do produto para manejo:", 
            placeholder="Ex: Herbicida, Fungicida, Inseticida...",
            help="Nome do produto químico que será aplicado",
            key="produto_input"
        )
        
        quantidade_por_metro = st.number_input(
            "Quantidade por m² (ml):", 
            min_value=0.1, 
            step=0.1, 
            value=10.0,
            help="Quantidade do produto em mililitros por metro quadrado",
            key="quantidade_input"
        )
        
        # Mostrar cálculo de insumos
        if quantidade_por_metro > 0:
            if cultura_nova == "soja":
                area_util_calc = area_util_preview
            else:  # milho
                area_util_calc = area_util_preview
            
            insumos_preview = convert_ml_to_l(quantidade_por_metro) * area_util_calc
            
            st.info(f"💧 **Insumos necessários:** {insumos_preview:.2f} Litros")
            st.caption(f"Cálculo: {quantidade_por_metro} ml/m² × {area_util_calc:.2f} m² ÷ 1000 = {insumos_preview:.2f} L")
        
        st.markdown("---")
        submitted = st.form_submit_button("✅ Adicionar Dados", type="primary", use_container_width=True)
        
        if submitted:
            if produto.strip() and quantidade_por_metro > 0:
                # Mostrar spinner durante o processamento
                with st.spinner("🔄 Processando dados..."):
                    time.sleep(1)  # Simular processamento
                    
                    try:
                        novo_dado = get_form_plantio_streamlit(cultura_nova, dimensoes, produto, quantidade_por_metro)
                        st.session_state.dados_plantio.append(novo_dado)
                        save_json(st.session_state.dados_plantio)
                        
                        # Configurar feedback de sucesso
                        st.session_state.ultimo_dado_adicionado = novo_dado
                        st.session_state.show_success_feedback = True
                        
                        # Reset da cultura selecionada para forçar limpeza dos campos
                        st.session_state.cultura_selecionada = "soja"
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar dados: {e}")
                        st.exception(e)  # Mostra detalhes do erro para debug
            else:
                st.error("❌ Por favor, preencha todos os campos obrigatórios!")
                
                # Feedback específico sobre campos vazios
                if not produto.strip():
                    st.warning("🧪 Campo 'Produto' é obrigatório!")
                if quantidade_por_metro <= 0:
                    st.warning("💧 Quantidade por m² deve ser maior que zero!")

def visualizar_dados():
    st.header("📋 Visualizar Dados")
    
    if not st.session_state.dados_plantio:
        st.info("🌾 Nenhum dado de plantio cadastrado. Use o menu lateral para adicionar dados.")
        return
    
    # Filtros
    st.subheader("🔍 Filtros")
    col1, col2 = st.columns(2)
    
    with col1:
        culturas_disponiveis = list(set(dado['cultura'] for dado in st.session_state.dados_plantio))
        cultura_filter = st.selectbox("Filtrar por cultura:", ["Todas"] + culturas_disponiveis)
    
    with col2:
        tipo_view = st.radio("Tipo de visualização:", ["📋 Cards", "📊 Tabela"])
    
    # Aplicar filtros
    dados_filtrados = st.session_state.dados_plantio
    if cultura_filter != "Todas":
        dados_filtrados = [dado for dado in dados_filtrados if dado['cultura'] == cultura_filter]
    
    if not dados_filtrados:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        return
    
    st.subheader(f"📊 Resultados ({len(dados_filtrados)} registro(s))")
    
    if tipo_view == "📋 Cards":
        for i, dado in enumerate(dados_filtrados):
            # Encontrar índice original
            indice_original = st.session_state.dados_plantio.index(dado)
            
            # Ícone baseado na cultura
            icon = "🌾" if dado['cultura'] == 'soja' else "🌽"
            
            with st.expander(f"{icon} Registro {indice_original} - {dado['cultura'].title()}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📊 Informações Básicas**")
                    st.write(f"{icon} **Cultura:** {dado['cultura'].title()}")
                    st.write(f"🧪 **Produto:** {dado['produto']}")
                    if dado['cultura'] == 'milho':
                        raio_calc = math.sqrt(dado['area_total'] / math.pi)
                        st.write(f"📐 **Raio:** {raio_calc:.2f} m")
                    st.write(f"📐 **Área Total:** {dado['area_total']:.2f} m²")
                
                with col2:
                    st.markdown("**🛣️ Informações das Ruas**")
                    st.write(f"🔢 **Número de Ruas:** {dado['quantidade_ruas']:.2f}")
                    st.write(f"📏 **Área das Ruas:** {dado['area_rua']:.2f} m²")
                    st.write(f"🎯 **Área Útil:** {dado['area_util']:.2f} m²")
                
                with col3:
                    st.markdown("**💧 Insumos**")
                    st.write(f"🧪 **Insumos Necessários:** {dado['insumos']:.2f} L")
                    if dado['area_util'] > 0:
                        ml_por_m2 = (dado['insumos'] * 1000) / dado['area_util']
                        st.write(f"📊 **ml por m²:** {ml_por_m2:.2f} ml")
    else:
        df = pd.DataFrame(dados_filtrados)
        
        # Adicionar índices originais
        indices_originais = []
        for dado in dados_filtrados:
            indices_originais.append(st.session_state.dados_plantio.index(dado))
        
        df.insert(0, 'Índice', indices_originais)
        
        # Formatação
        numeric_columns = ['area_total', 'area_util', 'area_rua', 'insumos', 'quantidade_ruas']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].round(2)
        
        st.dataframe(df, use_container_width=True)

def atualizar_dados():
    st.header("✏️ Atualizar Dados")
    
    if not st.session_state.dados_plantio:
        st.info("🌾 Nenhum dado de plantio cadastrado.")
        return
    
    # Seletor de registro
    opcoes = [f"Registro {i} - {dado['cultura'].title()} - {dado['produto']}" 
              for i, dado in enumerate(st.session_state.dados_plantio)]
    
    indice_selecionado = st.selectbox("Selecione o registro para atualizar:", range(len(opcoes)), 
                                     format_func=lambda x: opcoes[x])
    
    if indice_selecionado is not None:
        dado_atual = st.session_state.dados_plantio[indice_selecionado]
        
        with st.form("form_atualizar"):
            st.subheader(f"✏️ Atualizando Registro {indice_selecionado}")
            
            # Mostrar dados atuais
            icon = "🌾" if dado_atual['cultura'] == 'soja' else "🌽"
            st.info(f"{icon} **Dados Atuais:** {dado_atual['cultura'].title()} - {dado_atual['produto']}")
            
            # Seleção da cultura
            cultura_atual_index = 0 if dado_atual['cultura'] == 'soja' else 1
            cultura = st.selectbox("Cultura:", ["soja", "milho"], index=cultura_atual_index)
            
            # Campos específicos por cultura
            if cultura == "soja":
                st.info("🌾 **Soja**: Área retangular - informe largura e comprimento")
                
                # Estimar dimensões atuais para soja
                area_atual = dado_atual['area_total']
                largura_estimada = math.sqrt(area_atual)
                comprimento_estimado = area_atual / largura_estimada
                
                col1, col2 = st.columns(2)
                with col1:
                    largura = st.number_input("Largura (metros):", min_value=0.1, step=0.1, value=largura_estimada)
                with col2:
                    comprimento = st.number_input("Comprimento (metros):", min_value=0.1, step=0.1, value=comprimento_estimado)
                dimensoes = (largura, comprimento)
                
            else:  # milho
                st.info("🌽 **Milho**: Área circular - informe apenas o raio")
                
                # Calcular raio atual para milho
                if dado_atual['cultura'] == 'milho':
                    raio_atual = math.sqrt(dado_atual['area_total'] / math.pi)
                else:
                    raio_atual = math.sqrt(dado_atual['area_total'] / math.pi)
                
                raio = st.number_input("Raio (metros):", min_value=0.1, step=0.1, value=raio_atual)
                dimensoes = (raio,)
            
            produto = st.text_input("Produto:", value=dado_atual['produto'])
            
            # Calcular quantidade por metro baseada nos dados atuais
            if dado_atual['area_util'] > 0:
                quantidade_atual = (dado_atual['insumos'] * 1000) / dado_atual['area_util']
            else:
                quantidade_atual = 10.0
                
            quantidade_por_metro = st.number_input("Quantidade por m² (ml):", min_value=0.1, step=0.1, 
                                                 value=quantidade_atual)
            
            submitted = st.form_submit_button("✅ Atualizar Dados", type="primary")
            
            if submitted:
                if produto.strip() and quantidade_por_metro > 0:
                    try:
                        dados_atualizados = get_form_plantio_streamlit(cultura, dimensoes, produto, quantidade_por_metro)
                        st.session_state.dados_plantio[indice_selecionado] = dados_atualizados
                        save_json(st.session_state.dados_plantio)
                        st.success("✅ Dados atualizados com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar dados: {e}")
                else:
                    st.error("❌ Por favor, preencha todos os campos obrigatórios!")

def excluir_dados():
    st.header("🗑️ Excluir Dados")
    
    if not st.session_state.dados_plantio:
        st.info("🌾 Nenhum dado de plantio cadastrado.")
        return
    
    # Seletor de registro
    opcoes = [f"Registro {i} - {dado['cultura'].title()} - {dado['produto']}" 
              for i, dado in enumerate(st.session_state.dados_plantio)]
    
    indice_selecionado = st.selectbox("Selecione o registro para excluir:", range(len(opcoes)), 
                                     format_func=lambda x: opcoes[x])
    
    if indice_selecionado is not None:
        dado_selecionado = st.session_state.dados_plantio[indice_selecionado]
        
        st.subheader("📋 Dados a serem excluídos:")
        
        icon = "🌾" if dado_selecionado['cultura'] == 'soja' else "🌽"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"{icon} **Cultura:** {dado_selecionado['cultura'].title()}")
            st.write(f"🧪 **Produto:** {dado_selecionado['produto']}")
            st.write(f"📐 **Área Total:** {dado_selecionado['area_total']:.2f} m²")
        with col2:
            st.write(f"🎯 **Área Útil:** {dado_selecionado['area_util']:.2f} m²")
            st.write(f"🛣️ **Área das Ruas:** {dado_selecionado['area_rua']:.2f} m²")
            st.write(f"🔢 **Número de Ruas:** {dado_selecionado['quantidade_ruas']:.2f}")
        with col3:
            st.write(f"💧 **Insumos:** {dado_selecionado['insumos']:.2f} L")
            if dado_selecionado['cultura'] == 'milho':
                raio_calc = math.sqrt(dado_selecionado['area_total'] / math.pi)
                st.write(f"📐 **Raio:** {raio_calc:.2f} m")
        
        st.warning("⚠️ **ATENÇÃO:** Esta ação não pode ser desfeita!")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🗑️ Confirmar Exclusão", type="primary"):
                st.session_state.dados_plantio.pop(indice_selecionado)
                try:
                    save_json(st.session_state.dados_plantio)
                    st.success("✅ Dado removido com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar dados: {e}")

def executar_estatisticas():
    st.header("📈 Estatísticas (R)")
    
    st.info("🔬 Esta funcionalidade executa scripts R para análise estatística dos dados.")
    
    if st.button("🚀 Executar Análise Estatística", type="primary"):
        with st.spinner("🔄 Executando programa em R para estatísticas..."):
            try:
                resultado = subprocess.run(
                    ["Rscript", "projeto_r/main.R"], 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                
                if resultado.returncode == 0:
                    st.success("✅ Análise executada com sucesso!")
                    st.subheader("📊 Resultado da Análise:")
                    st.code(resultado.stdout, language="r")
                else:
                    st.error("❌ Erro na execução do script R")
                    st.subheader("❌ Mensagem de Erro:")
                    st.code(resultado.stderr, language="bash")
                    
            except subprocess.TimeoutExpired:
                st.error("⏰ Timeout: O script R demorou muito para executar (>30s)")
            except FileNotFoundError:
                st.error("❌ Rscript não encontrado. Certifique-se de que o R está instalado e no PATH do sistema")
                st.info("💡 **Dica:** Instale o R em https://www.r-project.org/")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")

def dados_climaticos():
    st.header("🌤️ Dados Climáticos")
    
    st.info("🌍 Esta funcionalidade consulta dados climáticos para auxiliar no planejamento do plantio.")
    
    cidade = st.text_input("🏙️ Informe a cidade:", placeholder="Ex: São Paulo, Rio de Janeiro...")
    
    if st.button("🌤️ Obter Dados Climáticos", type="primary") and cidade:
        with st.spinner(f"🔄 Obtendo dados climáticos para {cidade}..."):
            try:
                resultado = subprocess.run(
                    ["Rscript", "projeto_r/services/weatherLocationService.R", cidade], 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                
                if resultado.returncode == 0:
                    st.success(f"✅ Dados climáticos obtidos para {cidade}!")
                    st.subheader(f"🌤️ Dados Climáticos - {cidade}")
                    st.code(resultado.stdout, language="r")
                else:
                    st.error("❌ Erro na execução do script R")
                    st.subheader("❌ Mensagem de Erro:")
                    st.code(resultado.stderr, language="bash")
                    
            except subprocess.TimeoutExpired:
                st.error("⏰ Timeout: O script R demorou muito para executar (>30s)")
            except FileNotFoundError:
                st.error("❌ Rscript não encontrado. Certifique-se de que o R está instalado e no PATH do sistema")
                st.info("💡 **Dica:** Instale o R em https://www.r-project.org/")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")

# ================ EXECUÇÃO PRINCIPAL ================

if __name__ == "__main__":
    main()
