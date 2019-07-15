var browser;

if(window) {
    var document = window.document;
    var ua = window.navigator.userAgent.toLowerCase();
    var os = (function() {
	var os, patterns = {
            "windows": /windows|win32/,
            "macintosh": /macintosh|mac_powerpc/,
            "linux": /linux/
	};
	for (os in patterns) {
            if (patterns[os].test(ua)) {
		return os;
            }
	}
	return "other";
    })();

    var browser = (function() {
	var getVersionByPrefix = function(prefix) {
            var match = new RegExp(prefix + '(\\d+\\.\\d+)').exec(ua);
            return match ? parseFloat(match[1]) : 0;
	};
	var browser, browsers = [{
            tests: [/msie/, /^(?!.*opera)/],
            name: "ie",
            version: getVersionByPrefix("msie "),
            prefix: "ms", // not checked
            cssPrefix: "-ms-",
            engine: {
		name: "trident",
		version: getVersionByPrefix("trident\\/") || 4
            }
	}, {
            tests: [/gecko/, /^(?!.*webkit)/],
            name: "firefox",
            version: getVersionByPrefix("\\bfirefox\/"),
            prefix: "Moz",
            cssPrefix: "-moz-",
            engine: {
		name: "gecko",
		version: getVersionByPrefix("rv:") || 4
            }
	}, {
            tests: [/\bchrome\b/],
            name: "chrome",
            version: getVersionByPrefix('\\bchrome\/'),
            prefix: "webkit",
            cssPrefix: "-webkit-",
            engine: {
		name: 'webkit',
		version: getVersionByPrefix('webkit\\/')
            }
	}, {
            tests: [/safari/, /^(?!.*\bchrome\b)/],
            name: "safari",
            version: getVersionByPrefix('version\/'),
            prefix: "webkit",
            cssPrefix: "-webkit-",
            engine: {
		name: 'webkit',
		version: getVersionByPrefix('webkit\\/')
            }
	}, {
            tests: [/opera/],
            name: "opera",
            version: getVersionByPrefix('version\/'),
            prefix: "O",
            cssPrefix: "-o-",
            engine: {
		name: getVersionByPrefix("presto\\/") ? "presto" : "webkit",
		version: getVersionByPrefix("presto\\/") || getVersionByPrefix("webkit\\/")
            }
	}];
	// do browser determination one by one
	while (browsers.length) {
            browser = browsers.shift();
            while (browser.tests.length) {
		if (!browser.tests[0].test(ua)) {
                    break;
		}
		browser.tests.shift();
            }
            if (browser.tests.length) {
		continue;
            }
            delete browser.tests;
            return browser;
	}
	return {
            name: "other",
            version: 0,
            engine: {
		name: "unknown",
		version: 0
            }
	};
    })();
}

export default {
    browser: browser
};
