import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import { Components } from 'dui';
import "bootstrap/scss/bootstrap.scss";
import { BrowserRouter, Router, Route } from 'react-router-dom';
import { createBrowserHistory } from "history";
import Root from './Router';


const hist = createBrowserHistory({ basename: CONFIG.BASENAME });
const { SocialLoginHeader, BaseFooter } = Components;

const render = (Component) => {
    ReactDOM.render(
        <AppContainer>
            <div>
                <SocialLoginHeader />
                <BrowserRouter>
                    <Router history={hist}>
                        <Route path="/" component={Component} key="index" />
                    </Router>
                </BrowserRouter>
                <BaseFooter />
            </div>
        </AppContainer>,
        document.getElementById('root'),
    );
};

render(Root);

if (module.hot) {
    module.hot.accept('./Router', () => {
        const newApp = require('./Router').default;
        render(newApp);
    });
}
