import React, { useEffect, useState } from "react";
import { useFetching } from "../hooks/useFetching.js";
import { useParams } from "react-router-dom";
import ModelService from "../API/ModelService.jsx";
import Loader from "../components/UI/loader/Loader.jsx";
import ElementsField from "./Field/Field.jsx";

const ModelField = () => {
    const params = useParams();
    const [model, setModel] = useState({});
    const [elements, setElements] = useState({blocks: [], arrows: []});

    const [fetchModelById, isLoading] = useFetching(async (id) => {
        const response = await ModelService.getById(id);
        setModel(response);
    });

    const [fetchElementsById, isElementsLoading] = useFetching(async (id) => {
        const response = await ModelService.getElementsById(id);
        setElements(response);
    });

    useEffect(() => {
        fetchModelById(params.id);
        fetchElementsById(params.id);
    }, []);

    return (
        <div>
            {/* <h1>Вы открыли страницу модели с ID = {params.id}</h1>
            {isLoading ? (
                <Loader />
            ) : (
                <div>
                    {model.id}, {model.name}
                </div>
            )}
            {isElementsLoading ? <Loader /> : 
            <div>
                {
                    elements.blocks.map(block => 
                        <div style={{marginTop: 15}}>
                            <h5>{block.id}</h5>
                        </div>
                    )
                }
            </div>
            } */}
            <ElementsField/>
        </div>
    );
};

export default ModelField;
