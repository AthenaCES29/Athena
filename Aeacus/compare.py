# comparar saida produzida com saida esperada

# receber 3 argumentos (in, out, code)
# in e out vem do banco de dados
# code vem do upload do aluno
# code pode ser .c, .cpp, .zip ou .rar

# rodar codigo e gerar saida
# comparar saida produzida com saida esperada
# inicialmente apenas faz o diff pra ver se sao identicas
# e retorna a saida do diff se forem diferentes
# se forem iguais retorna "saidas iguais"

# enviar resultados para a pagina criada

# from compiler import compile
import subprocess
import os
from Aeacus.compiler import compile
from pprint import pprint

DIRETORIO_DO_ARQUIVO = os.path.dirname(os.path.realpath(__file__))


def _is_blank(myString):
    return not(myString and myString.strip())


def _copy_file(origem, destino):
    with open(destino, 'wb+') as destination:
        destination.write(origem)


def _bytes_to_text(bytes, text):
    with open(text, 'wb+') as destination:
        for chunk in bytes.chunks():
            destination.write(chunk)


def _execute(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()
    return process.communicate()


# remove arquivos de codigo de outras compilacoes
def _deletar_codigo_antigo():
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("compiler/code")

    return _execute("rm * -fv")


def mover(testador, entrada, entrada2, codigo, restricoes):

    out, err = _deletar_codigo_antigo()
    if not _is_blank(err):
        return ("CE", (
            "Erro ao deletar arquivos antigos:\n" + out).replace("\n", "<br>")
        )

    # prepara arquivo de codigo e compila
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("compiler/code")
    _bytes_to_text(codigo, 'codigo.c')
    ABS_PATH = os.path.join(DIRETORIO_DO_ARQUIVO, "compiler/code")

    out, err = compile.compile_cpp(ABS_PATH)

    if not _is_blank(err):
        return ("CE", (
            "Erro de compilacao!\n" + err).replace("\n", "<br>")
        )

    violations = compile.violations(ABS_PATH, restricoes.split(","))
    pprint(violations)
    if len(violations) > 0:
        strViolation = ""
        for violation in violations:
            strViolation = strViolation + violation + "\n"
        return ("INV", (
            "Erro: codigo viola restricao!\n" +
            strViolation).replace("\n", "<br>")
        )

    # prepara arquivo de codigo e compila
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("compiler/code")
    _bytes_to_text(testador, 'testador.c')
    ABS_PATH = os.path.join(DIRETORIO_DO_ARQUIVO, "compiler/code")

    out, err = compile.compile_cpp(ABS_PATH)

    # mover programa.out de /compiler para /runner
    os.chdir(DIRETORIO_DO_ARQUIVO)
    _execute("mv compiler/code/programa.out runner")

    # prepara arquivos de entrada/saida e roda
    os.chdir(DIRETORIO_DO_ARQUIVO)
    os.chdir("runner")
    _copy_file(entrada, 'entrada.txt')
    _copy_file(entrada2, 'entrada2.txt')

    out, err = _execute('./programa.out')
    """if not _is_blank(err):
        return ("RTE", err.replace("\n", "<br>"))"""

    if out > 0:
        return ("WA", err)
    else:
        return ("AC", err)

    """
    # diff das saidas
    outdiff, err = _execute("cat saida.txt")

    num_diffs, err = _execute('diff -b saida.txt resposta.txt | grep -c "^>"')
    num_diffs.replace("\n", "")
    num_diffs = int(num_diffs)
    cabecalho = str(num_diffs) + "\n"
    pprint(num_diffs)

    if num_diffs != 0:
        return ("WA", cabecalho + outdiff)
    else:
        return ("AC", cabecalho + outdiff)]
    """
