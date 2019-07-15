export default (function () {
    var weeks = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var monthsShort = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];
    var padZero = function (inString) {
        return ("00" + inString).slice(-2);
    };
    var selector = {
        "yyyy": function (date) {
            return date.getFullYear();
        },
        "yy": function (date) {
            return date.getFullYear().toString().slice(-2);
        },
        "MMMM": function (date) {
            return months[date.getMonth()];
        },
        "MMM": function (date) {
            return monthsShort[date.getMonth()];
        },
        "MM": function (date) {
            return padZero(date.getMonth() + 1);
        },
        "M": function (date) {
            return date.getMonth() + 1;
        },
        "dd": function (date) {
            return padZero(date.getDate());
        },
        "d": function (date) {
            return date.getDate();
        },
        "hh": function (date) {
            var h = date.getHours();
            return h === 12 ? "12" : padZero(h % 12);
        },
        "h": function (date) {
            var h = date.getHours();
            return h === 12 ? "12" : (h % 12);
        },
        "P": function (date) {
            return date.getHours() < 12 ? "AM" : "PM";
        },
        "HH": function (date) {
            return padZero(date.getHours());
        },
        "H": function (date) {
            return date.getHours();
        },
        "mm": function (date) {
            return padZero(date.getMinutes());
        },
        "m": function (date) {
            return date.getMinutes();
        },
        "ss": function (date) {
            return padZero(date.getSeconds());
        },
        "s": function (date) {
            return date.getSeconds();
        },
        "DDDD": function (date) {
            return weeks[date.getDay()];
        },
        "DDD": function (date) {
            return weeks[date.getDay()].substring(0, 3);
        },
        "D": function (date) {
            return date.getDay();
        }
    };
    return {
        now: Date.now,
        /**
         * A Date format function.
         * <table>
         * <tr><th>place holder</th><th>explain</th><th>example</th></tr>
         * <tr><td>yyyy</td><td>Full year</td><td>1970</td></tr>
         * <tr><td>yy</td><td>Short year</td><td>70</td></tr>
         * <tr><td>MMMM</td><td>Full month</td><td>January</td></tr>
         * <tr><td>MMM</td><td>Short month</td><td>Jan</td></tr>
         * <tr><td>MM</td><td>Month with pad 0</td><td>01</td></tr>
         * <tr><td>M</td><td>Month</td><td>1</td></tr>
         * <tr><td>dd</td><td>Day of month with pad 0</td><td>01</td></tr>
         * <tr><td>d</td><td>Day of month</td><td>1</td></tr>
         * <tr><td>hh</td><td>Hour in 12 with pad 0</td><td>00 or 12</td></tr>
         * <tr><td>h</td><td>Hour in 12</td><td>0 or 12</td></tr>
         * <tr><td>P</td><td>Period(AM/PM)</td><td>AM</td></tr>
         * <tr><td>HH</td>Hour in 24 with pad 0<td></td><td>00</td></tr>
         * <tr><td>H</td><td>Hour in 24</td><td>0</td></tr>
         * <tr><td>mm</td><td>Minute with pad 0</td><td>00</td></tr>
         * <tr><td>m</td><td>Minute</td><td>0</td></tr>
         * <tr><td>ss</td><td>Second with pad 0</td><td>00</td></tr>
         * <tr><td>s</td><td>Second</td><td>0</td></tr>
         * <tr><td>DDDD</td><td>Day name of week</td><td>Monday</td></tr>
         * <tr><td>DDD</td><td>Short day name of week</td><td>Mon</td></tr>
         * <tr><td>D</td><td>Day of week</td><td>0(Sunday)</td></tr>
         * </table>
         *
         * @method format
         * @param {String} format
         * @param {Date} date
         * @namespace nx.date
         */
        format: function (inFormat, inDate) {
            var format = inFormat || "yyyy-MM-dd hh:mm:ss DD";
            var date = inDate || new Date();
            return format.replace(/yyyy|yy|MMMM|MMM|MM|dd|d|hh|h|P|HH|H|mm|m|ss|s|DDDD|DDD|D/g, function (key) {
                return selector[key](date);
            });
        }
    };
})();
