import React from "react";
import api from "../api";
import PanelLoading from "Components/PanelLoading";

export default class extends React.Component {

    state = {}

    panel_actions = [{
        name:"OK",
        render: ()=>(
            <div className="fas fa-check" title="OK" />
        ),
        action: ()=>{
            var data = this.refs.form.getJsonData();
            api.accessors.deployments.create(data).then(response=>{
                this.close();
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
        window.location.href = `/${CONFIG.BASENAME}/deployments`;
    }
    
    render () {
        if(!this.state.applications || !this.state.clusters) {
            return (
                <PanelLoading />
            );
        }
        var props = this.props;
        var data = props.data || {};
        var controls = [{
            type: "select",
            label: "Application",
            key: "appId",
            options: this.state.applications.map(item=>({value:item.id, text:`${item.name} - ${item.version}`})),
        },{
            type: "select",
            label: "Cluster",
            key: "clusterId",
            options: this.state.clusters.map(item=>({value:item.id, text:item.name})),
        }];
        return (
            <PanelWithAction title={props.title} actions={this.panel_actions}>
                <CommonForm ref="form" controls={controls} data={data} />
            </PanelWithAction>
        );
    }

    componentDidMount () {
        api.accessors.clusters.list().then(response=>{
            this.setState({clusters:response.data});
        });
        api.accessors.applications.list().then(response=>{
            this.setState({applications:response.data});
        });
    }
}
