from arango import ArangoClient
from Database.config import *
from DataModels.ApiModels import *
from DataModels.DbModels import *
from DataModels.ModelsConvertor import ModelConvertor

"""
Принимает JSON, возвращает JSON
"""


class ArchModelGraphDb():
    """
    База данных с графом моделей
    """

    def __init__(self, host: str, username: str, password: str, databaseName: str):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__databaseName = databaseName

        client = ArangoClient(hosts=self.__host)
        sys_db = client.db('_system', username=self.__username, password=self.__password)
        if not sys_db.has_database(self.__databaseName):
            sys_db.create_database(self.__databaseName)

        self.database = client.db(self.__databaseName, username=self.__username, password=self.__password)

    def createModel(self, model: JSON):
        if self.database.has_graph(model["_key"]):
            model = self.database.graph(model["_key"])
        else:
            model = self.database.create_graph(model["_key"])
        # Create a new vertex collection named "blocks" if it does not exist.
        # This returns an API wrapper for "blocks" vertex collection.
        if not model.has_vertex_collection(CollectionNames.blocks.name):
            model.create_vertex_collection(CollectionNames.blocks.name)

        if not model.has_edge_definition(CollectionNames.arrows.name):
            model.create_edge_definition(
                edge_collection=CollectionNames.arrows.name,
                from_vertex_collections=[CollectionNames.blocks.name],
                to_vertex_collections=[CollectionNames.blocks.name]
            )

        if not model.has_edge_definition(CollectionNames.nests.name):
            model.create_edge_definition(
                edge_collection=CollectionNames.nests.name,
                from_vertex_collections=[CollectionNames.blocks.name],
                to_vertex_collections=[CollectionNames.blocks.name]
            )

    def deleteModel(self, model_id: str):
        self.database.delete_graph(model_id, drop_collections=True)

    """

    """

    def getElements(self, model_id: str):
        model = self.database.graph(model_id)
        allElements = {
            "elements": model.vertex_collection(CollectionNames.blocks.name),
            "arrows": model.edge_collection(CollectionNames.arrows.name)}
        return allElements

    """
    """

    def addBlock(self, model_id: str, block: JSON):
        model = self.database.graph(model_id)
        model.vertex_collection(CollectionNames.blocks.name).insert(block)

    def changeBlock(self, model_id: str, block_id: str, newBlock: JSON):
        model = self.database.graph(model_id)
        newBlock["_key"] = block_id
        model.vertex_collection(CollectionNames.blocks.name).replace(newBlock)

    def deleteBlock(self, model_id: str, block_id: str):
        model = self.database.graph(model_id)
        model.vertex_collection(CollectionNames.blocks.name).delete(block_id)

    """

    """

    def addArrow(self, model_id: str, arrow: JSON):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.arrows.name).insert(arrow)

    def changeArrow(self,):
        pass

    def deleteArrow(self, model_id: str, arrow_id: str):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.arrows.name).delete(arrow_id)

    """
    """

    def addNest(self, model_id: str, nest: JSON):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.nests.name).insert(nest)

    def changeNest(self):
        pass

    def deleteNest(self, model_id: str, nest_id: str):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.arrows.name).delete(nest_id)

    """
    """


class ArchModelInfoDb:
    """
    База данных с информацией о моделях
    """

    def __init__(self, host: str, username: str, password: str, databasename: str):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__databaseName = databasename

        client = ArangoClient(hosts=self.__host)
        sys_db = client.db('_system', username=self.__username, password=self.__password)
        if not sys_db.has_database(self.__databaseName):
            sys_db.create_database(self.__databaseName)

        self.database = client.db(self.__databaseName, username=self.__username, password=self.__password)
        if self.database.has_collection("DatabaseInfo"):
            self.collection = self.database.collection("DatabaseInfo")
        else:
            self.collection = self.database.create_collection("DatabaseInfo")

    def getModelDescription(self, model_id: str) -> Model | None:
        return self.collection.get(model_id)

    def createModel(self, model: JSON):
        self.collection.insert(model)

    def deleteModel(self, model_id: str):
        self.collection.delete(model_id)

    def changeModelDescription(self, model: JSON):
        self.collection.update_match({'_key': model["_key"]}, model)


archModelGraphDb = ArchModelGraphDb(HOST, ROOT_USERNAME, ROOT_PASSWORD, MODEL_GRAPH_DB_NAME)
archModelInfoDb = ArchModelInfoDb(HOST, ROOT_USERNAME, ROOT_PASSWORD, MODEL_INFO_DB_NAME)
