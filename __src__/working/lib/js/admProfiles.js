//<![CDATA[
	var userFormData;
	var rowSelected = 0;
	var userFormtype;
	var selected_username = "";
	var selected_uid = "";
	var group_membergrid_selected_gid = 0;
	var group_notmembergrid_selected_gid = 0;

	function disableSelection(target){
		if (typeof target.onselectstart!="undefined") //IE route
			target.onselectstart=function(){return false}
		else if (typeof target.style.MozUserSelect!="undefined") //Firefox route
			target.style.MozUserSelect="none"
		else //All other route (ie: Opera)
			target.onmousedown=function(){return false}
		target.style.cursor = "default"
	}

	function membership_grids_reload() {
		$("#membergrid").jqGrid('setGridParam',{
			url:'/db/groupsuserISmember?username='+selected_username,
			datatype:"json"
			}).trigger("reloadGrid");
	}
	
	function notmembership_grids_reload() {
		$("#notmembergrid").jqGrid('setGridParam',{
			url:'/db/groupsuserNOTmember?username='+selected_username,
			datatype:"json"
			}).trigger("reloadGrid");
	}
	
	function do_reload() {
		group_membergrid_selected_gid = 0;
		group_notmembergrid_selected_gid = 0;
		//document.getElementById("memberadd").disabled = true;
		//document.getElementById("memberdel").disabled = true;
		
		$('#addmember').attr('disabled', 'disabled');
		$('#delmember').attr('disabled', 'disabled');
		$('#addmember').attr('src','images/24-left-gray.png');
		$('#delmember').attr('src','images/24-right-gray.png');
		//getElementById("delmember").src='images/24-right-red.png';
		//getElementById("memberadd").attr('src','images/24-left-green.png');
		/*getElementById("memberadd").attr("disabled", true);
		getElementById("memberdel").attr("disabled", true);
		$("#memberadd").attr('disabled', 'disabled' );
		//$("#memberadd").attr('disabled', 'disabled' );
		*/
		membership_grids_reload();
		notmembership_grids_reload();

	}	
	
	function loadData() {		
		$("#usergrid").jqGrid({
			url:'/db/findUser?username='+document.getElementById("filtrado").value,
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
			colNames: ['uid','Usuario', 'Rol', 'Password','Descripción',
						'L_AH','M_AH','X_AH','J_AH','V_AH','S_AH','D_AH'],
			colModel: [
				{name:'uid', index:'uid', width:50, align: "right"},
				{name:'username',index:'username', width:80  },
				{name:'rol',index:'rol', width:30, align: "center" },
				{name:'password', index:'password', width:60, hidden: true },
				{name:'description', index:'description', width:180 },
				{name:'L_AH', index:'L_AH', width:40, sorttype:"int", align: "right", hidden: true},
				{name:'M_AH', index:'M_AH', width:40, sorttype:"int", align: "right", hidden: true},
				{name:'X_AH', index:'X_AH', width:40, sorttype:"int", align: "right", hidden: true},
				{name:'J_AH', index:'J_AH', width:40, sorttype:"int", align: "right", hidden: true},
				{name:'V_AH', index:'V_AH', width:40, sorttype:"int", align: "right", hidden: true},
				{name:'S_AH', index:'S_AH', width:40, sorttype:"int", align: "right", hidden: true},
				{name:'D_AH', index:'D_AH', width:40, sorttype:"int", align: "right", hidden: true}
				],
			height: 66,
			width: 381,
			shrinkToFit: false,
			forceFit: true,
			//rowNum:10,
			//pager: '#pager',
			//sortname: 'uid',
			viewrecords: true,
			//sortorder: "asc",
			caption: "Usuarios",
			gridComplete: function() { disableSelection(document.getElementById("usergrid")); },
		});
	
		$("#membergrid").jqGrid({
			url:'/db/groupsuserISmember?username='+selected_username,
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
				{name:'gid', index:'gid', width:50, align: "right"},
				{name:'groupname',index:'groupname', width:120  },
				{name:'description', index:'description', width:180 }
				],
			//rowNum:10,
			//pager: '#pager',
			//sortname: 'uid',
			viewrecords: true,
			//sortorder: "asc",
			caption: "Miembro de",
			height: 66,
			width: 390,
			shrinkToFit: false,
			forceFit: true,			

			gridComplete: function() { disableSelection(document.getElementById("membergrid")); },
			beforeSelectRow: function(rowid, e) {
				return getMemberRowGidData(rowid); // allow selection or unselection
			},
			
			loadComplete: function () {
				var rowIds = $(this).jqGrid('getDataIDs');
				for (i = 1; i <= rowIds.length; i++) {//iterate over each row
					if (!getMemberRowGidData(i)) {
						$(this).jqGrid('setRowData', i, false, "not-editable-row");
					} //if
				} //for
			}//loadComplete
			
		});

		$("#notmembergrid").jqGrid({
				url:'/db/groupsuserNOTmember?username='+selected_username,
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
					{name:'gid', index:'gid', width:50, align: "right"},
					{name:'groupname',index:'groupname', width:120  },
					{name:'description', index:'description', width:180 }
					],
				//rowNum:10,
				//pager: '#pager',
				//sortname: 'uid',
				viewrecords: true,
				//sortorder: "asc",
				caption: "No miembro de",
				height: 66,
				width: 390,
				shrinkToFit: false,
				forceFit: true,			

				gridComplete: function() { disableSelection(document.getElementById("notmembergrid")); },
				beforeSelectRow: function(rowid, e) {
					return getNOTMemberRowGidData(rowid); // allow selection or unselection
				},
				
				loadComplete: function () {
					var rowIds = $(this).jqGrid('getDataIDs');
					for (i = 1; i <= rowIds.length; i++) {//iterate over each row
						if (!getNOTMemberRowGidData(i)) {
							$(this).jqGrid('setRowData', i, false, "not-editable-row");
						} //if
					} //for
				}//loadComplete
				
			});
		
	}
	
	function updatediv() {
		$("#seleccionado").text('|'+selected_username+'|'+group_membergrid_selected_gid+'|'+group_notmembergrid_selected_gid+'|');
	}
	
	function getNOTMemberRowGidData(rowId) {
		//$('#myTable').jqGrid('getCell',row_id,'column_name');
		var rowData = jQuery('#notmembergrid').jqGrid('getRowData', rowId);
		if (rowData['gid'] < 1024) {
			return false;
		} else {
			return true;
		}
	}
	
	function getMemberRowGidData(rowId) {
		//$('#myTable').jqGrid('getCell',row_id,'column_name');
		var rowData = jQuery('#membergrid').jqGrid('getRowData', rowId);
		if (rowData['gid'] < 1024) {
			return false;
		} else {
			return true;
		}
	}
	
	function getRowIdData(rowId) {
		var rowData = jQuery('#usergrid').jqGrid ('getRowData', rowId);
		var jsondata=JSON.stringify(rowData);
		return jsondata;
	}
	
	$(window).focus(function() {
		do_reload();
	});
	
	$(window).load(function(){
		updatediv();
		loadData();
		do_reload();

		
		// !!!!! $('#delUser').attr("disabled", "disabled");
		
		/*
		$("#usergrid").jqGrid('setGridParam', {ondblClickRow: function(rowid,iRow,iCol,e){
			userFormData = getRowIdData(rowid);
			userFormType = 'modUser'
			window.open("formUser.html", 'userForm', '');

		}});
		*/
		

		
		$("#usergrid").jqGrid('setGridParam', {onSelectRow: function(rowid, status, e){
			var user_selected_data_row = jQuery('#usergrid').jqGrid('getRowData', rowid);
			selected_username = user_selected_data_row['username'];
//			alert(selected_username);
			do_reload();
			updatediv();
		}});
		
		$("#membergrid").jqGrid('setGridParam', {onSelectRow: function(rowid, status, e){
			var group_selected_data = jQuery('#membergrid').jqGrid('getRowData', rowid);
			group_membergrid_selected_gid = group_selected_data['gid'];
			
			if (group_membergrid_selected_gid != 0) {
				$('#delmember').attr('src','images/24-right-red.png');
				$('#delmember').removeAttr("disabled");
			}
			
			updatediv();
//			alert(selected_username);
			//membership_grids_reload();
		}});
		
		$("#notmembergrid").jqGrid('setGridParam', {onSelectRow: function(rowid, status, e){
			var notgroup_selected_data = jQuery('#notmembergrid').jqGrid('getRowData', rowid);
			group_notmembergrid_selected_gid = notgroup_selected_data['gid'];
			
			if (group_notmembergrid_selected_gid != 0) {
				$('#addmember').attr('src','images/24-left-green.png');
				$('#addmember').removeAttr("disabled");
			}	
			
			updatediv();
//			alert(selected_username);
			//membership_grids_reload();
		}});
		
	
		/*
		$("#filtrado" ).bind('input', function() {
			doreload()
		});
		*/
	});
		
	$(document).ready(function(){
		$('#delmember').click(function(){
			alert('#delmember');
		});
		$('#addmember').click(function(){
			alert('#addmember');
		});
	});
//]]>  