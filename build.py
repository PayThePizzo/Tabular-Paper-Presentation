#!/usr/bin/env python3
import os
import glob
import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def build_presentation():
    print("🚀 Inizio compilazione della presentazione...")

    # 1. Carica la configurazione del tema
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 2. Carica tutte le slide dalla cartella content/ ordinate per ID
    slide_files = sorted(glob.glob("content/*.yaml"))
    slides = []
    for filepath in slide_files:
        with open(filepath, "r", encoding="utf-8") as f:
            slide_data = yaml.safe_load(f)
            # Salta l'eventuale copertina se gestita a parte
            if slide_data.get("slide_id") != "00":
                slides.append(slide_data)

    # 3. Leggi il foglio di stile CSS
    css_path = os.path.join("static", "style.css")
    css_content = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    # 4. Inizializza l'environment Jinja2
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("base.html")

    # 5. Renderizza l'HTML finale
    html_out = template.render(
        config=config,
        slides=slides,
        css_content=css_content
    )

    # Salva il file HTML intermedio per debug
    with open("build_output.html", "w", encoding="utf-8") as f:
        f.write(html_out)
    print("✓ HTML generato: build_output.html")

    # 6. Compila il PDF tramite WeasyPrint
    output_pdf = "Tabular_Presentation.pdf"
    HTML("build_output.html").write_pdf(output_pdf)
    print(f"🎉 PDF generato con successo: {output_pdf}")

if __name__ == "__main__":
    build_presentation()