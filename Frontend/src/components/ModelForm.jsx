import React, { useState } from "react";
import MyInput from "./UI/input/MyInput";
import MyButton from "./UI/button/MyButton";

const ModelForm = function({create}){
    const [model, setModel] = useState({name: "", author: "", id: 0, info: ""})

    const addNewModel = (e) => {
        e.preventDefault()
        const newModel = {...model, id: (Date.now()).toString()}
        create(newModel)
        setModel({name: "", author: "", id: "", info: ""})
    }
    
    return (
        <form>
        <MyInput 
            value = {model.name} onChange = {e => setModel({...model, name: e.target.value})}
            type = "text" placeholder='Название модели'
        />
        <MyInput 
            value = {model.author} onChange = {e => setModel({...model, author: e.target.value})}
            type = "text" placeholder='Автор модели'
        />
        <MyInput 
            value = {model.info} onChange = {e => setModel({...model, info: e.target.value})}
            type = "text" placeholder='Описание модели'
        />
        <MyButton onClick = {addNewModel}>Создать модель</MyButton>
      </form> 
    )
}

export default ModelForm