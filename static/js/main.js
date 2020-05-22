function exportTableToExcel(tableID, filename = ''){
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');
    
    // Specify file name
    filename = filename?filename+'.xls':'excel_data.xls';
    
    // Create download link element
    downloadLink = document.createElement("a");
    
    document.body.appendChild(downloadLink);
    
    if(navigator.msSaveOrOpenBlob){
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob( blob, filename);
    }else{
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
    
        // Setting the file name
        downloadLink.download = filename;
        
        //triggering the function
        downloadLink.click();
    }
}

function deleteItem(){
    if(confirm("This action will delete the selected item. Are you sure you want to continue?")){
        return true;
}
    return false;
}
 $(function() {
    $("#term").autocomplete({
      source: '/searchusers',
      minLength:1,
        focus: function(event, ui){
            //alert(ui.item.key)
            //alert('hello');
            $("#term").val(ui.item.value);
        },
        select: function(event, ui){
            window.location.href ="/detail/"+ui.item.id
            //alert(ui.item.description);
            //$("#food_no").val(ui.item.id);

        }
    });
  });


    $(function() {
        $(".datepicker").datepicker({dateFormat: 'yy-m-d'});
    });


