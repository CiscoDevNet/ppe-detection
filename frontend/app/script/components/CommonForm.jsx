import React from "react";
import CommonDialog from "./CommonDialog";

export default class extends React.Component {

    state = {}

    getJsonData () {
	var form = this.refs.form;
	var data = {};
	this.props.controls.map(control=>{
	    if(control.key){
		data[control.key]=form.querySelector(`#${control.key}`).value;
	    }
	});
	return data;
    }

    getFormData () {
	return new FormData(this.refs.form);
    }

    clearErrorMessage () {
	this.setState({errorMessage: ""});
    }

    render () {
	var props = this.props;
	var data = props.data || {};
	var controls = props.controls || [];
	return (
	    <form {...props} ref="form" className={`form form-common ${props.className||""}`}>
		{this.renderError()}
		{this.renderControls(controls, data)}
		{props.children}
	    </form>
	);
	    
    }

    renderError () {
	if(this.state.errorMessage) {
	    return (
		<div className="alert alert-danger" role="alert">
		    {this.state.errorMessage}
		</div>
	    );
	}
	return null;
    }

    renderControls (controls, data) {
	var items = controls.map(control=>{
	    var comp;
	    switch(control.type) {
		default:
		    if(!control.key) {
			comp = control.render?control.render():control.text;
			break;
		    }
		    // PASS THROUGH
		case "input":
		    comp = (
			<div key={control.key} className="form-group">
			    {control.label && <label htmlFor={control.key}>{control.label}</label>}
			    <input className="form-control" name={control.key} id={control.key} aria-describedby={`desc-${control.key}`} defaultValue={data[control.key]} placeholder={control.placeholder} onChange={this.clearErrorMessage.bind(this)} />
			    {control.description && <small id={`desc-${control.key}`} className="form-text text-muted">{control.description}</small>}
			</div>
		    );
		    break;
		case "input:password":
		    comp = (
			<div key={control.key} className="form-group">
			    {control.label && <label htmlFor={control.key}>{control.label}</label>}
			    <input type="password" className="form-control" name={control.key} id={control.key} defaultValue={data[control.key]} aria-describedby={`desc-${control.key}`} placeholder={control.placeholder} onChange={this.clearErrorMessage.bind(this)} />
			    {control.description && <small id={`desc-${control.key}`} className="form-text text-muted">{control.description}</small>}
			</div>
		    );
		    break;
		case "input:file":
		    comp = (
			<div key={control.key} className="form-group">
			    {control.label && <label htmlFor={control.key}>{control.label}</label>}
			    <input type="file" className="form-control-file" name={control.key} id={control.key} defaultValue={data[control.key]} aria-describedby={`desc-${control.key}`} onChange={this.clearErrorMessage.bind(this)} />
			    {control.description && <small id={`desc-${control.key}`} className="form-text text-muted">{control.description}</small>}
			</div>
		    );
		    break;
		case "textarea":
		    comp = (
			<div key={control.key} className="form-group">
			    {control.label && <label htmlFor={control.key}>{control.label}</label>}
			    {control.description && <small id={`desc-${control.key}`} className="form-text text-muted">{control.description}</small>}
			    <textarea className="form-control" name={control.key} id={control.key} rows="3" defaultValue={data[control.key]} aria-describedby={`desc-${control.key}`} onChange={this.clearErrorMessage.bind(this)}></textarea>
			</div>
		    );
		    break;
		case "select":
		    comp = (
			<div key={control.key} className="form-group">
			    {control.label && <label htmlFor={control.key}>{control.label}</label>}
			    <select className="form-control" name={control.key} id={control.key} defaultValue={data[control.key]} aria-describedby={`desc-${control.key}`} onChange={this.clearErrorMessage.bind(this)}>
				{(control.options||[]).map(option=>(
				     <option key={option.value || option} value={option.value || option}>{option.text || option.value || option}</option>
				 ))}
			    </select>
			    {control.description && <small id={`desc-${control.key}`} className="form-text text-muted">{control.description}</small>}
			</div>
		    );
		    break;
		case "select:multiple":
		    comp = (
			<div key={control.key} className="form-group">
			    {control.label && <label htmlFor={control.key}>{control.label}</label>}
			    <select multiple className="form-control" name={control.key} id={control.key} defaultValue={data[control.key]} aria-describedby={`desc-${control.key}`} onChange={this.clearErrorMessage.bind(this)}>
				{(control.options||[]).map(option=>(
				     <option key={option.value || option} value={option.value || option}>{option.text || option.value || option}</option>
				 ))}
			    </select>
			    {control.description && <small id={`desc-${control.key}`} className="form-text text-muted">{control.description}</small>}
			</div>
		    );
		    break;
		    // TODO more
	    }
	    return comp;
	});
	return items;
    }
}
