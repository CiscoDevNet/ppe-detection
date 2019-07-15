import React from "react";
import utils from "utils";
import api from "../api";
import PanelLoading from "Components/PanelLoading";
import CommonFilter from "Components/CommonFilter";
import DefaultPage from "Parts/DefaultPage";
import PanelLogs from "Parts/PanelLogs";
import DEMO from "./DEMO.json";

export default class extends React.Component {

    state = {filter_selections: {}, logs:[]}

    filter_groups = [{
	"key": "cameraId",
	"text": "Camera",
	"options": [{
            "value": "camera1",
            "text": "Camera 1"
	}, {
            "value": "camera2",
            "text": "Camera 2"
	}, {
            "value": "camera3",
            "text": "Camera 3"
	}]
    }, {
	"key": "status",
	"text": "Warning level",
	"multiple": true,
	"options": [{
            "value": 0,
            "text": "None"
	}, {
            "value": 1,
            "text": "Missing vest"
	}, {
            "value": 2,
            "text": "Missing hardhat"
	}, {
            "value": 3,
            "text": "Missing both"
	}]
    }]
    
    render () {
	var logs = this.state.logs.map(log=>{
	    log.bound = log.cameraId==="camera1"?["10%", "10%", "30%", "50%"]:["60%", "20%", "15%", "20%"];
	    log.highlight = this.testHighlight(log);
	    return log;
	});
	return (
            <DefaultPage public="true">
		<div className="row">
		    <div className="col col-12 col-md-3">
                        <CommonFilter groups={this.filter_groups} data={this.state.filter_selections} onChange={(key,values)=>this.onFilterChange(key,values)} />
                    </div>
		    <div className="col col-12 col-md-9">
			<PanelLogs data={logs} />
		    </div>
		</div>
            </DefaultPage>
	);
    }

    testHighlight (log) {
	return this.filter_groups.map(group=>{
	    var selections = this.state.filter_selections[group.key] || [];
	    if(!selections.length) {
		return true;
	    } else {
		if(log.id==="uuid20")console.log(log, selections, group, !!selections.find(selection=>log[group.key]===selection));
		return selections.findIndex(selection=>log[group.key]===selection)>=0;
	    }
	}).reduce((x,y)=>x&&y, true);
    }

    onFilterChange (key, values) {
	var filter_selections = {};
	this.filter_groups.map(group=>{
	    filter_selections[group.key] = (group.key===key?values:this.state.filter_selections[group.key]) || [];
	});
	this.setState({filter_selections:filter_selections});
    }

    clearLogs (logs) {
	logs = logs.reduce((list, item)=>{
	    if(!list.find(i=>i.id===item.id)) {
		list.push(item);
	    }
	    return list;
	}, []);
	return logs.slice(0, 40);
    }

    componentDidMount () {
	// fetch TOP 10 history
	api.accessors.detections.query("limit=%s", "10").then(result=>{
	    this.setState({logs:this.clearLogs(this.state.logs.concat(result.data))});
	});
	this._io = api.io("detection", result=>{
	    console.log(result);
	    if(result) {
		this.setState({logs:this.clearLogs([result].concat(this.state.logs))});
	    }
	});
    }

    componentWillUnmount () {
	this._io.off();
    }
    
};
