from arango import ArangoClient
from Database.config import *
from DataModels.ApiModels import *
from DataModels.DbModels import *

"""
Принимает dict, возвращает dict
"""


class ArchModelGraphDb():
    """
    База данных с графом моделей
    """

    def __init__(self, host: str, username: str, password: str, data_base_name: str):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__data_base_name = data_base_name

        client = ArangoClient(hosts=self.__host)
        sys_db = client.db('_system', username=self.__username, password=self.__password)
        if not sys_db.has_database(self.__data_base_name):
            sys_db.create_database(self.__data_base_name)

        self.database = client.db(self.__data_base_name, username=self.__username, password=self.__password)

    def create_model(self, model: dict):
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

    def delete_model(self, model_id: str):
        self.database.delete_graph(model_id, drop_collections=True)

    """

    """

    def get_elements(self, model_id: str):
        model = self.database.graph(model_id)
        allElements = {
            "elements": model.vertex_collection(CollectionNames.blocks.name),
            "arrows": model.edge_collection(CollectionNames.arrows.name)}
        return allElements

    """
    """

    def add_block(self, model_id: str, block: dict):
        model = self.database.graph(model_id)
        model.vertex_collection(CollectionNames.blocks.name).insert(block)

    def get_block(self, model_id: str, block_id: str):
        model = self.database.graph(model_id)
        return model.vertex_collection(CollectionNames.blocks.name).get(block_id)

    def find_block(self, model_id: str, block: dict):
        model = self.database.graph(model_id)
        return model.vertex_collection(CollectionNames.blocks.name).find(block).pop()

    def change_block(self, model_id: str, block_id: str, new_block: dict):
        model = self.database.graph(model_id)
        new_block["_key"] = block_id
        model.vertex_collection(CollectionNames.blocks.name).replace(new_block)

    def delete_block(self, model_id: str, block_id: str):
        model = self.database.graph(model_id)
        model.vertex_collection(CollectionNames.blocks.name).delete(block_id)

    """

    """

    def add_arrow(self, model_id: str, arrow: dict):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.arrows.name).insert(arrow)

    def get_arrow(self, model_id: str, arrow_id: str):
        model = self.database.graph(model_id)
        return model.edge_collection(CollectionNames.arrows.name).get(arrow_id)

    def find_arrow(self, model_id: str, arrow: dict):
        model = self.database.graph(model_id)
        return model.edge_collection(CollectionNames.arrows.name).find(arrow).pop()

    def change_arrow(self, model_id: str, arrow_id: str, new_arrow: dict):
        model = self.database.graph(model_id)
        new_arrow["_key"] = arrow_id
        model.edge_collection(CollectionNames.arrows.name).replace(new_arrow)

    def delete_arrow(self, model_id: str, arrow_id: str):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.arrows.name).delete(arrow_id)

    """
    """

    def add_nest(self, model_id: str, nest: dict):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.nests.name).insert(nest)

    def get_nest(self, model_id: str, nest_id: str):
        model = self.database.graph(model_id)
        return model.edge_collection(CollectionNames.nests.name).get(nest_id)

    def find_nest(self, model_id: str, nest: dict):
        model = self.database.graph(model_id)
        return model.edge_collection(CollectionNames.nests.name).find(nest).pop()

    def change_nest(self, model_id: str, nest_id: str, new_nest: dict):
        model = self.database.graph(model_id)
        new_nest["_key"] = nest_id
        model.edge_collection(CollectionNames.nests.name).replace(new_nest)

    def delete_nest(self, model_id: str, nest_id: str):
        model = self.database.graph(model_id)
        model.edge_collection(CollectionNames.nests.name).delete(nest_id)

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
        self.__data_base_name = databasename

        client = ArangoClient(hosts=self.__host)
        sys_db = client.db('_system', username=self.__username, password=self.__password)
        if not sys_db.has_database(self.__data_base_name):
            sys_db.create_database(self.__data_base_name)

        self.database = client.db(self.__data_base_name, username=self.__username, password=self.__password)
        if self.database.has_collection("DatabaseInfo"):
            self.collection = self.database.collection("DatabaseInfo")
        else:
            self.collection = self.database.create_collection("DatabaseInfo")

    def get_model(self, model_id: str) -> dict | None:
        return self.collection.get(model_id)

    def create_model(self, model: dict):
        self.collection.insert(model)

    def delete_model(self, model_id: str):
        self.collection.delete(model_id)

    def change_model(self, model: dict):
        self.collection.update_match({'_key': model["_key"]}, model)


archModelGraphDb = ArchModelGraphDb(HOST, ROOT_USERNAME, ROOT_PASSWORD, MODEL_GRAPH_DB_NAME)
archModelInfoDb = ArchModelInfoDb(HOST, ROOT_USERNAME, ROOT_PASSWORD, MODEL_INFO_DB_NAME)
