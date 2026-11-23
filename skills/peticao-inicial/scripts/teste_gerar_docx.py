"""Teste rápido do gerar_docx.py. Rode: uv run --with python-docx python3 teste_gerar_docx.py"""
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
    assert [p.text for p in ps] == [
        "DAS HORAS EXTRAS",                      # número manual removido
        "Texto com negrito e\xa0\xa0espaço.",    # &nbsp; preservado
        "Horas extras\tR$ 7.338,46;",            # pontilhado vira tabulação
        "[NOTA DO VALIDADOR] confira",
        "vira corpo",
    ], [p.text for p in ps]
    assert ps[1].runs[1].bold and not ps[1].runs[0].bold
    assert ps[3].runs[0]._r.rPr.find(qn("w:highlight")) is not None
    assert "{{" not in "".join(p.text for p in ps)
print("ok")
