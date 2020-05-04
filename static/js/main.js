
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

