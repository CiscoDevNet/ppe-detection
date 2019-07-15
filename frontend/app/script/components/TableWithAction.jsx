import React from "react";
import "./TableWithAction.scss";

export default function (props) {
    var columns = (props.columns||[]).filter(column=>column.visible!==false);
    var actions = (props.actions||[]).filter(action=>action.visible!==false);
    var hasAction = actions.length;
    var colwidthtotal = columns.map(column=>column.width||1).reduce((v,i)=>(v+i),0);
    var colwidths = columns.map(column=>(column.width*(hasAction?80:100)/colwidthtotal+"%"));
    var items = (props.data||[]).map((dataitem,idx)=>(
	<tr key={dataitem[props["idkey"]||"id"]}>
	{
	    columns.map((column,colidx)=>(
		<td key={column.name} className={`cell`}>
		    {column.render?column.render(dataitem):dataitem[column.key]}
		</td>
	    ))
	}
	<td className="cell cell-actions" style={{display: hasAction?"table-cell":"none"}}>
	    {actions.map(action=>{
		 var enabled = !action.isDisabled || !action.isDisabled(dataitem);
		 var classDisable = enabled?"":"disabled";
		 return (
		     <div key={action.name}
			  className={`btn btn-link pt-0 pb-0 pr-0 ${classDisable}`}
			  onClick={()=>enabled && action.action(dataitem)}>
			 {action.render?action.render(dataitem):action.name}
		     </div>
		 );
	     })}
	</td>
	</tr>
    ));
    var header = (
	<thead>
	<tr>
	{columns.map((column,colidx)=>(
	    <th key={column.key} scope="col" className={`cell cell-header cell-${column.key}`} style={{width:colwidths[colidx]}}>
	    {column.name}
		 </th>
	))}
	<th className="cell cell-actions" style={{width: hasAction?"20%":"0%", display: hasAction?"table-cell":"none"}}>
	    Actions
	</th>
	</tr>
	</thead>
    );
    return (
	<div className="table-with-action table-responsive">
	<table className="table w-100">
	{header}
	<tbody>
	    {items}
	</tbody>
	</table>
	</div>
    );
};
