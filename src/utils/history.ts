// eslint-disable-next-line import/no-extraneous-dependencies
import { createBrowserHistory } from 'history';
import { Config } from './Config';

const history = createBrowserHistory({ basename: Config.routerBase });

export default history;
