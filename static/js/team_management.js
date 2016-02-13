$(document).ready(function(){
  $('.teams-container').sortable({
    stop: function(event, ui) {
      var order = 1;
      var json = []; // The json data sent to the server on sort.

      /* When the user drops the team get the ordering of all the teams
       * and put in into the json array. */
      $('.teams-container').children().each(function(){

        json.push({
          id: $(this).attr('data-id'),
          order: order,
        });

        // Change the order displayed on the page.
        $(this).find('.team-order').text(order);

        // The next item will have the next order.
        order += 1;
      });

      // Send the order to the server.
      $.ajax({
        type: 'post',
        url: 'reorder/',
        data: {
          data: JSON.stringify(json),
        },
        error: function(p){
          alert("Connection error, try again later.");
        },
      });
    },
  });
});
