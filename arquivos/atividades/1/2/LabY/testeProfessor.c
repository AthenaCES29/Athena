#include <stdio.h>
#include "codigo.c"

int main () {
	FILE *entrada1, *entrada2;
	int par1, par2, resultado;

	entrada1 = fopen("entrada1.txt", "r");
	entrada2 = fopen("entrada2.txt", "r");

	fscanf(entrada1, "%d", &par1);
	fscanf(entrada2, "%d", &par2);

	resultado = 0;

	if (funcao1(par1) == par1*par1)
		resultado++;
	if (funcao1(par2) == par2*par2)
		resultado = resultado + 2;

	fclose(entrada1);
	fclose(entrada2);

	// Printar a nota do aluno
	printf("%d", (resultado*33 +1));

	return 0;
}