// import React from 'react'
// import ReactDOM from 'react-dom/client'
// import App from './App.jsx'
// import './index.css'

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
// )

import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider,createBrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './index.css'
 
import './index.css';
import Login from './components/Login/Login.jsx'
import PageNotFound from './components/PageNotFound.jsx'
import Home from './components/Home/Home.jsx'

 
const router = createBrowserRouter([
  {
    index: true,
    element: <Login />,
  },
  {
    path: "*",
    element: <PageNotFound />,
  },
  {
    path: "/home",
    element: <Home />,
  },
]);
ReactDOM.createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
