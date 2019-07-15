import axios from "axios";
import ioclient from "socket.io-client";

var axios_instance = axios.create();

function accessor(method, urlpattern) {
    return function(){
	var vals = Array.prototype.slice.call(arguments);
	var url = urlpattern;
	while(url.indexOf("%s")>=0) {
	    url = url.substring(0, url.indexOf("%s")) + vals.shift() + url.substring(url.indexOf("%s")+2);
	}
	return axios_instance.request({
	    method: method,
	    url: url,
	    data: vals[0]
	});
    }
};

function entity(name) {
    return {
	query: function (query) {
	    var vals = Array.prototype.slice.call(arguments, 1);
	    return accessor("get", `/v1/${name}?${query}`).apply(this, vals);
	},
	send: function (method, suffix) {
	    var vals = Array.prototype.slice.call(arguments, 2);
	    return accessor(method, `/v1/${name}/${suffix}`).apply(this, vals);
	},
	list: accessor("get", `/v1/${name}`),
	create: accessor("post", `/v1/${name}`),
	get: accessor("get", `/v1/${name}/%s`),
	remove:accessor("delete", `/v1/${name}/%s`),
	update: accessor("put", `/v1/${name}/%s`),
	patch: accessor("patch", `/v1/${name}/%s`)
    }
}

var accessors = {
    logs: entity("logs"),
    policies: entity("policys"),
    detections: entity("detections")
};

var io = (()=>{
    var io, regs = {}, listeners = {};
    var connect = (url)=>{
	io = ioclient("/", {
	    transports: ['polling']
	});
	io.on("disconnect", ()=>{
	    console.log("disconnected");
	    connect();
	});
    };
    return (key, callback) => {
	if(!io) {
	    connect();
	}
	if(!regs[key]) {
	    regs[key] = [callback];
	    listeners[key] = (data)=>{
		regs[key].map(c=>c(data));
	    };
	    io.on(key, listeners[key]);
	} else {
	    regs[key].push(callback);
	}
	return {
	    off:()=>{
		regs[key] = regs[key].filter(c=>c!==callback);
		if(!regs[key].length) {
		    io.off(key, listeners[key]);
		}
	    }
	};
    };
})();

export default {
    accessors, io
};
