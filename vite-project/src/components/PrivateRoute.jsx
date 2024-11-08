// import React from 'react';
// import { Navigate } from 'react-router-dom';

// const PrivateRoute = ({ element: Element, ...rest }) => {
//   // Проверка наличия токена в localStorage
//   const isAuthenticated = !!localStorage.getItem('access_token');

//   return isAuthenticated ? (
//     <Element {...rest} />
//   ) : (
//     <Navigate to="/login" replace />
//   );
// };

// export default PrivateRoute;
import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element: Element, ...rest }) => {
  const isAuthenticated = !!localStorage.getItem('access_token');
  return isAuthenticated ? <Element {...rest} /> : <Navigate to="/login" />;
};

export default PrivateRoute;
