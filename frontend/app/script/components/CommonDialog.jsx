import React from "react";
import "./CommonDialog.scss";

export default class extends React.Component {

    resizer (size) {
	
    }
    
    render () {
	return (
	    <div className={`common-dialog visible-${this.props.visible}`}>
		<div className="common-dialog-mask" />
		<div className={`common-dialog-container ${this.props.className}`} style={this.props.style}>
		    <div className="panel-header row">
			<div className="panel-title col">{this.props.title}</div>
			<div className="panel-actions col">
			    {(this.props.actions||[]).map(action=>{
				 var enabled = !action.isDisabled || !action.isDisabled(dataitem);
				 var classDisable = enabled?"":"disabled";
				 return (
				     <div key={action.name}
					  className={`btn btn-link pt-0 pb-0 pr-0 ${classDisable}`}
					  onClick={()=>enabled && action.action(dataitem)}>
					 {action.render?action.render(dataitem):action.name}
				     </div>
				 );
			     })}
			</div>
		    </div>
		    <div className="panel-body">
			{this.props.children}
		    </div>
		</div>
	    </div>
	);
    }
    
    componentDidMount () {
	
    }

    componentWillUnmount () {
	
    }
}
