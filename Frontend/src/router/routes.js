import ModelField from "../pages/ModelField";
import Models from "../pages/Models";

const routes = [
    {path: "/models", component: Models, exact: true},
    {path: "/models/:id", component: ModelField, exact: true}
]

export default routes