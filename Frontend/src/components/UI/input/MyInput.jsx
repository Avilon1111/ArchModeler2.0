import React from "react";
import classes from "./MyInput.module.css"
const MyInput = function(props) {
    return(
        <input className={classes.myInput} {...props}/>
    )
}

export default MyInput