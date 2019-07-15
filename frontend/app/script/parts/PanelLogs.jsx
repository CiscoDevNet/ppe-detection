import React from "react";
import utils from "utils";
import api from "../api";
import "./PanelLogs.scss";
import PanelLogsItem from "Parts/PanelLogsItem";

export default class extends React.Component {

    render () {
	var props = this.props;
	var items = (props.data||[]).map(item=>(
	    <PanelLogsItem className="col col-12 col-md-4" key={item.id} data={item} />
	));
	return (
	    <div className="panel panel-logs row">
		{items}
	    </div>
	);
    }

};
