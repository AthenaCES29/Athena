import subprocess
import os
from pprint import pprint


def _unzip(file):
    command = 'unzip ' + file + ' -d ' + os.path.dirname(file)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()


def _unrar(file):
    command = 'unrar e ' + file + ' ' + os.path.dirname(file)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.wait()


def _descompactar(path_to_folder):
    process = subprocess.Popen(
        'find ' + path_to_folder + ' -name "*.rar" -o -name "*.zip"',
        stdout=subprocess.PIPE, shell=True
    )

    out, err = process.communicate()
    process.wait()
    files = out.split('\n')
    for file in files:
        filename, fileExt = os.path.splitext(file)
        if fileExt == '.zip':
            _unzip(file)
        elif fileExt == '.rar':
            _unrar(file)


def _find_sources(folder_path):
    process = subprocess.Popen(
        'find ' +
        folder_path +
        ' -name "*.h" -o -name "*.cpp" -o -name "*.c" -o -name "*.a" ',
        stdout=subprocess.PIPE, shell=True
    )
    process.wait()
    out, err = process.communicate()
    return out


def _move_file_to_code_root(folder_path, file_path):
    path = folder_path
    file_name = os.path.basename(file_path)
    new_file_path = path + "/" + file_name
    if file_path != new_file_path:
        command = "mv " + file_path + " " + new_file_path
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        process.wait()


def _code_files(abs_path_to_folder):
    _descompactar(abs_path_to_folder)
    os.chdir(abs_path_to_folder)
    files = _find_sources(abs_path_to_folder).split('\n')
    # remove strings vazias
    files = filter(None, files)
    for file_path in files:
        _move_file_to_code_root(abs_path_to_folder, file_path)
    files = _find_sources(abs_path_to_folder).split('\n')

    codefiles = []
    for file in files:
        if '.c' in file:
            codefiles.append(file)

    return codefiles


def compile_cpp(abs_path_to_folder):

    files = _code_files(abs_path_to_folder)
    command = "g++ "
    for file in files:
        command += os.path.basename(file) + " "
    command += " -g -pthread -pg -std=c++0x -o programa.out"

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    process.wait()
    out, err = process.communicate()
    return out, err


def compile_prof_cpp(abs_path_to_folder):

    command = "g++ "
    command += abs_path_to_folder + "/" + os.path.basename("testador.c")
    command += " -g -pthread -pg -std=c++0x -o programa.out"

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    process.wait()
    out, err = process.communicate()
    return out, err


def _crop_abs_path(abs_path_to_folder):
    file = abs_path_to_folder
    index = file.rfind("/") + 1
    return file[index:]


def violations(abs_path_to_folder, restricoes):

    violations = []
    files = _code_files(abs_path_to_folder)

    for file in files:
        codigo = open(file)
        fileName = "File: " + _crop_abs_path(file) + " - "
        for num, line in enumerate(codigo, 1):
            pprint(line)
            for restricao in restricoes:
                if restricao in line:
                    linha = "Linha " + str(num) + " : "
                    violations.append(
                        fileName + linha + restricao
                    )

    return violations
