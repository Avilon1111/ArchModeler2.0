import axios from "axios";

const basePath = "http://127.0.0.1:8089"
export default class ModelService {
    static async getAll() {
        const response = await axios.get(basePath + "/models");
        return response.data;
    }

    static async getById(id) {
        const response = await axios.get(basePath + "/models/" + id);
        return response.data;
    }

    static async postModel(model) {
        const response = await axios.post(basePath + "/models/", {
            "id": model.id,
            "name": model.name,
            "author": model.author,
            "info": model.info
          });
        return response.data
    }

    static async deleteModel(id){
        const response = await axios.delete(basePath + "/models/" + id)
        return response.data
    }

    static async getElementsById(id) {
        const response = await axios.get(
            "http://127.0.0.1:8089/models/" + id + "/elements"
        );
        return response.data;
    }
}
