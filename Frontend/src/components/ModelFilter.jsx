import React from "react";
import MySelect from "./UI/select/MySelect";
import MyInput from "./UI/input/MyInput";

const ModelFilter = ({filter, setFilter}) => {
    return (
        <div>
            <MyInput
                value = {filter.query}
                onChange = {e => setFilter({...filter, query: e.target.value})}
                placeholder = "Поиск..."
            />
            <MySelect 
                value={filter.sort}
                onChange={selectedSort => setFilter({...filter, sort: selectedSort})}
                defaultValue="Сортировка" 
                options={[
                    {value: 'name', name: 'По названию'}, 
                    {value: 'author', name: 'По автору'},
                ]}           
            />
        </div>
    )
}

export default ModelFilter