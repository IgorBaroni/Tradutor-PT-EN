from flask import Flask, request, render_template, redirect, url_for
from deep_translator import GoogleTranslator
import speech_recognition as sr

app = Flask(__name__)

def Traduzir(txt):
    tradutor = GoogleTranslator(source="pt", target="en")
    traducao = tradutor.translate(txt)
    return traducao

def gravarVoz():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic)
        audio = rec.listen(mic)
        fala = rec.recognize_google(audio, language="pt-BR")
        fala_traduzida = Traduzir(fala)
        return fala, fala_traduzida

@app.route("/")
def iniciar():
    return redirect(url_for("homepage", ft='true'))

@app.route("/voice")
def voice():
    return redirect(url_for("homepage", ft='false'))

@app.route("/tradutor", methods=["GET", "POST"])
def homepage():
    ft_param = request.args.get('ft', 'true')
    ft_bool = ft_param.lower()
    if request.method == "POST":
        texto = request.form.get("input-text")
        texto_traduzido = Traduzir(texto)
        return render_template("index.html", input=texto, output=texto_traduzido)
    if request.method == "GET":
        if ft_bool == 'true':
            fala, fala_traduzida = "", ""
        if ft_bool == 'false':
            fala, fala_traduzida = gravarVoz()
        return render_template("index.html", input=fala, output=fala_traduzida)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
