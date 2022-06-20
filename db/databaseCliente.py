import pymongo
from models.cliente import Cliente


class DatabaseCliente:
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

    def create(self, cliente: Cliente):
        return self.collection.insert_one(
            {"codigo": cliente.codigo, "nome": cliente.nome, "cpf": cliente.cpf, "email": cliente.email,
             "nascimento": cliente.data_nascimento, "cadastro": cliente.data_cadastro})

    def delete(self, nome):
        return self.collection.delete_one({"nome": nome})
