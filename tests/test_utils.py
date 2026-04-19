from src.fasta_parser import leer_fasta


def test_fasta_simple(tmp_path):
    contenido = ">seq1\nAUGC\n"
    archivo = tmp_path / "test.fasta"
    archivo.write_text(contenido)

    secuencias = leer_fasta(str(archivo))

    assert secuencias == [("seq1", "AUGC")]


def test_fasta_multiple(tmp_path):
    contenido = ">seq1\nAUGC\n>seq2\nGGCC\n"
    archivo = tmp_path / "test2.fasta"
    archivo.write_text(contenido)

    secuencias = leer_fasta(str(archivo))

    assert secuencias == [("seq1", "AUGC"), ("seq2", "GGCC")]
