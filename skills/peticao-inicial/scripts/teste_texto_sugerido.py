"""Teste de texto_sugerido.py. Rodar: python3 teste_texto_sugerido.py"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texto_sugerido import desembrulhar, linhas


def run(texto, **extra):
    return {"textRun": {"content": texto, **extra}}


doc = {
    "revisionId": "r1",
    "tabs": [{"documentTab": {"body": {"content": [
        {"endIndex": 1, "sectionBreak": {}},
        {"startIndex": 1, "endIndex": 20, "paragraph": {"elements": [run("Linha um do teste.\n")]}},
        {"startIndex": 20, "endIndex": 82, "paragraph": {"elements": [
            run("Horas extras com "),
            run("adicional de 90%", suggestedInsertionIds=["s1"]),
            run("adicional de 50%", suggestedDeletionIds=["s1"]),
            run(" e reflexos.\n"),
        ]}},
        {"startIndex": 82, "endIndex": 100, "paragraph": {"elements": [
            run("Nota a retirar.\n", suggestedDeletionIds=["s2"]),
        ]}},
        {"startIndex": 100, "endIndex": 130, "table": {"tableRows": [{"tableCells": [
            {"content": [{"startIndex": 103, "endIndex": 110, "paragraph": {"elements": [run("Célula\n")]}}]},
        ]}]}},
    ]}}}],
}

esperado = [
    "[1,20] Linha um do teste.",
    "[20,82] Horas extras com adicional de 90% e reflexos.",
    "[103,110] Célula",
]
assert list(linhas(doc)) == esperado, list(linhas(doc))

# Os envelopes que o app usa ao salvar o resultado em disco.
cru = json.dumps({"content": doc})
salvo = json.dumps([{"type": "text", "text": cru}])
assert list(linhas(desembrulhar(salvo))) == esperado

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    f.write(salvo)
saida = os.popen(f'python3 "{os.path.dirname(os.path.abspath(__file__))}/texto_sugerido.py" "{f.name}"').read()
os.unlink(f.name)
assert saida.splitlines() == esperado, saida
print("ok")
