import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import pygame
import openai

# Inicialize o reconhecedor e o motor de síntese de fala
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Nome do assistente
assistente_nome = "atena"

# Inicialize o mixer do pygame
pygame.mixer.init()

# Configurar a chave da API do OpenAI
openai.api_key = "your_openai_api_key"

def listar_vozes():
    """Lista todas as vozes disponíveis no pyttsx3."""
    voices = tts_engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name}")

def escolher_voz(index):
    """Escolhe uma voz com base no índice fornecido."""
    voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', voices[index].id)

def speak(texto):
    """Converte texto em fala."""
    tts_engine.say(texto)
    tts_engine.runAndWait()

def listen():
    """Escuta e reconhece o comando de voz do usuário."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Ouvindo...")
        audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("Desculpe, não entendi isso.")
            return None
        except sr.RequestError:
            print("Desculpe, meu serviço de reconhecimento de fala está fora do ar.")
            return None

def criar_lista_de_tarefas():
    """Cria uma lista de tarefas a partir de comandos de voz."""
    lista_de_tarefas = []
    speak("O que você gostaria de adicionar à sua lista de tarefas?")
    while True:
        item = listen()
        if item:
            if "parar" in item or "é só" in item:
                break
            lista_de_tarefas.append(item)
            speak(f"Adicionado {item} à sua lista de tarefas.")
        else:
            speak("Por favor, repita isso.")
    return lista_de_tarefas

def pesquisar_na_web(consulta):
    """Realiza uma pesquisa na web usando o Google."""
    url = f"https://www.google.com/search?q={consulta}"
    webbrowser.open(url)
    speak(f"Aqui estão os resultados para {consulta}")

def pesquisar_no_youtube(consulta):
    """Realiza uma pesquisa por vídeos no YouTube."""
    url = f"https://www.youtube.com/results?search_query={consulta}"
    webbrowser.open(url)
    speak(f"Aqui estão os resultados para {consulta} no YouTube")

def definir_lembrete(tempo_para_lembrete, mensagem):
    """Define um lembrete para um tempo específico."""
    speak(f"Definindo um lembrete para {mensagem} em {tempo_para_lembrete} segundos.")
    try:
        tempo_para_lembrete = int(tempo_para_lembrete)
        time.sleep(tempo_para_lembrete)
        speak(f"Lembrete: {mensagem}")
    except ValueError:
        speak("O tempo deve ser um número válido de segundos.")

def listar_arquivos():
    """Lista os arquivos no diretório atual."""
    arquivos = os.listdir('.')
    speak("Os arquivos no diretório atual são: " + ', '.join(arquivos))

def tocar_musica(caminho):
    """Toca uma música a partir de um arquivo local."""
    if os.path.isfile(caminho):
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()
        speak(f"Tocando música {os.path.basename(caminho)}")
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    else:
        speak("Desculpe, não consegui encontrar o arquivo de música.")

def sair():
    """Encerra a execução do assistente de voz."""
    speak("Até logo!")
    exit()

def consultar_openai_gpt3(query):
    """Consulta a API do OpenAI GPT-3.5."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": query}
        ]
    )
    return response['choices'][0]['message']['content']

def responder_pergunta():
    """Obtém uma resposta para a pergunta do usuário usando a API do OpenAI GPT-3.5."""
    speak("Qual é a sua pergunta?")
    pergunta = listen()
    if pergunta:
        resposta = consultar_openai_gpt3(pergunta)
        speak(resposta)
    else:
        speak("Desculpe, não entendi a pergunta.")

def main():
    """Função principal que gerencia os comandos do usuário."""
    speak("Olá! Como posso ajudar você hoje?")
    while True:
        comando = listen()
        if comando and assistente_nome in comando:
            comando = comando.replace(assistente_nome, "").strip()
            if "criar uma lista de tarefas" in comando:
                lista_de_tarefas = criar_lista_de_tarefas()
                speak(f"Sua lista de tarefas: {', '.join(lista_de_tarefas)}")
            elif "pesquisar por" in comando:
                consulta = comando.replace("pesquisar por", "").strip()
                pesquisar_na_web(consulta)
            elif "pesquisar no youtube por" in comando:
                consulta = comando.replace("pesquisar no youtube por", "").strip()
                pesquisar_no_youtube(consulta)
            elif "definir um lembrete" in comando:
                speak("Qual é a mensagem do lembrete?")
                mensagem = listen()
                speak("Em quantos segundos?")
                segundos = listen()
                definir_lembrete(segundos, mensagem)
            elif "listar arquivos" in comando:
                listar_arquivos()
            elif "tocar música" in comando:
                speak("Qual é o caminho do arquivo de música?")
                caminho = listen()
                tocar_musica(caminho)
            elif "parar" in comando or "sair" in comando:
                sair()
            elif "responder pergunta" in comando:
                responder_pergunta()
            else:
                speak("Desculpe, não entendi esse comando.")
        else:
            speak("Por favor, repita isso.")

if __name__ == "__main__":
    listar_vozes()
    # Peça ao usuário para escolher uma voz ao iniciar o programa
    speak("Por favor, escolha uma voz pelo número. Diga o número da voz que deseja usar.")
    voice_index = listen()
    if voice_index and voice_index.isdigit():
        escolher_voz(int(voice_index))
    main()