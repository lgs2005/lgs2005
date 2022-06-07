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

def encontrar_gene(fita: str, complementar: bool = False) -> str:
	gene_preliminar = fita[fita.index("AUG" if complementar else "ATG"):]
	trincas = split_em_trincas(gene_preliminar)

	trincas_gene = []
	trincas_fim = ("UAG", "UAA", "UGA") if complementar else ("TAG", "TAA", "TGA")

	for trincas in trincas:
		trincas_gene.append(trincas)

		if trincas in trincas_fim:
			break

	return ''.join(trincas_gene)

fita = "AAAATTGTTT TAAAGGAATA CCATGCCTCC CAAGAAGAAG GATGAGAAGT CACAACCGCC CCGCACGATT TTGCTGGGCC GACCTGGAAG TAACTTGAAG ATTGGGATTG TTGGGCTTCC TAACGTTGGC AAGTCCACAT TTTTCAACGT TCTATCTAAA AAAGGTGTTC CCGCTGAAAA GAAGTAGTTT TATTTATTTG AATCAATAAT AATAATAATA TTGATAAAGT AACGGGAAGG GGAACCTCCA AAAAAAAAAA AAAAAAAAA"
fita = fita.replace(" ", "")

gene = encontrar_gene(fita)

print(f"\nA) Gene:   ({len(gene)} bases)")
print(gene)

fita_complementar = multi_char_replace(fita, tabela_complementar)

print("\nB) Fita complementar:")
print("'5", fita_complementar, "'3")

codons_mensageiro = multi_char_replace(fita_complementar, tabela_transcricao)

print(f"\nC) RNA mensageiro: ({len(codons_mensageiro) / 3} códons)")
print(codons_mensageiro)

gene_no_mensageiro = encontrar_gene(codons_mensageiro, True)
anticodons = multi_char_replace(gene_no_mensageiro, tabela_anticodons)

print(f"\nD) Anticódons: ({len(anticodons) / 3} códons)")
print(' '.join(split_em_trincas(anticodons)))
