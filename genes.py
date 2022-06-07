
from posixpath import split
import re

def multi_char_replace(input: str, replace: dict[str, str]) -> str:
	return ''.join([replace[c] if c in replace else c for c in input])

def split_em_trincas(input: str) -> list[str]:
	return list(filter(None, re.split("(\S{3})", input)))

tabela_complementar = {
	'T': 'A',
	'A': 'T',
	'G': 'C',
	'C': 'G',
}

tabela_transcricao = {
	'T': 'A',
	'A': 'U',
	'G': 'C',
	'C': 'G',
}

tabela_anticodons = {
	'U': 'A',
	'A': 'U',
	'G': 'C',
	'C': 'G',
}

# inicio: ATG ou AUG
# fim:
# TAG TAA TGA ou
# UAG UAA UGA

def encontrar_gene(fita: str, do_mensageiro: bool = False) -> str:
	gene_preliminar = fita[fita.index("AUG" if do_mensageiro else "ATG"):]
	trincas_gene = []
	trincas_fim = ("UAG", "UAA", "UGA") if do_mensageiro else ("TAG", "TAA", "TGA")

	for trinca in split_em_trincas(gene_preliminar):
		trincas_gene.append(trinca)

		if trinca in trincas_fim:
			break

	return ''.join(trincas_gene)

fita = "AAAATTGTTT TAAAGGAATA CCATGCCTCC CAAGAAGAAG GATGAGAAGT CACAACCGCC CCGCACGATT TTGCTGGGCC GACCTGGAAG TAACTTGAAG ATTGGGATTG TTGGGCTTCC TAACGTTGGC AAGTCCACAT TTTTCAACGT TCTATCTAAA AAAGGTGTTC CCGCTGAAAA GAAGTAGTTT TATTTATTTG AATCAATAAT AATAATAATA TTGATAAAGT AACGGGAAGG GGAACCTCCA AAAAAAAAAA AAAAAAAAA"
fita = fita.replace(" ", "")

gene = encontrar_gene(fita)

print(f"\nA) Gene:   ({len(gene)} bases)")
print(' '.join(split_em_trincas(gene)))

fita_complementar = multi_char_replace(fita, tabela_complementar)

print("\nB) Fita complementar:")
print("'5", fita_complementar, "'3")

gene_complementar = multi_char_replace(gene, tabela_complementar)
mensageiro = multi_char_replace(gene_complementar, tabela_transcricao)
ncodons = len(mensageiro) / 3

print(f"\nC) RNA mensageiro: ({ncodons} códons)")
print(' '.join(split_em_trincas(mensageiro)))

anticodons = multi_char_replace(mensageiro, tabela_anticodons)
nanticodons = len(anticodons) / 3

print(f"\nD) Anticódons: ({nanticodons} códons)")
print(' '.join(split_em_trincas(anticodons)))

tabela_aminoacidos = {
    'Phe': ["UUU", "UUC"],
    'Leu': ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
    'Ile': ["AUU", "AUC", "AUA"],
    'Met': ["AUG"],
    'Val': ["GUU", "GUC", "GUA", "GUG"],
    'Ser': ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
    'Pro': ["CCU", "CCC", "CCA", "CCG"],
    'Thr': ["ACU", "ACC", "ACA", "ACG"],
    'Ala': ["GCU", "GCC", "GCA", "GCG"],
    'Tyr': ["UAU", "UAC"],
    'His': ["CAU", "CAC"],
    'Gln': ["CAA", "CAG"],
    'Asn': ["AAU", "AAC"],
    'Lys': ["AAA", "AAG"],
    'Asp': ["GAU", "GAC"],
    'Glu': ["GAA", "GAG"],
    'Cys': ["UGU", "UGC"],
    'Trp': ["UGG"],
    'Arg': ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
    'Gly': ["GGU", "GGC", "GGA", "GGG"],
    'pare': ["UAA", "UAG", "UGA"],
}

transformer = []

for trinca in split_em_trincas(mensageiro):
    encontrado = False
    
    for aminoacido in tabela_aminoacidos:
        trincasAceitas = tabela_aminoacidos[aminoacido]

        if trinca in trincasAceitas:
            transformer.append(aminoacido)
            encontrado = True
            break

    if not encontrado:
        transformer.append("Erro")

print("\nE) Teoricamente os aminoácidos:")
print(" ".join(transformer))
    
