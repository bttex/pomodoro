import time
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Pomodoro Timer", layout="centered", page_icon=":tomato:")

# Inicializando estados
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
    st.session_state.time_left = 25 * 60  # Tempo padrão de 25 minutos
    st.session_state.break_time = 5 * 60  # Pausa padrão de 5 minutos
    st.session_state.tasks = []  # Lista de tarefas
if "current_task" not in st.session_state:
    st.session_state.current_task = None

# Função para formatar o tempo
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# CSS para o tema escuro
def inject_css():
    st.markdown(
        """
        <style>
            body {background-color: #1D1D1D; color: #FFFFFF;}
            h1 {color: #E74C3C;}  /* Vermelho Pomodoro */
        </style>
        """,
        unsafe_allow_html=True,
    )

# Aplica o tema escuro
inject_css()

# Seleção de idioma
language = st.radio("Escolha o idioma / Choose the language", ["Português", "English"])

# Dicionário de traduções
translations = {
    "title": {"Português": "Pomodoro Timer", "English": "Pomodoro Timer"},
    "work_time": {"Português": "Tempo de trabalho (minutos)", "English": "Work time (minutes)"},
    "break_time": {"Português": "Tempo de pausa (minutos)", "English": "Break time (minutes)"},
    "save_button": {"Português": "Salvar", "English": "Save"},
    "save_success": {"Português": "Configurações salvas com sucesso!", "English": "Settings saved successfully!"},
    "tasks_subheader": {"Português": "Tarefas", "English": "Tasks"},
    "new_task": {"Português": "Nova tarefa", "English": "New task"},
    "add_task": {"Português": "Adicionar tarefa", "English": "Add task"},
    "add_success": {"Português": "Tarefa adicionada!", "English": "Task added!"},
    "add_error": {"Português": "Digite uma tarefa antes de adicionar!", "English": "Please enter a task before adding!"},
    "no_tasks": {"Português": "Nenhuma tarefa adicionada ainda.", "English": "No tasks added yet."},
    "current_task": {"Português": "Tarefa atual: {}", "English": "Current task: {}"},
    "start_button": {"Português": "Iniciar", "English": "Start"},
    "pause_button": {"Português": "Pausar", "English": "Pause"},
    "restart_button": {"Português": "Reiniciar", "English": "Restart"},
    "cycle_end": {"Português": "Fim do ciclo! Hora de descansar.", "English": "Cycle complete! Time to rest."},
}

# Título
st.title(translations["title"][language])

# Configurações de tempo
st.sidebar.subheader(translations["tasks_subheader"][language])
work_time = st.sidebar.number_input(translations["work_time"][language], min_value=1, max_value=60, value=25)
break_time = st.sidebar.number_input(translations["break_time"][language], min_value=1, max_value=30, value=5)
if st.sidebar.button(translations["save_button"][language]):
    st.session_state.time_left = work_time * 60
    st.session_state.break_time = break_time * 60
    st.success(translations["save_success"][language])

# Adicionar tarefas
new_task = st.sidebar.text_input(translations["new_task"][language])
if st.sidebar.button(translations["add_task"][language]):
    if new_task:
        st.session_state.tasks.append(new_task)
        st.session_state.current_task = new_task if st.session_state.current_task is None else st.session_state.current_task
        st.sidebar.success(translations["add_success"][language])
    else:
        st.sidebar.error(translations["add_error"][language])

# Exibir tarefas
st.subheader(translations["tasks_subheader"][language])
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([8, 2])
        col1.write(f"{i + 1}. {task}")
        if col2.button("Remover", key=f"remove_{i}"):
            st.session_state.tasks.pop(i)
            if st.session_state.current_task == task:
                st.session_state.current_task = st.session_state.tasks[0] if st.session_state.tasks else None
            st.rerun()
else:
    st.info(translations["no_tasks"][language])

# Exibir tarefa atual
if st.session_state.current_task:
    st.subheader(translations["current_task"][language].format(st.session_state.current_task))

# Cronômetro
time_display = st.empty()
time_display.markdown(
    f"<h1>{format_time(st.session_state.time_left)}</h1>",
    unsafe_allow_html=True,
)

# Controles do cronômetro
col1, col2, col3 = st.columns(3)
if col1.button(translations["start_button"][language]):
    st.session_state.timer_running = True
if col2.button(translations["pause_button"][language]):
    st.session_state.timer_running = False
if col3.button(translations["restart_button"][language]):
    st.session_state.timer_running = False
    st.session_state.time_left = work_time * 60

# Atualizar o cronômetro
if st.session_state.timer_running:
    while st.session_state.time_left > 0 and st.session_state.timer_running:
        st.session_state.time_left -= 1
        time_display.markdown(
            f"<h1>{format_time(st.session_state.time_left)}</h1>",
            unsafe_allow_html=True,
        )
        time.sleep(1)
        st.rerun()

# Mensagens ao finalizar
if st.session_state.time_left == 0 and st.session_state.timer_running:
    st.session_state.timer_running = False
    st.success(translations["cycle_end"][language])
