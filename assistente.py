from openai import OpenAI
import os
import speech_recognition as sr
from dotenv import load_dotenv


class Assistant:
    def __init__(self):
        try:
            load_dotenv()
            self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            self.user_language = None
        except Exception as e:
            print(f"Erro ao carregar as variáveis de ambiente: {e}")
            exit()

    def iniciar_interacao(self):
        try:
            self.solicitar_idioma()

            while True:
                entrada = self.ouvir_entrada()

                if entrada:
                    resposta_gpt3 = self.obter_resposta_gpt3(entrada)

                    if "não entendi" in resposta_gpt3.lower():
                        print("Assistente: Desculpe, não entendi. Pode me explicar de outra forma?")
                        continue
                    else:
                        print("Assistente:", resposta_gpt3)
                        resposta_traduzida = self.traduzir_para_idioma_usuario(resposta_gpt3)
                        self.reproduzir_resposta(resposta_traduzida)

        except KeyboardInterrupt:
            print("Interação encerrada.")

    def obter_resposta_gpt3(self, entrada):
        max_tokens = 30
        resposta = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Você está aprendendo " + self.user_language + "."},
                      {"role": "user", "content": entrada}],
            max_tokens=max_tokens
        )

        try:
            resposta_texto = resposta.choices[0].message.content.strip()
            return resposta_texto
        except (KeyError, TypeError, IndexError):
            print("Erro ao processar a resposta do modelo.")
            return "Desculpe, não consegui gerar uma resposta neste momento."

    def traduzir_para_idioma_usuario(self, texto):
        # Você pode usar uma API ou biblioteca de tradução para traduzir o texto para o idioma do usuário
        # Para simplificar, vamos assumir uma função básica de tradução para fins de demonstração.
        # Em um cenário real, você pode querer usar uma API de tradução dedicada.
        traducao = f"Tradução para {self.user_language}: {texto}"
        return traducao

    def solicitar_idioma(self):
        print("Assistente: Olá! Qual idioma você gostaria de aprender?")
        while True:
            entrada = self.ouvir_entrada()

            if entrada:
                # Você pode adicionar lógica aqui para detectar e definir o idioma preferido do usuário
                self.user_language = entrada.lower()  # Assumindo que o usuário menciona o idioma que deseja aprender
                print(f"Assistente: Ótimo! Vamos começar a aprender {self.user_language.capitalize()}. qual fraze quer aprender hoje?")
                break
    def reproduzir_resposta(self, resposta):
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=resposta,
            )
            audio_content = response.content

            with open("output.mp3", "wb") as f:
                f.write(audio_content)

            # Código específico do sistema para reprodução de áudio
            if os.name == 'posix':  # macOS
                os.system('open output.mp3')
            elif os.name == 'nt':   # Windows
                os.system('start output.mp3')
            else:
                print("Sistema operacional não suportado para reprodução de áudio.")

        except Exception as e:
            print(f"Erro ao reproduzir a resposta: {e}")        

    def ouvir_entrada(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Ajustando para o ruído ambiente. Aguarde alguns segundos...")
            recognizer.adjust_for_ambient_noise(source, duration=5)

            print("Diga algo:")
            audio = recognizer.listen(source, phrase_time_limit=10)

        try:
            entrada_texto = recognizer.recognize_google(audio, language='pt-BR')
            print("Você disse:", entrada_texto)
            return entrada_texto
        except sr.UnknownValueError:
            print("Não foi possível entender a entrada.")
            return None

        
    def traduzir_para_idioma_usuario(self, texto):
        # Você pode usar uma API ou biblioteca de tradução para traduzir o texto para o idioma do usuário
        # Para simplificar, vamos assumir uma função básica de tradução para fins de demonstração.
        # Em um cenário real, você pode querer usar uma API de tradução dedicada.
        traducao = f"Tradução para {self.user_language}: {texto}"
        return traducao

if __name__ == "__main__":
    assistente = Assistant()
    assistente.iniciar_interacao()
