from typing import List
from time import sleep

from models.cliente import Cliente
from models.conta import Conta

from db.database import Database
from db.databaseCliente import DatabaseCliente

db = Database("Bank", "Accounts")
db.resetDatabase()
dbc = DatabaseCliente("Bank", "Clients")
dbc.resetDatabase()

def main() -> None:
    menu()


def menu() -> None:
    print('=====================================')
    print('============== ATM ==================')
    print('============ AR BANK ================')
    print('=====================================')

    print('Selecione uma opção no menu: ')
    print('1 - Criar conta')
    print('2 - Efetuar saque')
    print('3 - Efetuar depósito')
    print('4 - Efetuar transferência')
    print('5 - Listar contas')
    print('6 - Deletar conta')
    print('7 - Sair do sistema')

    opcao: int = int(input())

    if opcao == 1:
        criar_conta()
    elif opcao == 2:
        efetuar_saque()
    elif opcao == 3:
        efetuar_deposito()
    elif opcao == 4:
        efetuar_transferencia()
    elif opcao == 5:
        listar_contas()
    elif opcao == 6:
        deletar_conta()
    elif opcao == 7:
        print('Volte sempre')
        sleep(2)
        exit(0)
    else:
        print('Opção inválida')
        sleep(2)
        menu()


def criar_conta() -> None:
    print('Informe os dados do cliente: ')

    nome: str = input('Nome do cliente: ')
    email: str = input('E-mail do cliente: ')
    cpf: str = input('CPF do cliente: ')
    data_nascimento: str = input('Data de nascimento do cliente (dd/mm/yyyy): ')

    cliente: Cliente = Cliente(nome, email, cpf, data_nascimento)

    conta: Conta = Conta(cliente)

    db.create(conta)
    dbc.create(cliente)

    print('Conta criada com sucesso.')
    print('Dados da conta: ')
    print('-----------------')
    print(conta)
    sleep(2)
    menu()


def efetuar_saque() -> None:
    if db.read_total_contas() > 0:
        numero: int = int(input('Informe o número da sua conta: '))
        if db.retornar_conta(numero) is None:
            print('Conta não encontrada')
        else:
            valor: float = float(input('Informe o valor do saque: '))
            if db.sacar(numero, valor):
                print('Saque efetuado com sucesso.')
            else:
                print('Saldo insuficiente.')
    else:
        print('Não existem contas cadastradas.')
    sleep(2)
    menu()


def efetuar_deposito() -> None:
    if db.read_total_contas() > 0:
        numero: int = int(input('Informe o número da sua conta: '))
        if db.retornar_conta(numero) is None:
            print('Conta não encontrada')
        else:
            valor: float = float(input('Informe o valor do depósito: '))
            db.depositar(numero, valor)
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def efetuar_transferencia() -> None:
    if db.read_total_contas() > 0:
        numero_o: int = int(input('Informe o número da sua conta: '))
        if db.retornar_conta(numero_o) is None:
            print(f'A sua conta com número {numero_o} não foi encontrada.')
        else:
            numero_d: int = int(input('Informe o número da conta destino: '))
            if db.retornar_conta(numero_o) is None:
                print(f'A conta destino com número {numero_d} não foi encontrada.')
            else:
                valor: float = float(input('Informe o valor da transferência: '))
                if db.transferir(numero_o, numero_d, valor):
                    print('Transferência efetuada com sucesso.')
                else:
                    print('Saldo insuficiente.')
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def listar_contas() -> None:
    if db.read_total_contas() > 0:
        contas: List[Conta] = db.read()
        for conta in contas:
            print(f" Numero da Conta: {conta['nConta']}")
            print(f" Nome do Cliente: {conta['cliente']}")
            print(f" Saldo: {conta['saldo']}")
            print(f" Limite: {conta['limite']}")
            print('-----------------')
    else:
        print('Não existem contas cadastradas.')
    sleep(2)
    menu()


def deletar_conta() -> None:
    if db.read_total_contas() > 0:
        numero: int = int(input('Informe o número da conta que deseja deletar: '))
        if db.retornar_conta(numero) is None:
            print('Conta não encontrada')
        else:
            dbc.delete(db.delete(numero))
            print('Conta deletada com sucesso.')
    else:
        print('Não existem contas cadastradas.')
    sleep(2)
    menu()

if __name__ == '__main__':
    main()
