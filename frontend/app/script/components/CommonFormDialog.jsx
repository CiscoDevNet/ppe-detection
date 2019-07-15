import React from "react";
import "./CommonFormDialog.scss";
import CommonDialog from "./CommonDialog";
import CommonForm from "./CommonForm";

export default class extends React.Component {

    actions = [{
	name:"OK",
	render: itemdata=>(
	    <div className="fas fa-check" title="OK" />
	),
	action: ()=>{
	    // TODO
	    var data;
	    data = {};
	    this.props.controls.map(control=>{
		if(control.key) {
		    data[contorl.key] = this.refs.form.querySelector(`#${control.key}`).value;
		}
	    });
	    this.props.onSubmit(data, new FormData(this.refs.form), ()=>this.setProps({visible:false}));
	}
    }, {
	name:"Cancel",
	render: itemdata=>(
	    <div className="fas fa-times" title="Cancel" />
	),
	action: ()=>{
	    this.setProps({visible:false});
	}
    }];

    render () {
	var props = this.props;
	return (
	    <CommonDialog className="common-form-dialog" visible={props.visible} title={props.title} className={props.className} style={props.style}>
		<CommonForm ref="form" controls={props.controls} />
	    </CommonDialog>
	);
    }
}
