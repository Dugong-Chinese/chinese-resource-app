export const UI_STATE_ACTIONS = {
};

type UIStateReducerAction = {
  type: string;
};

const initialState = {
};

export const uiStateReducer = (
  state = initialState,
  action: UIStateReducerAction
) => {
  switch (action.type) {
    default:
      return state;
  }
};
