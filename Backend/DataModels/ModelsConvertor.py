from DataModels.ApiModels import Model, Block, Arrow, Nest
from DataModels.DbModels import JSON, CollectionNames

"""
У JSON всегда есть поле "_key"
"""


class ModelConvertor:


    @staticmethod

    @staticmethod
    def convert_model_to_api(model: JSON) -> Model:
        model["model_id"] = model["_key"]
        del model["_key"]
        ret = Model(**model)
        return ret

    @staticmethod
    def convert_block_to_api(block: JSON) -> Block:
        block["id"] = block["_key"]
        del block["_key"]
        ret = Model(**block)
        return ret

    @staticmethod
    def convert_arrow_to_api(arrow: JSON) -> Arrow:
        arrow["id"] = arrow["_key"]
        del arrow["_key"]
        arrow["from_element"] = arrow["_from"][len(CollectionNames.arrows):]
        del arrow["_from"]
        arrow["to_element"] = arrow["_to"][len(CollectionNames.arrows):]
        del arrow["_to"]
        ret = Model(**arrow)
        return ret

    @staticmethod
    def convert_nest_to_api(nest: JSON) -> Nest:
        return ModelConvertor.api_convertor(nest)

    @staticmethod
    def convert_model_to_db(model: Model) -> JSON:
        ret = model.dict()
        if ret["model_id"] == "":
            del ret["model_id"]
        if "model_id" in ret.keys():
            ret["_key"] = ret["model_id"]
            del ret["model_id"]
        return ret

    @staticmethod
    def convert_block_to_db(block: Block) -> JSON:
        ret = block.dict()
        if ret["id"] == "":
            del ret["id"]
        if "id" in ret.keys():
            ret["_key"] = ret["id"]
            del ret["id"]
        return ret

    @staticmethod
    def convert_arrow_to_db(arrow: Arrow) -> JSON:
        ret = arrow.dict()
        if ret["id"] == "":
            del ret["id"]
        if "id" in ret.keys():
            ret["_key"] = ret["id"]
            del ret["id"]
        if "from_element" in ret.keys():
            ret["_from"] = CollectionNames.blocks + "/" + ret["from_element"]
            del ret["from_element"]
        if "to_element" in ret.keys():
            ret["_to"] = CollectionNames.blocks + "/" + ret["to_element"]
            del ret["to_element"]
        return ret

    @staticmethod
    def convert_nest_to_db(nest: Nest) -> JSON:
        ret = nest.dict()
        if ret["id"] == "":
            del ret["id"]
        if "id" in ret.keys():
            ret["_key"] = ret["id"]
            del ret["id"]
        if "from_element" in ret.keys():
            ret["_from"] = CollectionNames.blocks + "/" + ret["from_element"]
            del ret["from_element"]
        if "to_element" in ret.keys():
            ret["_to"] = CollectionNames.blocks + "/" + ret["to_element"]
            del ret["to_element"]
        return ret
