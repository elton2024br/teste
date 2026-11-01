#!/usr/bin/env bash
set -euo pipefail
bichos_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$bichos_root/logs"
command -v apt-get >/dev/null || { echo 'Este script precisa de Ubuntu/Debian, por exemplo no WSL Ubuntu.'; exit 1; }
sudo apt-get update
sudo apt-get install -y build-essential binutils-arm-none-eabi libpng-dev git python3 python3-pil
cd "$bichos_root/agbcc"
bash ./build.sh > "$bichos_root/logs/agbcc.log" 2>&1
bash ./install.sh "$bichos_root/pokefirered"
cd "$bichos_root/pokefirered"
make generated
make GAME_VERSION=FIRERED GAME_REVISION=1 -W data/maps.s -W data/map_events.s build/firered_rev1/data/maps.o build/firered_rev1/data/map_events.o
make -j4 firered_rev1 > "$bichos_root/logs/game-build.log" 2>&1
sha1sum pokefirered_rev1.gba
printf '\nBuild concluido. ROM: %s/pokefirered/pokefirered_rev1.gba\n' "$bichos_root"
