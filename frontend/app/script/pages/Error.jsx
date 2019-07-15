import React from "react";

export default class extends React.Component {
    render() {
        const homeUrl = `/${CONFIG.BASENAME}`;
        return (
            <div id="dn-404-page" className="container">
                <a href={homeUrl}>Go to Homepage</a>
            </div>
        );
    }
}
