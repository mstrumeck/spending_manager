$(document).ready(function(){
    $('.detail').hide();
    $('.detail-button').click(function(){
        $(this).closest('tbody').next().toggle('slow');
            });
    });