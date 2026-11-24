"""Texto de um Google Doc como fica se todas as sugestões forem aceitas.

Uso:
    python3 texto_sugerido.py <doc.json>

<doc.json> é o resultado do read_doc (conector Google Docs), cru ou como o app
salvou em disco. Imprime um parágrafo por linha:

    [início,fim] texto

[início,fim] são os índices do parágrafo no Doc de hoje (com as sugestões
pendentes dentro), para usar em insertText e deleteContentRange. O texto é o
proposto: trecho com exclusão sugerida sai, trecho com inserção sugerida entra.
"""
import json
import sys


def desembrulhar(x):
    """Tira os envelopes que o app põe em volta do JSON do documento."""
    while True:
        if isinstance(x, str):
            x = json.loads(x)
        elif isinstance(x, list) and x and isinstance(x[0], dict) and "text" in x[0]:
            x = x[0]["text"]
        elif isinstance(x, dict) and "content" in x and "body" not in x and "tabs" not in x:
            x = x["content"]
        else:
            return x


def blocos(doc):
    if doc.get("tabs"):
        return doc["tabs"][0]["documentTab"]["body"]["content"]
    return doc["body"]["content"]


def paragrafos(conteudo):
    for el in conteudo:
        if "paragraph" in el:
            yield el
        elif "table" in el:
            for linha in el["table"]["tableRows"]:
                for celula in linha["tableCells"]:
                    yield from paragrafos(celula["content"])
        elif "tableOfContents" in el:
            yield from paragrafos(el["tableOfContents"]["content"])


def linhas(doc):
    for p in paragrafos(blocos(doc)):
        partes, apagado = [], False
        for e in p["paragraph"]["elements"]:
            run = e.get("textRun")
            if not run:
                continue
            if run.get("suggestedDeletionIds"):
                apagado = True
                continue
            partes.append(run["content"])
        texto = "".join(partes).rstrip("\n")
        if apagado and not texto.strip():
            continue  # parágrafo inteiro com exclusão sugerida
        yield f"[{p['startIndex']},{p['endIndex']}] {texto}"


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        doc = desembrulhar(f.read())
    for linha in linhas(doc):
        print(linha)
