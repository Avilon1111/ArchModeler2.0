import React from "react";
import MyButton from "./UI/button/MyButton";
import { useNavigate } from 'react-router-dom';

const Model = function (props) {
    const navigate = useNavigate()
  
  return (
    <div className="model">
      <div className="model__info">
        <div className="model__name">{props.model.name}</div>
        <div>{props.model.author}</div>
        <div>{props.model.id}</div>
      </div>
      <div className="model__btns">
        <MyButton onClick={() => {navigate((props.model.id))}}>Открыть</MyButton>
        <MyButton onClick={() => props.remove(props.model)}>Удалить</MyButton>
      </div>
    </div>
  );
};

export default Model;
