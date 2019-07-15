import React from "react";
import "./CommonFilter.scss";
import CommonFilterGroup from "./CommonFilterGroup";

export default class extends React.Component {

    render () {
	var props = this.props;
	var data = props.data || {};
	var items = (props.groups||[]).map(group=>(
	    <CommonFilterGroup key={group.key} config={group} defaultValues={data[group.key]} onChange={newValues=>this.onGroupChange(group.key, newValues)} />
	));
	return (
	    <div className="common-filter">
		{items}
	    </div>
	);
    }

    onGroupChange (key, values) {
	if(this.props.onChange) {
	    this.props.onChange(key, values);
	}
    }
    
}
