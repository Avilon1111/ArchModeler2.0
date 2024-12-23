import React, { useEffect, useState } from "react";
import ModelList from "../components/ModelList.jsx";
import "../styles/App.css";
import ModelForm from "../components/ModelForm.jsx";
import ModelFilter from "../components/ModelFilter.jsx";
import MyModal from "../components/UI/MyModal/MyModal.jsx";
import MyButton from "../components/UI/button/MyButton.jsx";
import { useModels } from "../hooks/useModel.js";
import ModelService from "../API/ModelService.jsx";
import Loader from "../components/UI/loader/Loader.jsx";
import { useFetching } from "../hooks/useFetching.js";

function Models() {
  const [models, setModels] = useState([]);
  const [modal, setModal] = useState(false);
  const [modelFilter, setModelFilter] = useState({ sort: "", query: "" });
  const sortedAndSearchedModels = useModels(
    models,
    modelFilter.sort,
    modelFilter.query
  );
  const [fetchModels, isModelsLoading, modelsError] = useFetching(async () => {
    const models = await ModelService.getAll();
    setModels(models);
  });
  // Нижний уровень создания модели
  const createModel = (newModel) => {
    ModelService.postModel(newModel)
    setModels([...models, newModel]);
    setModal(false);
  };


  useEffect(() => {
    fetchModels();
  }, []);

  // Нижний уровень удаления модели
  const removeModel = (model) => {
    ModelService.deleteModel(model.id)
    setModels(models.filter((m) => m.id !== model.id));
  };

  return (
    <div className="App">
      <MyButton style={{marginTop: 30}} onClick={() => setModal(true)}>
        Создать модель
      </MyButton>
      <MyModal visible={modal} setVisible={setModal}>
        <ModelForm create={createModel} />
      </MyModal>
      <hr style={{ margin: "15px 0" }} />
      <ModelFilter filter={modelFilter} setFilter={setModelFilter} />
      {modelsError && <h1>Произошла ошибка</h1>}
      {isModelsLoading ? (
        <div
          style={{ display: "flex", justifyContent: "center", marginTop: 50 }}
        >
          <Loader />
        </div>
      ) : (
        <ModelList
          remove={removeModel}
          models={sortedAndSearchedModels}
          title={"Все модели"}
        />
      )}
    </div>
  );
}

export default Models;
