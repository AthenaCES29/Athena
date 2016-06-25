#include <stdio.h>
#include "codigo.c"

int main () {
	FILE *entrada1, *entrada2;
	int par1, par2, resultado;

	entrada1 = fopen("entrada1.txt", "r");
	par2 = 3;

	fscanf(entrada1, "%d", &par1);
	resultado = 0;

	if (funcao1(par1) == par1*par1)
		resultado++;
	if (funcao1(par2) == par2*par2)
		resultado = resultado + 2;

	fclose(entrada1);

	// Printar a nota do aluno
	printf("%d", (resultado*33 +1));

	return 0;
}