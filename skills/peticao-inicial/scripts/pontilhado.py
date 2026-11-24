#!/usr/bin/env python3
"""Pontilhado das linhas de valor da petição.

O Google Docs não tem tabulação com pontilhado: na conversão do docx o pontilhado some e
sobra um espaço em branco antes do valor. Por isso a esteira escreve os pontos no próprio
texto, até perto do valor, e a tabulação alinhada à direita (432 pt) leva o valor ao fim da linha.

Uso:
    uv run --with pillow python3 pontilhado.py "<rótulo>" "<valor>" [--negrito]
Imprime a linha pronta: "<rótulo> <pontos>\\t<valor>".
"""
import sys

TAB_PT = 432     # tabulação à direita das linhas de valor, a partir da margem
RECUO_PT = 7.05  # recuo das linhas de valor
CORPO_PT = 11    # Times New Roman 11
FONTE = "/System/Library/Fonts/Supplemental/Times New Roman{}.ttf"


def largura(texto, negrito=False):
    """Largura do texto em pontos, em Times New Roman 11."""
    try:
        from PIL import ImageFont
        return ImageFont.truetype(FONTE.format(" Bold" if negrito else ""), 1000).getlength(texto) * CORPO_PT / 1000
    except (ImportError, OSError):
        # ponytail: média da Times sem a fonte instalada; erra alguns pontos, por isso a folga abaixo
        return sum(0.25 if c in ".,;:' " else 0.5 for c in texto) * CORPO_PT


def pontos(rotulo, valor, negrito=False):
    """Pontos que cabem entre o rótulo e o valor, deixando meio corpo de folga antes do valor."""
    livre = TAB_PT - RECUO_PT - largura(rotulo + " ", negrito) - largura(valor, negrito) - CORPO_PT / 2
    return "." * max(3, int(livre // largura(".", negrito)))


def linha(rotulo, valor, negrito=False):
    return f"{rotulo} {pontos(rotulo, valor, negrito)}\t{valor}"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--negrito"]
    if len(args) != 2:
        sys.exit(__doc__)
    print(linha(*args, negrito="--negrito" in sys.argv))
