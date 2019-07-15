import React from "react";
import api from "../api";
import PanelLoading from "Components/PanelLoading";
import PanelWithAction from "Components/PanelWithAction";
import CommonForm from "Components/CommonForm";

export default class extends React.Component {

    state = {}

    panel_actions = [{
	name:"OK",
	render: ()=>(
	    <div className="fas fa-check" title="OK" />
	),
	action: ()=>{
	    var data = this.refs.form.getJsonData();
	    var request = this.getRequest(data);
	    request.then(response=>{
		this.close();
	    }).catch(error=>{
		var response = error.response || {};
		switch(response.status) {
		    case 400:
			this.setErrorMessage(response.data.message);
			break;
		    case 401:
			window.location.href = `/${CONFIG.BASENAME}/login?pending=${window.location.href}`
			break;
		    case 500:
			this.setErrorMessage("Service internal error");
			break;
		    default:
			this.setErrorMessage("Unknown error");
			break;
		}
	    });
	}
    }, {
	name:"Cancel",
	render: itemdata=>(
	    <div className="fas fa-times" title="Cancel" />
	),
	action: ()=>{
	    this.close();
	}
    }]

    close () {
	window.location.href = this.getReturnUrl();
    }

    setErrorMessage (message) {
	this.refs.form.setState({errorMessage: message});
    }

    getRequest () {
	// TO BE OVERRIDE
	return {};
    }

    getControls () {
	// TO BE OVERRIDE
	return [];
    }

    getReturnUrl () {
	// TO BE OVERRIDE
	return window.location.href;
    }

    isReady () {
	// TO BE OVERRIDE
	return true;
    }
    
    render () {
	if(this.state.errorMessage) {
	    return (
		<div className="alert alert-danger" role="alert">
		    {this.state.errorMessage}
		</div>
	    );
	}
	if(!this.isReady()) {
	    return (
		<PanelLoading />
	    );
	}
	return (
	    <PanelWithAction className="panel-user-form" title={this.props.title} actions={this.panel_actions}>
		<CommonForm ref="form" controls={this.getControls()} data={this.props.data} />
	    </PanelWithAction>
	);
    }
}
