import React from "react";
import "./CommonContainer.scss";

export default function (props) {
    return (
	<div {...props} className={`container common-container ${props.className||""}`} />
    );
};
