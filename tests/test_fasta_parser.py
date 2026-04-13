from src.fasta_parser import leer_fasta


def test_leer_fasta_contenido(tmp_path):
    contenido = ">seq1\nGCUACG\n"
    archivo = tmp_path / "test.fasta"
    archivo.write_text(contenido)

    resultado = leer_fasta(str(archivo))

    assert resultado == ["GCUACG"]


def test_leer_fasta_multilinea(tmp_path):
    contenido = ">seq1\nGGGG\nAAAA\n"
    archivo = tmp_path / "test2.fasta"
    archivo.write_text(contenido)

    resultado = leer_fasta(str(archivo))

    assert resultado == ["GGGGAAAA"]