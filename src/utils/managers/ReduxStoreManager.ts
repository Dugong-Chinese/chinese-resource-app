import { applyMiddleware, createStore } from "redux";
import { composeWithDevTools } from "redux-devtools-extension/index";

import thunk from "redux-thunk";
import rootReducer from "../../reducers/index";

const store = createStore(
  rootReducer,
  composeWithDevTools(applyMiddleware(thunk))
);

export default store;
