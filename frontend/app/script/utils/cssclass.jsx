export default (function() {
    return {
        has: function(dom, name) {
            if (dom.classList) {
                return dom.classList.contains(name);
            }
            return (" " + dom.className + " ").indexOf(" " + name + " ") >= 0;
        },
        add: function(dom, name) {
            if (dom.classList) {
                dom.classList.add(name);
                return String(dom.className);
            }
            if (!this.has(dom, name)) {
                dom.className = (dom.className || "") + " " + name;
            }
            return String(dom.className);
        },
        remove: function(dom, name) {
            if (dom.classList) {
                return dom.classList.remove(name);
            }
            // TODO optimizable?
            return dom.className = String(dom.className || "")
                .split(" ")
                .filter(function(cname) {
                    return cname && cname !== name;
                })
                .join(" ");
        },
        toggle: function(dom, name, existance) {
            if (arguments.length > 2) {
                return existance ? this.add(dom, name) : this.remove(dom, name);
            } else {
                if (dom.classList) {
                    return dom.classList.toggle(name);
                } else {
                    if (this.has(dom, name)) {
                        this.remove(dom, name);
                    } else {
                        this.add(dom, name);
                    }
                }
            }
            return null;
        }
    };
})();
