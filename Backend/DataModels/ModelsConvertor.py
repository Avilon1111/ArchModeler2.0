from DataModels.ApiModels import Model, Block, Arrow, Nest
from DataModels.DbModels import CollectionNames
from copy import deepcopy


class ModelConvertor:

    @staticmethod
    def model_to_dict(model: Model) -> dict:
        """
        required attribute "id"
        """
        model_dict = model.model_dump()

        model_dict["_key"] = model_dict["id"]
        del model_dict["id"]

        return model_dict

    @staticmethod
    def model_to_api(model: dict) -> Model:
        """
        required attribute "_key"
        """
        model_dict = deepcopy(model)

        model_dict["id"] = model_dict["_key"]
        del model_dict["_key"]

        model_API = Model(**model_dict)
        return model_API


    @staticmethod
    def block_to_dict(block: Block) -> dict:
        """
        Optional attribute "id"
        """

        block_dict = block.model_dump()

        if "id" in block_dict.keys():
            if block_dict["id"] != "":
                block_dict["_key"] = block_dict["id"]
            del block_dict["id"]

        return block_dict

    @staticmethod
    def block_to_api(block: dict) -> Block:
        """
        Optional attribute "_key"
        """
        block_dict = deepcopy(block)

        if "_key" in block_dict.keys():
            if block_dict["_key"] != "":
                block_dict["id"] = block_dict["_key"]
            del block_dict["_key"]

        block_API = Block(**block_dict)
        return block_API


    @staticmethod
    def arrow_to_dict(arrow: Arrow) -> dict:
        """
        Optional attribute "id"
        """

        arrow_dict = arrow.model_dump()

        if "id" in arrow_dict.keys():
            if arrow_dict["id"] != "":
                arrow_dict["_key"] = arrow_dict["id"]
            del arrow_dict["id"]

        arrow_dict["_from"] = CollectionNames.arrows + "/" + arrow_dict["from_element"]
        del arrow_dict["from_element"]

        arrow_dict["_to"] = CollectionNames.arrows + "/" + arrow_dict["to_element"]
        del arrow_dict["to_element"]

        return arrow_dict

    @staticmethod
    def arrow_to_api(arrow: dict) -> Arrow:
        """
        Optional attribute "_key"
        """
        arrow_dict = deepcopy(arrow)

        if "_key" in arrow_dict.keys():
            if arrow_dict["_key"] != "":
                arrow_dict["id"] = arrow_dict["_key"]
            del arrow_dict["_key"]

        arrow_dict["from_element"] = arrow_dict["_from"][len(CollectionNames.arrows) + 1:]
        del arrow_dict["_from"]

        arrow_dict["to_element"] = arrow_dict["_to"][len(CollectionNames.arrows) + 1:]
        del arrow_dict["_to"]

        arrow_API = Arrow(**arrow_dict)
        return arrow_API



    @staticmethod
    def nest_to_dict(nest: Nest) -> dict:
        """
        Optional attribute "id"
        """

        nest_dict = nest.model_dump()

        if "id" in nest_dict.keys():
            if nest_dict["id"] != "":
                nest_dict["_key"] = nest_dict["id"]
            del nest_dict["id"]

        nest_dict["_from"] = CollectionNames.nests + "/" + nest_dict["from_element"]
        del nest_dict["from_element"]

        nest_dict["_to"] = CollectionNames.nests + "/" + nest_dict["to_element"]
        del nest_dict["to_element"]

        return nest_dict


    @staticmethod
    def nest_to_api(nest: dict) -> Nest:
        """
        Optional attribute "_key"
        """
        nest_dict = deepcopy(nest)

        if "_key" in nest_dict.keys():
            if nest_dict["_key"] is not None:
                nest_dict["id"] = nest_dict["_key"]
            del nest_dict["_key"]

        nest_dict["from_element"] = nest_dict["_from"][len(CollectionNames.nests) + 1:]
        del nest_dict["_from"]

        nest_dict["to_element"] = nest_dict["_to"][len(CollectionNames.nests) + 1:]
        del nest_dict["_to"]

        nest_API = Nest(**nest_dict)
        return nest_API
