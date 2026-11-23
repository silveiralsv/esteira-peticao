#!/usr/bin/env bash
# Liga a skill e os agentes deste repositório ao Claude Code com links simbólicos.
# Pode rodar de novo: link certo fica como está; arquivo diferente no destino não é tocado.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
home="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$home/skills" "$home/agents"

link() {
  local src="$1" dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "ok        $dst"
  elif [ -e "$dst" ] || [ -L "$dst" ]; then
    echo "CONFLITO  $dst já existe e não aponta para $src. Não mexi." >&2
    conflict=1
  else
    ln -s "$src" "$dst"
    echo "ligado    $dst -> $src"
  fi
}

conflict=0
link "$repo/skills/peticao-inicial" "$home/skills/peticao-inicial"
for f in "$repo"/agents/*.md; do
  link "$f" "$home/agents/$(basename "$f")"
done

cfg="$repo/skills/peticao-inicial/config.local.md"
[ -f "$cfg" ] || echo "Falta $cfg. Copie config.example.md e preencha o link do banco de teses."
exit "$conflict"
