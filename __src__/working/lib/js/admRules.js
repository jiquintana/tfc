//<![CDATA[
	var groupFormData;
	var rowSelected = 0;
	var groupFormtype;
	
	function disableSelection(target){
		if (typeof target.onselectstart!="undefined") //IE route
			target.onselectstart=function(){return false}
		else if (typeof target.style.MozUserSelect!="undefined") //Firefox route
			target.style.MozUserSelect="none"
		else //All other route (ie: Opera)
			target.onmousedown=function(){return false}
		target.style.cursor = "default"
	}

	function doreload() {
		$("#groupgrid").jqGrid('setGridParam',{
			url:'/db/findGroup?groupname='+document.getElementById("filtrado").value,
			datatype:"json"
			}).trigger("reloadGrid");
		$('#delGroup').attr("disabled", "disabled");
	}
	
	function loadData() {
		$(window).focus(function() {
			doreload();
		});
		
		$("#groupgrid").jqGrid({
			url:'/db/findGroup?groupname='+document.getElementById("filtrado").value,
			datatype: "json",
			autoencode: true,
			hidegrid: false,
			jsonReader: {
				repeatitems: false,
				root: function (obj) { return obj; },
				page: function (obj) { return 1; },
				total: function (obj) { return 1; },
				records: function (obj) { return obj.length; }
			},
			colNames: ['gid','Nombre', 'Descripción'],
			colModel: [
				{name:'gid', index:'gid', width:50, sorttype:"int", align: "right", hidden: true},
				{name:'groupname',index:'groupname', width:120  },
				{name:'description', index:'description', width:180 }
				],
			//rowNum:10,
			//pager: '#pager',
			//sortname: 'uid',
			viewrecords: true,
			//sortorder: "asc",
			caption: "Grupos",
			height: 66,
			width: 325,
			shrinkToFit: false,
			forceFit: true,			

			gridComplete: function() { disableSelection(document.getElementById("groupgrid")); },
			beforeSelectRow: function(rowid, e) {
				return getRowGidData(rowid); // allow selection or unselection
			},
		});
	}
	
	function getRowGidData(rowId) {
		//$('#myTable').jqGrid('getCell',row_id,'column_name');
		var rowData = jQuery('#groupgrid').jqGrid('getRowData', rowId);
		if (rowData['gid'] < 1024) {
			return false;
		} else {
			return true;
		}
	}
	
	function getRowIdData(rowId) {
		var rowData = jQuery('#groupgrid').jqGrid('getRowData', rowId);
		var jsondata=JSON.stringify(rowData);
		return jsondata;
	}
	
	$(window).load(function(){ 
		loadData();
		$('#delGroup').attr("disabled", "disabled");
		
		$("#groupgrid").jqGrid('setGridParam', {ondblClickRow: function(rowid,iRow,iCol,e){
			if (getRowGidData(rowid)) {
				groupFormData = getRowIdData(rowid);
				groupFormType = 'modGroup'
				window.open("formGroup.html", 'groupForm', '');
			}
		}});
		
		$("#groupgrid").jqGrid('setGridParam', {onSelectRow: function(rowid, status, e){
			$('#delGroup').removeAttr("disabled");
			rowSelected = rowid;
		}});
		
		$("#filtrado" ).bind('input', function() {
			doreload()
		});
	});
	
	$(document).ready(function(){
			$('#newGroup').click(function(){
			$('#delGroup').attr("disabled", "disabled");
			groupFormType = 'addGroup'
			window.open("formGroup.html", 'groupForm', '');
		});
	});
	
	$(document).ready(function(){
		$('#delGroup').click(function(){
			groupFormType = 'delGroup'
			groupFormData = getRowIdData(rowSelected);
			window.open("delGroup.html", 'groupForm', '');
			$('#delGroup').attr("disabled", "disabled");
		});
	});
//]]>  
