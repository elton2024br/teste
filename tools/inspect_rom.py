"""Read-only GBA ROM identification. Usage: python inspect_rom.py path.gba"""
import hashlib
import json
from pathlib import Path
import sys

KNOWN = {
    '41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc': 'FireRed inglês, revisão 0 (pret/pokefirered)',
    'dd5945db9b930750cb39d00c84da8571feebf417': 'FireRed inglês, revisão 1 (pret/pokefirered)',
}

def inspect(path):
    digest = hashlib.sha1()
    with path.open('rb') as stream:
        header = stream.read(192)
        if len(header) < 192:
            raise ValueError('Arquivo menor que o cabeçalho GBA; não é uma ROM GBA completa.')
        digest.update(header)
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    sha1 = digest.hexdigest()
    return {
        'arquivo': path.name,
        'bytes': path.stat().st_size,
        'titulo_cabecalho': header[0xA0:0xAC].decode('ascii', errors='replace').rstrip('\x00'),
        'codigo_jogo': header[0xAC:0xB0].decode('ascii', errors='replace'),
        'revisao': header[0xBC],
        'checksum_cabecalho_valido': header[0xBD] == (-sum(header[0xA0:0xBD]) - 0x19) & 0xFF,
        'sha1': sha1,
        'identificacao': KNOWN.get(sha1, 'Hash não reconhecido: pode ser outra edição, tradução ou modificação. Exige investigação.'),
        'observacao': 'Cabeçalho e hash não provam integridade completa quando o hash não é reconhecido.',
    }

def main():
    if len(sys.argv) != 2:
        raise ValueError('Uso: python inspect_rom.py caminho_do_arquivo.gba (ou pasta com arquivos .gba)')
    target = Path(sys.argv[1])
    paths = sorted(p for p in target.iterdir() if p.is_file() and p.suffix.lower() == '.gba') if target.is_dir() else [target]
    if not paths:
        raise ValueError('Nenhum arquivo .gba encontrado nessa pasta. Descompacte o arquivo antes da análise.')
    for path in paths:
        print(json.dumps(inspect(path), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
