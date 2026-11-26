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
        "<html><head><title>PETIÇÃO</title><style>p {}</style></head><body>"  # não entra no texto
        "<h2>4.1. DAS HORAS EXTRAS</h2>"
        "<p>Texto com <b>negrito</b> e&nbsp;&nbsp;espaço.</p>"
        '<p class="item">Horas extras ........ R$ 7.338,46;</p>'
        '<p class="nota"><b>[NOTA DO VALIDADOR]</b> confira</p>'
        '<p class="inexistente">vira corpo</p>'
        "</body></html>"
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

# Encerramento: só o último fecho leva o espaço do modelo; os de cima ficam juntos.
from docx.shared import Pt
with tempfile.TemporaryDirectory() as d:
    modelo, html, saida = (os.path.join(d, n) for n in ("m.docx", "p.html", "s.docx"))
    m = Document()
    m.add_paragraph("{{corpo}}")
    f = m.add_paragraph("{{fecho}}").paragraph_format
    f.space_before, f.space_after = Pt(24), Pt(36)
    m.save(modelo)
    open(html, "w", encoding="utf-8").write(
        '<p class="fecho">Termos em que,</p><p class="fecho">Pede deferimento.</p>'
        '<p class="fecho">São Paulo, data e assinatura certificadas.</p>')
    gerar(modelo, html, saida)
    esp = [(p.paragraph_format.space_before, p.paragraph_format.space_after) for p in Document(saida).paragraphs]
    assert esp == [(0, 0), (0, 0), (Pt(24), Pt(36))], esp
print("ok fecho")

# A linha com os pontos cabe antes da tabulação, com e sem negrito.
from pontilhado import RECUO_PT, TAB_PT, largura, linha
for rotulo, valor, negrito in [("Horas extras", "R$ 2.876,49;", False),
                               ("TOTAL DAS HORAS EXTRAS", "R$ 4.141,51;", True)]:
    texto, val = linha(rotulo, valor, negrito).split("\t")
    assert RECUO_PT + largura(texto, negrito) + largura(val, negrito) <= TAB_PT, (rotulo, texto)
    assert len(texto) - len(rotulo) > 40, texto
print("ok pontilhado")

# Linhas em branco da advogada e SUBTOTAL com tabulações e R$ junto do número.
with tempfile.TemporaryDirectory() as d:
    modelo, html, saida = (os.path.join(d, n) for n in ("m.docx", "p.html", "s.docx"))
    m = Document()
    for papel in ("corpo", "enderecamento", "em-face", "subtotal", "fecho"):
        m.add_paragraph("{{%s}}" % papel)
    m.save(modelo)
    open(html, "w", encoding="utf-8").write(
        '<p class="enderecamento">AO JUÍZO</p><p>PREÂMBULO</p><p class="em-face">em face de X</p>'
        '<p class="local">Local</p><p class="subtotal"><b>SUBTOTAL em 1 de maio de 2027 R$ 1,00 (um real).</b></p>'
        '<p>G – valor</p><p class="fecho">Termos em que,</p><p class="fecho">Pede deferimento.</p>')
    gerar(modelo, html, saida)
    textos = [p.text for p in Document(saida).paragraphs]
    assert textos == ["AO JUÍZO", "", "", "", "PREÂMBULO", "em face de X", "", "", "Local",
                      "SUBTOTAL em 1 de maio de 2027 \t\t\t\t\tR$1,00 (um real).", "", "G – valor", "",
                      "Termos em que,", "Pede deferimento."], textos
print("ok linhas em branco")

# Rótulo longo não cabe (só 3 pontos, o gerar_docx avisa); o rótulo curto da advogada cabe.
from pontilhado import pontos
assert pontos("Integração e reflexos das diferenças do acúmulo de função na multa de 40% do FGTS", "R$ 1.234,56;") == "..."
assert len(pontos("Integração e reflexos das diferenças do acúmulo de função na multa de 40%", "R$ 1.234,56;")) > 3
print("ok rótulo longo")
