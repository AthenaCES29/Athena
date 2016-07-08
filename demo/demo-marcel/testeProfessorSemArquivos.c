#include <stdio.h>
#include "codigo.c"

int main () {
	int par1, par2, resultado;

	par1 = 2;
	par2 = 3;

	resultado = 0;

	if (funcao1(par1) == par1*par1)
		resultado++;
	if (funcao1(par2) == par2*par2)
		resultado = resultado + 2;

	// Printar a nota do aluno
	printf("%d", (resultado*33 +1));

	return 0;
}