import cssclass from "./utils/cssclass.jsx";
import cssstyle from  "./utils/cssclass.jsx";
import dateutil from "./utils/dateutil.jsx";
import domutil from "./utils/domutil.jsx";

const timeOptions = { hour: 'numeric', minute: 'numeric',  hour12: false, weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };

function formatDate(date) {
    return date.toLocaleString('en-US', timeOptions);
}

function formatDateForDebug(date) {
    return date.toISOString();
}

export default {
    formatDate,
    formatDateForDebug,
    cssclass,
    cssstyle,
    dateutil,
    domutil
};
