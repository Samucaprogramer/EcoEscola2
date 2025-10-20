import streamlit as st
from datetime import datetime
import random

# Configuração da página
st.set_page_config(
    page_title="EcoEscola",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para aparência moderna
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 20px auto;
        max-width: 1200px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .stat-card h1 {
        font-size: 3em;
        margin: 10px 0;
    }
    .card-ok {
        background: #d4edda;
        border: 2px solid #28a745;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .card-wait {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .card {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    h1 {
        color: #667eea;
        text-align: center;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 12px 25px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session_state
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = []
if 'descartes' not in st.session_state:
    st.session_state.descartes = []
if 'resgates' not in st.session_state:
    st.session_state.resgates = []
if 'user' not in st.session_state:
    st.session_state.user = None
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'

# Dados do sistema
TURMAS = ['501', '502', '503', '504', '601', '602', '603', '604', '605', '606',
          '701', '702', '703', '704', '705', '706', '707', '708',
          '801', '802', '803', '804', '805', '806', '807',
          '901', '902', '903', '904', '905']

MATERIAIS = {
    'Celular': 5,
    'Tablet': 3,
    'Notebook': 3.5,
    'Monitor': 2.5,
    'Teclado': 4,
    'Mouse': 4.5,
    'Bateria': 2,
    'Carregador': 6,
    'Fone': 5.5,
    'Cabo': 6.5
}

CATEGORIAS = {
    'Direção': [
        {'nome': 'Brinde', 'pontos': 15},
        {'nome': 'Pizza', 'pontos': 30},
        {'nome': 'Lanche', 'pontos': 10}
    ],
    'Matemática': [{'nome': 'Professor 1', 'pontos': 3}],
    'Português': [{'nome': 'Professor 2', 'pontos': 3}],
    'Inglês': [{'nome': 'Professor 3', 'pontos': 3}],
    'Ed. Física': [{'nome': 'Professor 4', 'pontos': 3}],
    'Artes': [{'nome': 'Professor 5', 'pontos': 3}],
    'Ciências': [{'nome': 'Professor 6', 'pontos': 3}],
    'Geografia': [{'nome': 'Professor 7', 'pontos': 3}],
    'História': [{'nome': 'Professor 8', 'pontos': 3}]
}

ADMIN_PASSWORD = 'soadminpode'


# Funções auxiliares
def find_user(nome, turma):
    for user in st.session_state.usuarios:
        if user['nome'] == nome and user['turma'] == turma:
            return user
    return None


def update_user_points(user_id, points):
    for user in st.session_state.usuarios:
        if user['id'] == user_id:
            user['pontos'] += points
            if st.session_state.user and st.session_state.user['id'] == user_id:
                st.session_state.user['pontos'] += points
            break


def get_user_descartes(user_id):
    return [d for d in st.session_state.descartes if d['usuarioId'] == user_id]


def get_user_resgates(user_id):
    return [r for r in st.session_state.resgates if r['usuarioId'] == user_id]


# Telas do aplicativo
def home_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2 style='color: #667eea;'>Bem-vindo ao EcoEscola!</h2>
        <p style='font-size: 1.2em; margin: 30px 0;'>
            📱 Traga eletrônicos antigos<br>
            ⭐ Ganhe pontos<br>
            🎁 Troque por cupons
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Cadastrar", key="btn_cadastro", use_container_width=True):
            st.session_state.screen = 'cadastro'
            st.rerun()
    with col2:
        if st.button("🔑 Entrar", key="btn_login", use_container_width=True):
            st.session_state.screen = 'login'
            st.rerun()
    with col3:
        if st.button("⚙️ Admin", key="btn_admin", use_container_width=True):
            st.session_state.screen = 'admin_login'
            st.rerun()


def cadastro_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## 📝 Cadastro")

    nome = st.text_input("Nome Completo", key="cad_nome")
    turma = st.selectbox("Turma", ['Selecione...'] + TURMAS, key="cad_turma")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cadastrar", key="btn_do_cadastro", use_container_width=True):
            if not nome or turma == 'Selecione...':
                st.error("❌ Preencha todos os campos!")
            else:
                novo_user = {
                    'id': int(datetime.now().timestamp() * 1000),
                    'nome': nome,
                    'turma': turma,
                    'pontos': 0,
                    'categoriasCompradas': []
                }
                st.session_state.usuarios.append(novo_user)
                st.session_state.user = novo_user
                st.success("✅ Cadastro realizado!")
                st.session_state.screen = 'dashboard'
                st.rerun()
    with col2:
        if st.button("Voltar", key="btn_voltar_cad", use_container_width=True):
            st.session_state.screen = 'home'
            st.rerun()


def login_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## 🔑 Login")

    nome = st.text_input("Nome", key="login_nome")
    turma = st.selectbox("Turma", ['Selecione...'] + TURMAS, key="login_turma")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar", key="btn_do_login", use_container_width=True):
            if turma != 'Selecione...':
                user = find_user(nome, turma)
                if user:
                    st.session_state.user = user
                    st.success("✅ Login realizado!")
                    st.session_state.screen = 'dashboard'
                    st.rerun()
                else:
                    st.error("❌ Dados incorretos!")
    with col2:
        if st.button("Voltar", key="btn_voltar_login", use_container_width=True):
            st.session_state.screen = 'home'
            st.rerun()


def dashboard_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)

    # Botões de navegação
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📱 Cadastrar", key="btn_cadastrar_eletro", use_container_width=True):
            st.session_state.screen = 'cadastrar_eletro'
            st.rerun()
    with col2:
        if st.button("ℹ️ Cupons", key="btn_cupons", use_container_width=True):
            st.session_state.screen = 'cupons'
            st.rerun()
    with col3:
        if st.button("🎫 Meus Cupons", key="btn_resgates", use_container_width=True):
            st.session_state.screen = 'resgates'
            st.rerun()
    with col4:
        if st.button("🚪 Sair", key="btn_logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.screen = 'home'
            st.rerun()

    st.markdown(f"## 👋 Olá, {st.session_state.user['nome']}!")

    # Card de pontos
    st.markdown(f"""
    <div class='stat-card'>
        <p>Seus Pontos</p>
        <h1>{st.session_state.user['pontos']:.1f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📱 Seus Eletrônicos:")
    descartes = get_user_descartes(st.session_state.user['id'])[:10]

    if descartes:
        for d in descartes:
            card_class = 'card-ok' if d['status'] == 'Aprovado' else 'card-wait'
            status_icon = '✅' if d['status'] == 'Aprovado' else '⏳'
            st.markdown(f"""
            <div class='{card_class}'>
                <b>Número:</b> {d['numero']}<br>
                <b>Material:</b> {d['material']} ({d['quantidade']} un)<br>
                <b>Pontos:</b> {d['pontos']}<br>
                <b>Status:</b> {status_icon} {d['status']}<br>
                <small>{d['data']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum eletrônico cadastrado ainda")


def cadastrar_eletro_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## 📱 Cadastrar Eletrônico")

    material = st.selectbox("Material", list(MATERIAIS.keys()),
                            format_func=lambda x: f"{x} ({MATERIAIS[x]}pts)")
    quantidade = st.number_input("Quantidade", min_value=1, value=1)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cadastrar", key="btn_do_eletro", use_container_width=True):
            pontos = MATERIAIS[material] * quantidade
            descarte = {
                'id': int(datetime.now().timestamp() * 1000),
                'usuarioId': st.session_state.user['id'],
                'numero': f"DSC-{int(datetime.now().timestamp() * 1000)}",
                'material': material,
                'quantidade': quantidade,
                'pontos': pontos,
                'status': 'Pendente',
                'data': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            st.session_state.descartes.append(descarte)
            st.success(f"✅ Cadastrado! {pontos} pontos")
            st.session_state.screen = 'dashboard'
            st.rerun()
    with col2:
        if st.button("Voltar", key="btn_voltar_eletro", use_container_width=True):
            st.session_state.screen = 'dashboard'
            st.rerun()


def cupons_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## 🎁 Cupons Disponíveis")

    st.markdown(f"### Seus pontos: {st.session_state.user['pontos']:.1f}")

    categorias_disponiveis = [cat for cat in CATEGORIAS.keys()
                              if cat == 'Direção' or cat not in st.session_state.user.get('categoriasCompradas', [])]

    if 'categoria_selecionada' not in st.session_state:
        st.session_state.categoria_selecionada = None

    if st.session_state.categoria_selecionada:
        # Mostrar cupons da categoria
        cat = st.session_state.categoria_selecionada
        st.markdown(f"### 🎫 {cat}")

        for cupom in CATEGORIAS[cat]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class='card-wait'>
                    <b>{cupom['nome']}</b> - {cupom['pontos']} pts
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(f"Comprar", key=f"comprar_{cat}_{cupom['nome']}", use_container_width=True):
                    if cat != 'Direção' and cat in st.session_state.user.get('categoriasCompradas', []):
                        st.error("❌ Você já comprou cupom dessa categoria!")
                    elif st.session_state.user['pontos'] < cupom['pontos']:
                        st.error("❌ Pontos insuficientes!")
                    else:
                        # Comprar cupom
                        st.session_state.user['pontos'] -= cupom['pontos']
                        if 'categoriasCompradas' not in st.session_state.user:
                            st.session_state.user['categoriasCompradas'] = []
                        if cat != 'Direção':
                            st.session_state.user['categoriasCompradas'].append(cat)

                        # Criar resgate
                        codigo = f"CUP-{random.randint(1000, 9999)}"
                        resgate = {
                            'id': int(datetime.now().timestamp() * 1000),
                            'usuarioId': st.session_state.user['id'],
                            'categoria': cat,
                            'cupom': cupom['nome'],
                            'codigo': codigo,
                            'pontos': cupom['pontos'],
                            'status': 'Pendente',
                            'data': datetime.now().strftime('%d/%m/%Y %H:%M')
                        }
                        st.session_state.resgates.append(resgate)

                        # Atualizar usuário na lista
                        for u in st.session_state.usuarios:
                            if u['id'] == st.session_state.user['id']:
                                u['pontos'] = st.session_state.user['pontos']
                                u['categoriasCompradas'] = st.session_state.user['categoriasCompradas']

                        st.success(f"✅ Cupom {codigo} solicitado!")
                        st.session_state.categoria_selecionada = None
                        st.rerun()

        if st.button("⬅️ Voltar para Categorias", key="btn_voltar_cat"):
            st.session_state.categoria_selecionada = None
            st.rerun()
    else:
        # Mostrar categorias disponíveis
        cols = st.columns(3)
        for idx, cat in enumerate(categorias_disponiveis):
            with cols[idx % 3]:
                if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                    st.session_state.categoria_selecionada = cat
                    st.rerun()

    st.markdown("---")
    if st.button("🏠 Voltar ao Dashboard", key="btn_voltar_cupons", use_container_width=True):
        st.session_state.screen = 'dashboard'
        st.session_state.categoria_selecionada = None
        st.rerun()


def resgates_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## 🎫 Meus Cupons")

    resgates = get_user_resgates(st.session_state.user['id'])

    if resgates:
        for r in resgates:
            if r['status'] == 'Aprovado':
                card_class = 'card-ok'
                status_text = '✅ Aprovado'
            elif r['status'] == 'Recusado':
                card_class = 'card'
                status_text = '❌ Recusado'
            else:
                card_class = 'card-wait'
                status_text = '⏳ Pendente'

            st.markdown(f"""
            <div class='{card_class}'>
                <b>🎫 {r['categoria']} - {r['cupom']}</b><br>
                Código: <b style='font-size:24px'>{r['codigo']}</b><br>
                <b>Status:</b> {status_text}<br>
                <small>{r['data']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum cupom resgatado ainda")

    if st.button("Voltar", key="btn_voltar_resgates", use_container_width=True):
        st.session_state.screen = 'dashboard'
        st.rerun()


def admin_login_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## 🔒 Acesso Administrativo")

    senha = st.text_input("Senha", type="password", key="admin_senha")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar", key="btn_admin_entrar", use_container_width=True):
            if senha == ADMIN_PASSWORD:
                st.session_state.screen = 'admin'
                st.rerun()
            else:
                st.error("❌ Senha incorreta!")
    with col2:
        if st.button("Voltar", key="btn_voltar_admin_login", use_container_width=True):
            st.session_state.screen = 'home'
            st.rerun()


def admin_screen():
    st.markdown("<h1>♻️ EcoEscola</h1>", unsafe_allow_html=True)
    st.markdown("## ⚙️ Painel Administrativo")

    if st.button("🚪 Sair", key="btn_sair_admin"):
        st.session_state.screen = 'home'
        st.rerun()

    # Estatísticas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <p>Usuários</p>
            <h1>{len(st.session_state.usuarios)}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <p>Descartes</p>
            <h1>{len(st.session_state.descartes)}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        aprovados = len([d for d in st.session_state.descartes if d['status'] == 'Aprovado'])
        st.markdown(f"""
        <div class='stat-card'>
            <p>Aprovados</p>
            <h1>{aprovados}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        pendentes = len([r for r in st.session_state.resgates if r['status'] == 'Pendente'])
        st.markdown(f"""
        <div class='stat-card'>
            <p>Cupons Pendentes</p>
            <h1>{pendentes}</h1>
        </div>
        """, unsafe_allow_html=True)

    # Descartes Pendentes
    st.markdown("### ⏳ Descartes Pendentes")
    descartes_pend = [d for d in st.session_state.descartes if d['status'] == 'Pendente']

    if descartes_pend:
        for d in descartes_pend:
            user = next((u for u in st.session_state.usuarios if u['id'] == d['usuarioId']), None)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class='card-wait'>
                    <b>Número:</b> {d['numero']}<br>
                    <b>Aluno:</b> {user['nome'] if user else 'N/A'} ({user['turma'] if user else 'N/A'})<br>
                    <b>Material:</b> {d['material']} ({d['quantidade']} un)<br>
                    <b>Pontos:</b> {d['pontos']}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(f"✅ Aprovar", key=f"aprovar_desc_{d['id']}", use_container_width=True):
                    d['status'] = 'Aprovado'
                    update_user_points(d['usuarioId'], d['pontos'])

                    # Criar cupom automático
                    codigo = f"CUP-{random.randint(1000, 9999)}"
                    resgate = {
                        'id': int(datetime.now().timestamp() * 1000),
                        'usuarioId': d['usuarioId'],
                        'categoria': 'Descarte',
                        'cupom': f"Cupom de {d['pontos']} pts - {d['material']}",
                        'codigo': codigo,
                        'pontos': d['pontos'],
                        'status': 'Pendente',
                        'descarte_id': d['id'],
                        'data': datetime.now().strftime('%d/%m/%Y %H:%M')
                    }
                    st.session_state.resgates.append(resgate)
                    st.success(f"✅ Descarte aprovado! Cupom {codigo} criado!")
                    st.rerun()
    else:
        st.info("Nenhum descarte pendente")

    # Cupons Pendentes
    st.markdown("### 🎫 Cupons Pendentes")
    cupons_pend = [r for r in st.session_state.resgates if r['status'] == 'Pendente']

    if cupons_pend:
        for r in cupons_pend:
            user = next((u for u in st.session_state.usuarios if u['id'] == r['usuarioId']), None)
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"""
                <div class='card-wait'>
                    <b>Código:</b> {r['codigo']}<br>
                    <b>Aluno:</b> {user['nome'] if user else 'N/A'} ({user['turma'] if user else 'N/A'})<br>
                    <b>Cupom:</b> {r['categoria']} - {r['cupom']}<br>
                    <b>Pontos:</b> {r['pontos']}<br>
                    <small>{r['data']}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(f"✅ Aprovar", key=f"aprovar_cupom_{r['id']}", use_container_width=True):
                    r['status'] = 'Aprovado'
                    st.success("✅ Cupom aprovado!")
                    st.rerun()
            with col3:
                if st.button(f"❌ Recusar", key=f"recusar_cupom_{r['id']}", use_container_width=True):
                    r['status'] = 'Recusado'
                    # Devolver pontos
                    update_user_points(r['usuarioId'], r['pontos'])
                    st.warning("⚠️ Cupom recusado! Pontos devolvidos.")
                    st.rerun()
    else:
        st.info("Nenhum cupom pendente")


# Roteamento principal
def main():
    if st.session_state.screen == 'home':
        home_screen()
    elif st.session_state.screen == 'cadastro':
        cadastro_screen()
    elif st.session_state.screen == 'login':
        login_screen()
    elif st.session_state.screen == 'dashboard':
        if st.session_state.user:
            dashboard_screen()
        else:
            st.session_state.screen = 'home'
            st.rerun()
    elif st.session_state.screen == 'cadastrar_eletro':
        cadastrar_eletro_screen()
    elif st.session_state.screen == 'cupons':
        cupons_screen()
    elif st.session_state.screen == 'resgates':
        resgates_screen()
    elif st.session_state.screen == 'admin_login':
        admin_login_screen()
    elif st.session_state.screen == 'admin':
        admin_screen()


if __name__ == "__main__":
    main()