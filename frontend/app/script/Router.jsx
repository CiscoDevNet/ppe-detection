import React from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import Error from "./pages/Error";
import Show from "./pages/Show";
import Admin from "./pages/Admin";

export default class Root extends React.Component {
    componentWillReceiveProps(nextProps) {
        if (nextProps.location !== this.props.location) {
            AnalyticsSDK.trackPageView();
        }
    }
    render() {
        return (
            <Switch>
                <Route path="/404" component={Error} exact />
                <Route path="/" component={Show} exact />
                <Route path="/show" component={Show} exact />
                <Route path="/admin" component={Admin} exact />
                <Redirect from="*" to="/404" />
            </Switch>
        );
    }
}
