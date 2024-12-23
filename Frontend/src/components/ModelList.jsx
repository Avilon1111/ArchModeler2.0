import React from "react";
import Model from "./model.jsx";

const ModelList = function ({ models, title, remove }) {
  if (!models.length) {
    return <h1 style={{ textAlign: "center" }}>Модели не найдены</h1>;
  }
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>{title}</h1>
      {models.map((model) => (
        <Model remove={remove} model={model} />
      ))}
    </div>
  );
};

export default ModelList;
