"""Teste rápido do gerar_docx.py. Rode: uv run --with python-docx --with pillow python3 teste_gerar_docx.py"""
import os
import tempfile

from docx import Document
from docx.oxml.ns import qn

from gerar_docx import gerar

with tempfile.TemporaryDirectory() as d:
    modelo, html, saida = (os.path.join(d, n) for n in ("m.docx", "p.html", "s.docx"))
    m = Document()
    for papel in ("corpo", "secao", "item", "nota"):
        m.add_paragraph("{{%s}}" % papel)
    m.save(modelo)
    open(html, "w", encoding="utf-8").write(
        "<h2>4.1. DAS HORAS EXTRAS</h2>"
        "<p>Texto com <b>negrito</b> e&nbsp;&nbsp;espaço.</p>"
        '<p class="item">Horas extras ........ R$ 7.338,46;</p>'
        '<p class="nota"><b>[NOTA DO VALIDADOR]</b> confira</p>'
        '<p class="inexistente">vira corpo</p>'
    )
    gerar(modelo, html, saida)
    ps = Document(saida).paragraphs
    textos = [p.text for p in ps]
    rotulo, valor = textos[2].split("\t")
    assert rotulo.startswith("Horas extras ....") and rotulo.rstrip(".") == "Horas extras ", rotulo  # pontos no texto
    assert valor == "R$ 7.338,46;", valor                                       # valor depois da tabulação
    textos[2] = None
    assert textos == [
        "DAS HORAS EXTRAS",                      # número manual removido
        "Texto com negrito e\xa0\xa0espaço.",    # &nbsp; preservado
        None,
        "[NOTA DO VALIDADOR] confira",
        "vira corpo",
    ], textos
    assert ps[1].runs[1].bold and not ps[1].runs[0].bold
    assert ps[3].runs[0]._r.rPr.find(qn("w:highlight")) is not None
    assert "{{" not in "".join(p.text for p in ps)
print("ok")

# A linha com os pontos cabe antes da tabulação, com e sem negrito.
from pontilhado import RECUO_PT, TAB_PT, largura, linha
for rotulo, valor, negrito in [("Horas extras", "R$ 2.876,49;", False),
                               ("TOTAL DAS HORAS EXTRAS", "R$ 4.141,51;", True)]:
    texto, val = linha(rotulo, valor, negrito).split("\t")
    assert RECUO_PT + largura(texto, negrito) + largura(val, negrito) <= TAB_PT, (rotulo, texto)
    assert len(texto) - len(rotulo) > 40, texto
print("ok pontilhado")
