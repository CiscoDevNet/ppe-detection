import React from "react";
import "./CommonFilterGroup.scss";

export default class extends React.Component {

    state = {
	selections: null
    }

    getSelections () {
	return (this.state.selections || this.getDefaultSelections() || []);
    }

    getDefaultSelections () {
	return (this.props.defaultValues||[]).map(value=>this.props.config.options.find(option=>option.value===value));
    }

    toggleSelection (selection) {
	var selections = this.getSelections().slice();
	var idx = selections.findIndex(item=>item.value===selection.value);
	if(idx>=0) {
	    selections.splice(idx, 1);
	} else {
	    if(this.props.config.multiple) {
		selections.push(selection);
	    } else{
		selections = [selection];
	    }
	}
	this.setState({selections:selections});
	if(this.props.onChange) {
	    this.props.onChange(selections.map(item=>item.value));
	}
    }
    
    render () {
	var props = this.props;
	var selections = this.getSelections();
	var items = props.config.options.map(option=>{
	    var isSelected = !!selections.find(selection=>option.value===selection.value);
	    return (
		<div key={option.value} className={isSelected?"option option-selected":"option"} onClick={()=>this.toggleSelection(option)}>
		    <div className={`fas toggle ${isSelected?"fa-check-square":"fa-square"}`}></div>
		    {option.text}
		</div>
	    );
	});
	return (
	    <div className="common-filter-group">
		<div className="title">{props.config.text}</div>
		{items}
	    </div>
	);
    }
}
