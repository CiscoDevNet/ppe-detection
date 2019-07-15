import React from "react";
import "./PanelWithAction.scss";

export default class extends React.Component {
    render () {
	var actions = (this.props.actions||[]).filter(action=>action.visible!==false);
	return (
	    <div className={`panel-with-action ${this.props.className}`}>
		<div className="panel-header row">
		    <div className="panel-title col">{this.props.title}</div>
		    <div className="panel-actions col">
			{actions.map(action=>{
			     var enabled = !action.isDisabled || !action.isDisabled();
			     return (
				 <div key={action.name}
				      className={`btn btn-link pt-0 pb-0 pr-0 ${enabled?"":"disabled"}`}
				      onClick={()=>(enabled && action.action())}>
				     {action.render?action.render():action.name}
				 </div>
			     );
			 })}
		    </div>
		</div>
		<div className="panel-body">
		    {this.props.children}
		</div>
	    </div>
	);
    }
}
