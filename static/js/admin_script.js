$(document).ready(function (){

$("#id_group").change(function () {
    $("#id_subGroup").empty();
    $.getJSON("/course/sub_groups_json/" + $("#id_group :selected").val(),
        function (data) {

            $.each(data,
                function () {
                    $("#id_subGroup").append('<option value=' + this.pk + '>' + this.fields.groupTitle + '</option>');

                });

        });


});
});