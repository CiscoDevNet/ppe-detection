import urlparse from "url-parse";

import "./domutil.scss";
import cssclass from "./cssclass.jsx";

var util = {
    parseURL: function(url) {
        var result = urlparse(url);
	// Got [protocol, slashes, auth, username, password, host, hostname, port, pathname, query, hash, href, origin]
        result.search = (result.query ? result.query.substring(1) : "").split("&").reduce(function(data, arg) {
            var key, value, idx = arg.indexOf("=");
            // check if value given
            if (idx >= 0) {
                key = decodeURI(arg.substring(0, idx));
                value = decodeURI(arg.substring(idx + 1));
            } else {
                key = decodeURI(arg);
                value = true;
            }
            // mark the key
            if (key) {
                data[key] = value;
            }
            return data;
        }, {});
        result.hash = (result.hash || "").split("&").map(function(arg, order) {
            var key, value, idx = arg.indexOf("=");
            if (order === 0) {
                if (!arg) {
                    return ["#", null];
                }
                if (idx == -1) {
                    return ["#", decodeURI(arg.substring(1))];
                }
                arg = arg.substring(1);
            }
            // normal key-value pair
            idx = arg.indexOf("=");
            if (idx >= 0) {
                key = decodeURI(arg.substring(0, idx));
                value = decodeURI(arg.substring(idx + 1));
            } else {
                key = decodeURI(arg);
                value = null;
            }
            return [key, value];
        }).reduce(function(data, pair) {
            data[pair[0]] = pair[1];
            return data;
        }, {});
	result.location = (function(url){
	    if(url.indexOf("#")>=0){
		url = url.substring(0, url.indexOf("#"));
	    }
	    if(url.indexOf("?")>=0) {
		url = url.substring(0, url.indexOf("?"));
	    }
	    return url;
	})(url);
	result.action = result.location.substring(result.location.lastIndexOf("/")+1);
        return result;
    }
};

var URL = util.parseURL(window.location.href);

export default {
    URL: URL,
    parseURL: util.parseURL,
    isDemo: ()=>(URL.search["DEMO"]===true),
    fold: function(target, out, callback) {
        var height;
        if (out) {
            height = target.clientHeight;
            target.style.height = "0px";
            target.style.overflow = "hidden";
            setTimeout(function() {
                target.style.transition = "height .3s";
                setTimeout(function() {
                    target.style.height = height + "px";
                    setTimeout(function() {
                        target.style.removeProperty("overflow");
                        target.style.removeProperty("height");
                        target.style.removeProperty("transition");
                        callback();
                    }, 300);
                }, 0);
            }, 0);
        } else {
            height = target.clientHeight;
            target.style.overflow = "hidden";
            target.style.height = height + "px";
            setTimeout(function() {
                target.style.transition = "height .3s";
                setTimeout(function() {
                    target.style.height = "0px";
                    setTimeout(function() {
                        target.style.removeProperty("overflow");
                        target.style.removeProperty("height");
                        target.style.removeProperty("transition");
                        callback();
                    }, 300);
                }, 0);
            }, 0);
        }
    },
    withPopup: function(callback, target) {
        var container = document.createElement("div");
        cssclass.toggle(container, "dialog-container", true);
        var mask = document.createElement("div");
        cssclass.toggle(mask, "dialog-mask", true);
        container.appendChild(mask);
        var box = document.createElement("div");
        cssclass.toggle(box, "dialog-box", true);
        container.appendChild(box);
        container.box = box;
        var actions = {
            open: function() {
                (target || document.body).appendChild(container);
            },
            close: function() {
                container.parentNode.removeChild(container);
            }
        };
        actions.open();
        callback(container, actions.close);
        return actions;
    }
};
