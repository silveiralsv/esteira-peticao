#!/usr/bin/env python3
"""Gera a petição .docx no papel timbrado do escritório a partir do HTML do Redator.

Uso:
    uv run --with python-docx --with pillow python3 gerar_docx.py <modelo.docx> <peticao.html> <saida.docx>

O modelo é um .docx com cabeçalho, rodapé, estilos e um parágrafo de exemplo por
papel, cujo texto é só "{{papel}}" (ex.: "{{corpo}}"). Cada bloco do HTML copia a
formatação do parágrafo de exemplo do seu papel. Ver referencia/formatacao.md.
"""
import copy
import re
import sys
from html.parser import HTMLParser

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from pontilhado import pontos

TAG_PAPEL = {"h1": "titulo", "h2": "secao", "h3": "subsecao", "li": "lista", "p": "corpo"}
BLOCOS = set(TAG_PAPEL) | {"blockquote"}
LINHA_VALOR = {"item", "total", "subtotal"}
PONTILHADO = re.compile(r"\s*(?:\.|…){4,}\s*")
NUMERO_MANUAL = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s+")
# Ordem dos filhos de w:rPr exigida pelo schema do Word.
ORDEM_RPR = [qn("w:" + t) for t in (
    "rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint "
    "noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u "
    "effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath").split()]


class LeitorHTML(HTMLParser):
    """Lê o HTML simples do Redator: blocos com papel e trechos com negrito, itálico e sublinhado."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocos, self.atual, self.estilo, self.na_citacao = [], None, [], False

    def handle_starttag(self, tag, attrs):
        classe = (dict(attrs).get("class") or "").split()
        if tag == "blockquote":
            self.na_citacao = True
        elif tag in TAG_PAPEL:
            papel = classe[0] if classe else ("citacao" if self.na_citacao else TAG_PAPEL[tag])
            self.atual = (papel, [])
            self.blocos.append(self.atual)
        elif tag in ("b", "strong", "i", "em", "u"):
            self.estilo.append({"strong": "b", "em": "i"}.get(tag, tag))
        elif tag == "br" and self.atual:
            self.atual[1].append(("\n", set()))

    def handle_endtag(self, tag):
        if tag == "blockquote":
            self.na_citacao = False
        elif tag in TAG_PAPEL:
            self.atual = None
        elif tag in ("b", "strong", "i", "em", "u"):
            marca = {"strong": "b", "em": "i"}.get(tag, tag)
            if marca in self.estilo:
                self.estilo.reverse(); self.estilo.remove(marca); self.estilo.reverse()

    def handle_data(self, data):
        if self.atual is None:
            if not data.strip():
                return
            self.atual = ("corpo", [])  # texto solto vira corpo
            self.blocos.append(self.atual)
        self.atual[1].append((re.sub(r"[ \t\r\n]+", " ", data), set(self.estilo)))  # &nbsp; fica


def novo_rpr(base, marcas, destacar):
    rpr = copy.deepcopy(base) if base is not None else OxmlElement("w:rPr")
    for filho in list(rpr):
        if filho.tag in (qn("w:b"), qn("w:bCs"), qn("w:i"), qn("w:iCs"), qn("w:u"), qn("w:highlight")) or (
                destacar and filho.tag == qn("w:shd")):
            rpr.remove(filho)
    novos = []
    if "b" in marcas:
        novos += [OxmlElement("w:b"), OxmlElement("w:bCs")]
    if "i" in marcas:
        novos += [OxmlElement("w:i"), OxmlElement("w:iCs")]
    if destacar:
        h = OxmlElement("w:highlight"); h.set(qn("w:val"), "yellow"); novos.append(h)
    if "u" in marcas:
        u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); novos.append(u)
    filhos = list(rpr) + novos
    for f in list(rpr):
        rpr.remove(f)
    for f in sorted(filhos, key=lambda e: ORDEM_RPR.index(e.tag) if e.tag in ORDEM_RPR else len(ORDEM_RPR)):
        rpr.append(f)
    return rpr


def novo_run(texto, marcas, base, destacar=False, tab=False):
    r = OxmlElement("w:r")
    r.append(novo_rpr(base, marcas, destacar))
    if tab:
        r.append(OxmlElement("w:tab"))
    for k, parte in enumerate(texto.split("\n")):
        if k:
            r.append(OxmlElement("w:br"))
        if parte:
            t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = parte
            r.append(t)
    return r


def texto_de(p):
    return "".join(t.text or "" for t in p.iter(qn("w:t"))).strip()


def gerar(modelo, html, saida):
    doc = Document(modelo)
    corpo = doc.element.body
    exemplos = {}
    for p in list(corpo.iterchildren(qn("w:p"))):
        m = re.fullmatch(r"\{\{([\w-]+)\}\}", texto_de(p))
        if m:
            exemplos[m.group(1)] = p
        corpo.remove(p)
    for t in list(corpo.iterchildren(qn("w:tbl"))):
        corpo.remove(t)
    fim = corpo.find(qn("w:sectPr"))

    leitor = LeitorHTML()
    leitor.feed(open(html, encoding="utf-8").read())
    faltando = set()
    for papel, trechos in leitor.blocos:
        trechos = [(t, m) for t, m in trechos if t]
        if not "".join(t for t, _ in trechos).strip():
            continue
        if papel not in exemplos:
            faltando.add(papel)
        base_p = exemplos[papel] if papel in exemplos else exemplos["corpo"]
        p = copy.deepcopy(base_p)
        runs = p.findall(qn("w:r"))
        base_r = next((r.find(qn("w:rPr")) for r in runs if texto_de(r)), None)
        for filho in list(p):
            if filho.tag != qn("w:pPr"):
                p.remove(filho)
        # tira espaços nas pontas do bloco
        t0, m0 = trechos[0]; trechos[0] = (t0.lstrip(), m0)
        tn, mn = trechos[-1]; trechos[-1] = (tn.rstrip(), mn)
        if papel in ("secao", "subsecao"):
            t0, m0 = trechos[0]; trechos[0] = (NUMERO_MANUAL.sub("", t0, count=1), m0)
        destacar = papel == "nota"
        if papel in LINHA_VALOR:
            inteiro = "".join(t for t, _ in trechos)
            partes = PONTILHADO.split(inteiro)
            negrito = papel != "item" or all("b" in m for _, m in trechos)
            marcas = {"b"} if negrito else set()
            if len(partes) >= 2:
                # O Google Docs perde o pontilhado da tabulação: os pontos vão no texto.
                rotulo, valor = " ".join(partes[:-1]).strip(), partes[-1].strip()
                p.append(novo_run(f"{rotulo} {pontos(rotulo, valor, negrito)}", marcas, base_r))
                p.append(novo_run(valor, marcas, base_r, tab=True))
            else:
                p.append(novo_run(inteiro, marcas, base_r))
        else:
            for texto, marcas in trechos:
                p.append(novo_run(texto, marcas, base_r, destacar))
        fim.addprevious(p)
    doc.save(saida)
    if faltando:
        print("Papéis sem exemplo no modelo (usei 'corpo'):", ", ".join(sorted(faltando)), file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    gerar(*sys.argv[1:])
