import pymongo
from models.conta import Conta

class Database:
    def __init__(self, database, collection):
        connectionString = "mongodb+srv://adm:adm@bank.regl2gy.mongodb.net/?retryWrites=true&w=majority"
        self.clusterConnection = pymongo.MongoClient(
            connectionString,
            # CASO OCORRA O ERRO [SSL_INVALID_CERTIFICATE]
            tlsAllowInvalidCertificates=True
        )
        self.db = self.clusterConnection[database]
        self.collection = self.db[collection]

    def resetDatabase(self):
        self.db.drop_collection(self.collection)

    def create(self, conta: Conta):
        return self.collection.insert_one({"nConta": conta.numero, "cliente": conta.cliente.nome, "saldo": conta.saldo, "limite": conta.limite})

    def read(self):
        return self.collection.find({})

    def read_total_contas(self):
        return self.collection.count_documents({})

    def retornar_saldo(self,nConta):
        v = self.collection.find_one({"nConta": nConta}, {"_id": 0, "saldo": 1 })
        return v["saldo"]

    def retornar_conta(self,nConta):
        return self.collection.find_one({"nConta": nConta}, {"_id": 0, "saldo": 1, "limite": 1})

    def update(self, nConta, saldo, limite):
        return self.collection.update_one({"nConta": nConta}, {"$set": {"saldo": saldo, "limite": limite}})

    def depositar(self, nConta, valor):
        self.collection.update_one({"nConta": nConta}, {"$inc": {"saldo": valor}})
        print("Depósito realizado com sucesso!")

    def sacar(self, nConta, valor):
        if self.retornar_saldo(nConta) >= valor:
            self.collection.update_one({"nConta": nConta}, {"$inc": {"saldo": -valor}})
            return True
        else:
            print("Sem saldo suficiente")
            return False

    def transferir(self, nContaOrigem, nContaDestino, valor):
        if self.sacar(nContaOrigem, valor):
            self.depositar(nContaDestino, valor)
            return True
        return False

    def delete(self, nConta):
        v = self.collection.find_one({"nConta": nConta}, {"_id": 0, "cliente": 1})
        nome = v["cliente"]
        self.collection.delete_one({"nConta": nConta})
        return nome
