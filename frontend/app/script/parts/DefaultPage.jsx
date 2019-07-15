import React from "react";
import PropTypes from "prop-types";
import utils from "utils";
import api from "../api";
import DefaultHeader from "Parts/DefaultHeader";
import CommonContainer from "Components/CommonContainer";
import PanelLoading from "Components/PanelLoading";
import "./DefaultPage.scss";

export default class extends React.Component {

    static childContextTypes = {
	credential: PropTypes.any
    }

    getChildContext () {
	return {
	    credential: this.state.credential
	};
    }
    
    state = {}
    
    render () {
	if(!this.props.public || this.props.public==="false") {
	    if(this.state.credential===undefined) {
		return (
		    <CommonContainer>
			<PanelLoading />
		    </CommonContainer>
		)
	    }
	    if(!this.state.credential) {
		window.location.href = `/${CONFIG.BASENAME}/login?pending=${window.location.href}`;
	    }
	    if(this.state.error) {
		window.location.href = `/${CONFIG.BASENAME}/error`;
	    }
	}
	return (
	    <div {...this.props} className={`page page-${this.props.pagename}`}>
		<DefaultHeader />
		<CommonContainer>
		    {this.props.children}
		</CommonContainer>
	    </div>
	);
    }

    componentDidMount () {
	if(!this.props.public || this.props.public==="false") {
	    // TODO Login
	    api.accessors.users.send("get", "me").then(response=>(
		this.setState({credential: response.data})
	    )).catch(error=>{
		this.setState({credential: false});
	    });
	}
    }
}
