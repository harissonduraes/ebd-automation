import tkinter as tk
from tkinter import scrolledtext, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configurações da Automação ---
URL = "https://www.igrejacristamaranata.org.br/ebd/participacoes/"

# --- Variáveis Globais para os Widgets Tkinter (serão definidas abaixo) ---
# Declaramos aqui para que a função run_automation possa referenciá-las
cpf_input_area = None
texto_participacao_area = None
log_area = None

def log_message(message):
    """Função para adicionar mensagens ao log na interface Tkinter."""
    if log_area: # Verifica se log_area já foi inicializado
        log_area.config(state='normal')
        log_area.insert(tk.END, message + "\n")
        log_area.see(tk.END) # Rola para o final da área de texto
        log_area.config(state='disabled')
    else:
        print(f"LOG (GUI não inicializada): {message}") # Fallback para depuração

def run_automation():
    """Função principal que executa a automação Selenium."""
    log_area.delete(1.0, tk.END) # Limpa o log anterior
    # log_message("Iniciando automação web...")
    # log_message("Certifique-se de que o WebDriver (ex: ChromeDriver) está no seu PATH.")

    # Obter CPFs da área de texto do Tkinter
    cpfs_raw = cpf_input_area.get("1.0", tk.END).strip()
    if not cpfs_raw:
        messagebox.showwarning("Aviso", "Por favor, insira os CPFs na caixa de texto.")
        log_message("Nenhum CPF fornecido. Automação cancelada.")
        return

    # Dividir os CPFs por linha e remover linhas vazias
    cpfs_para_automacao = [cpf.strip() for cpf in cpfs_raw.split('\n') if cpf.strip()]

    if not cpfs_para_automacao:
        messagebox.showwarning("Aviso", "Nenhum CPF válido encontrado na caixa de texto.")
        log_message("Nenhum CPF válido encontrado. Automação cancelada.")
        return

    # Obter o texto de participação da área de texto do Tkinter
    texto_participacao_gui = texto_participacao_area.get("1.0", tk.END).strip()
    if not texto_participacao_gui:
        messagebox.showwarning("Aviso", "Por favor, insira o texto de participação.")
        log_message("Nenhum texto de participação fornecido. Automação cancelada.")
        return

    # driver = None
    # # Inicializa o WebDriver (usando Chrome como exemplo).
    # # Se o chromedriver não estiver no PATH, especifique o caminho completo:
    # # driver = webdriver.Chrome(executable_path="/caminho/para/seu/chromedriver")
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # log_message("Navegando para a URL: " + URL)
    # driver.get(URL)

    # # Configura um tempo de espera explícito para elementos carregarem
    # wait = WebDriverWait(driver, 20) # Espera até 20 segundos
    

    # Loop para processar cada CPF na lista
    for i, cpf in enumerate(cpfs_para_automacao):
        driver = None
        # Inicializa o WebDriver (usando Chrome como exemplo).
        # Se o chromedriver não estiver no PATH, especifique o caminho completo:
        # driver = webdriver.Chrome(executable_path="/caminho/para/seu/chromedriver")
        driver = webdriver.Chrome()
        driver.maximize_window()
        # log_message("Navegando para a URL: " + URL)
        driver.get(URL)

        # Configura um tempo de espera explícito para elementos carregarem
        wait = WebDriverWait(driver, 20) # Espera até 20 segundos

        driver.execute_script("document.body.style.zoom='35%'")
        # log_message(f"\n--- Processando CPF {i+1}/{len(cpfs_para_automacao)}: {cpf} ---")

        # Recarrega a página para garantir um formulário limpo para cada CPF
        driver.get(URL)
        # log_message("Página recarregada para o próximo CPF.")
        driver.execute_script("document.body.style.zoom='35%'")

        cpf_input = wait.until(EC.presence_of_element_located((By.NAME, "icm_member_cpf"))) # SUBSTITUA 'cpf_field_id' pelo ID real

        cpf_input.clear()
        cpf_input.send_keys(cpf)
        # cpf_input.send_keys(Keys.ENTER)
        # log_message("CPF digitado e Enter pressionado. Aguardando carregamento de dados...")
        time.sleep(5) # Pequena pausa para a página reagir e carregar dados
        
        # funcao_input_clickable = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[3]/div[4]/div[1]/div/div[1]/input")
        # funcao_input_clickable.click()

        funcao_input_clickable = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[3]/div[4]/div[1]/div/div[1]/input")))
        funcao_input_clickable.click()

        # trabalho_select_element = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[3]/div[4]/div[1]/div/div[2]/div/div[4]")
        # trabalho_select_element.click()

        trabalho_select_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[3]/div[4]/div[1]/div/div[2]/div/div[4]"))) # SUBSTITUA 'trabalho_select_id'
        trabalho_select_element.click()

        # log_message("Opção 'Membro' selecionada para Função.")

        trabalho_select_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[3]/div[4]/div[2]/div/div[1]/input"))) # SUBSTITUA 'trabalho_select_id'
        trabalho_select_element.click()

        trabalho_select_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[3]/div[4]/div[2]/div/div[2]/div/div[1]")))
        trabalho_select_element.click()

        # log_message("Trabalho 'Participação individual' selecionado.")

        # radio_participacao = driver.find_element((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[5]/div/div[1]/input[2]"))
        # radio_participacao.is_selected()
        # print("radio" + radio_participacao)

        # --- Passo 4: Clicar na bolinha de "Participação" (Radio Button) ---
        try:
            # Encontra o radio button com name='icm_member_categoria' e value='3'
            radio_participacao = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='icm_member_categoria' and @value='2']")))
            
            # Verifica se já está selecionado para evitar cliques desnecessários
            if not radio_participacao.is_selected():
                radio_participacao.click()
            # log_message("Radio button 'Participação' clicado.")
        except Exception as e:
            log_message(f"ERRO: Não foi possível clicar no radio button 'Participação'. Verifique o XPath. Erro: {e}")
            continue

        box_input = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/div[6]/div/div/div/label/input")))
        box_input.click()

        try:
            # 1. Localizar o elemento div com as classes ql-editor e ql-blank
            # Usaremos um seletor CSS para ser conciso e eficaz.
            # O seletor 'div.ql-editor.ql-blank' procura por um div que tenha AMBAS as classes.
            print("Localizando o elemento div.ql-editor.ql-blank...")
            editor_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor.ql-blank")))
            print("Elemento div localizado.")

            # 2. Inserir texto no editor (se ainda não o fez)
            # Geralmente, ao inserir texto, a classe ql-blank é removida automaticamente.
            # Se você já inseriu texto e a classe ainda está lá, talvez haja um problema.
            # Se não inseriu, esta é a forma de fazê-lo:
            editor_div.clear() # Limpa o conteúdo existente (se houver)
            editor_div.send_keys(texto_participacao_gui)
            print(f"Texto inserido no editor: '{texto_participacao_gui}'")
            time.sleep(1) # Pequena pausa para o JS do editor reagir

            # 3. Verificar se a classe ql-blank ainda existe
            # Se sim, remova-a manualmente via JavaScript.
            if "ql-blank" in editor_div.get_attribute("class"):
                print("A classe 'ql-blank' ainda está presente. Removendo via JavaScript...")
                # Executa JavaScript para remover a classe 'ql-blank'
                # arguments[0] refere-se ao 'editor_div' que é passado como argumento.
                driver.execute_script("arguments[0].classList.remove('ql-blank');", editor_div)
                print("Classe 'ql-blank' removida.")
            else:
                print("A classe 'ql-blank' já foi removida automaticamente.")

            time.sleep(2) # Pausa para visualização

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            # driver.save_screenshot("erro_ql_editor.png") # Para depuraçãoepuração

        input_salvar = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[2]/article/div/div/div/div/div/div/div/div/div/button")))
        input_salvar.click()

        time.sleep(2) # Pausa para visualização

        if driver:
            log_message(f"CPF {cpf} enviado")
            driver.quit()

# --- Configuração da Interface Gráfica Tkinter ---
root = tk.Tk()
root.title("Automação EBD - Igreja Cristã Maranata")
root.geometry("800x750") # Aumenta o tamanho da janela para acomodar os novos campos

# Frame para os controles
control_frame = tk.Frame(root, padx=10, pady=10)
control_frame.pack(pady=10)

# Botão para iniciar a automação
start_button = tk.Button(control_frame, text="Iniciar Automação", command=run_automation, font=("Arial", 14, "bold"), bg="green", fg="white")
start_button.pack(side=tk.LEFT, padx=5)

# Campo para entrada de CPFs
cpf_label = tk.Label(root, text="Insira os CPFs (um por linha):", font=("Arial", 12, "bold"))
cpf_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

# ATENÇÃO: Definindo as variáveis globais aqui
cpf_input_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=8, font=("Courier New", 10), bg="#f0f0f0", fg="#333")
cpf_input_area.pack(padx=10, pady=5)

# Adicione CPFs de exemplo para facilitar o teste
# cpf_input_area.insert(tk.END, """111.111.111-11
# 222.222.222-22
# 333.333.333-33
# """)

# Campo para entrada do texto de participação
texto_participacao_label = tk.Label(root, text="Texto da Participação:", font=("Arial", 12, "bold"))
texto_participacao_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

# ATENÇÃO: Definindo as variáveis globais aqui
texto_participacao_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=12, font=("Courier New", 10), bg="#f0f0f0", fg="#333")
texto_participacao_area.pack(padx=10, pady=5)

# Define um texto padrão para o campo de participação
# texto_participacao_area.insert(tk.END, "Participação em aula da EBD conforme solicitação.")


# Área de log
log_label = tk.Label(root, text="Log de Automação:", font=("Arial", 12, "bold"))
log_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

# ATENÇÃO: Definindo as variáveis globais aqui
log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, font=("Courier New", 10), bg="#f0f0f0", fg="#333")
log_area.pack(padx=10, pady=5)

log_area.config(state='disabled')

root.mainloop()