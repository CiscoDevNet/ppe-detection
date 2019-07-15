import React from "react";
import "./PanelLogsItem.scss";
import pictureMap from "../../assets/images/map.svg";
import pictureArchived from "../../assets/images/archived.png";

export default class extends React.Component {
    render (props) {
	var props = this.props;
	var data = props.data;
	return (
	    <div className={`${props.className} panel-logs-item highlight-${data.highlight}`}>
		<img className="picture" src={this.getRealImageUrl(data.image.url)} onClick={()=>this.showImage(data.image)} onError={(e)=>{e.target.onerror = null; if(e.target.src!==pictureArchived)e.target.src=pictureArchived}} />
		<div className="map-container">
		    <img className="map" src={pictureMap} onClick={()=>this.showImage(data.image)} />
		    <div className="area" style={{left:`${data.bound[0]}`, top:`${data.bound[1]}`, width: `${data.bound[2]}`, height: `${data.bound[3]}`}} />
		</div>
		<div className="detail">
		    <span className="icon icon-0">{data.persons.filter(v=>v.hardhat&&v.vest).length}</span>
		    <span className="icon icon-1">{data.persons.filter(v=>v.hardhat&&!v.vest).length}</span>
		    <span className="icon icon-2">{data.persons.filter(v=>!v.hardhat&&v.vest).length}</span>
		    <span className="icon icon-3">{data.persons.filter(v=>!v.hardhat&&!v.vest).length}</span>
		</div>
	    </div>
	);
    }

    getRealImageUrl (url) {
	return `/v1/images/${url.substring(url.lastIndexOf("/")+1)}`;
    }

    showImage (image) {
	window.open(this.getRealImageUrl(image.url));
    }
};
