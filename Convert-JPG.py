import os
import shutil
import sys
from pathlib import Path
from PIL import Image

# Ativar o prg através do menu de contexto no NEMO.
# Colocar o script.sh na pasta:
# diretorio="/home/rodrigo/.local/share/nemo/scripts"

print("Script iniciado!")
print(f"Python executado: {sys.version}")
print(f"Pillow versão: {Image.__version__}")


def converter_extensoes_para_minusculas(pasta):
    for arquivo in pasta.iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix
            nome_base = arquivo.stem
            extensao_min = extensao.lower()

            if extensao != extensao_min:
                novo_nome = arquivo.with_name(f"{nome_base}{extensao_min}")
                arquivo.rename(novo_nome)
                print(f"Renomeado: {arquivo} -> {novo_nome}")

def gerar_nome_unico(arquivo):
    contador = 1
    novo_nome = arquivo
    while novo_nome.exists():
        novo_nome = arquivo.with_name(f"{arquivo.stem}_cv_{contador}.jpg")
        contador += 1
    return novo_nome

def processar_arquivos(pasta):
    lixo_pasta = pasta / "Lixo-Conversão-JPG"
    lixo_pasta.mkdir(exist_ok=True)
    print(f"Pasta criada: {lixo_pasta}")

    for imagem in pasta.iterdir():
        if imagem.is_file():
            extensao = imagem.suffix.lower()
            nome_base = imagem.stem
            nova_extensao = ".jpg"

            # Adicionar verificação para ignorar tipos não suportados
            if extensao not in [".jpeg", ".png", ".heic", ".webp", ".jpg"]:
                print(f"Ignorando arquivo não suportado: {imagem}")
                continue

            if extensao == ".jpg":
                print(f"Ignorando arquivo já no formato .jpg: {imagem}")
            elif extensao in [".jpeg", ".png", ".heic", ".webp"]:
                novo_nome = pasta / f"{nome_base}{nova_extensao}"
                if novo_nome.exists():
                    novo_nome = gerar_nome_unico(novo_nome)

                try:
                    with Image.open(imagem) as img:
                        img.convert("RGB").save(novo_nome, "JPEG")
                    print(f"Convertido: {imagem} -> {novo_nome}")
                    shutil.move(str(imagem), lixo_pasta / imagem.name)
                    print(f"Movido para Lixo-Conversão-JPG: {imagem}")
                except Exception as e:
                    print(f"Erro ao converter {imagem}: {e}")

def main():
    # Diretório passado como argumento ou diretório atual
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    if not pasta.is_dir():
        print(f"Erro: {pasta} não é um diretório válido.")
        sys.exit(1)

    # Verifica dependência do Pillow
    try:
        import PIL
    except ImportError:
        print("Erro: O Pillow não está instalado. Instale com 'pip install pillow'")
        sys.exit(1)

    # Etapas do script
    print("Convertendo extensões para minúsculas...")
    converter_extensoes_para_minusculas(pasta)

    print("Processando arquivos...")
    processar_arquivos(pasta)

    print(f"Conversão finalizada. Arquivos originais movidos para {pasta / 'Lixo-Conversão-JPG'}.")

if __name__ == "__main__":
    main()