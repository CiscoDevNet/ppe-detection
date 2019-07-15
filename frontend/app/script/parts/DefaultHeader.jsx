import React from "react";
import PropTypes from "prop-types";
import utils from "utils";
import "./DefaultHeader.scss";

export default class extends React.Component {

    static contextTypes = {
	credential: PropTypes.any
    }
    
    render (props) {
	var navs = [{
	    path: "show",
	    icon: "history"
	}];
	navs = navs.filter(nav=>nav.visible!==false);
	var path = utils.domutil.URL.pathname.replace(new RegExp(`^/${CONFIG.BASENAME}/([^/]*).*$`), "$1");
	var items = navs.map(nav=>(
	    <a key={nav.path} className={`text-decoration-none fas fa-${nav.icon} nav-item nav-item-${nav.path===path}`} href={`/${CONFIG.BASENAME}/${nav.path}`}>
		&nbsp;{nav.text || nav.path}
	    </a>
	));
	return (
	    <div className="header default-header">
		<div className="container">
		    {items}
		</div>
	    </div>
	);
    }
};
