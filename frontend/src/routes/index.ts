import { createBrowserRouter} from "react-router";
import Application from "../components/Application";

const routes = createBrowserRouter([
  {
    path: "/",
    Component: Application
  },
]);

export default routes;