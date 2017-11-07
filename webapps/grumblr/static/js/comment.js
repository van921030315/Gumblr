$(document).on('submit', '#add_comment_form',  function( event ) {
    event.preventDefault();
    var pid = event.target.dataset.id;
    var username = event.target.dataset.name;
    $.ajax({
        type: 'POST',
        url: '/add_comment/'+pid,
        data: {
            text: $('#'+pid).val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(resp){
            var time = new Date(resp[0]['fields']['time']);
            var date = time.toDateString().slice(4);
            var dates = date.split(" ");
            var times = time.toLocaleTimeString().split(" ");
            var date_str = dates[0]+". "+dates[1]+". "+dates[2]+", ";
            var time_str = times[0].slice(0,5)+ " ";
            time_str = times[1] == "PM" ? time_str+"p.m.":time_str+"a.m.";
            var comment_box = (document).getElementById(pid).parentNode.parentNode.nextElementSibling;
            var table = comment_box.lastElementChild;
            var t_body = (document).createElement("tbody");
            var row = document.createElement("tr");
            var col1 = document.createElement("th");
            var newphoto = document.createElement("img");
            newphoto.src = "photo/" + resp[0]['fields']['username'];
            newphoto.alt = resp[0]['fields']['username'];
            newphoto.height = "20";
            newphoto.width = "20";
            col1.appendChild(newphoto);
            var col2 = document.createElement("th");
            col2.innerText = resp[0]['fields']['username'];
            var col3 = document.createElement("th");
            col3.innerText = "commented @ " +date_str+time_str+ ":" ;
            var col4 = document.createElement("th");
            var div =  document.createElement("div");
            div.style.color = "midnightblue";
            div.innerHTML = resp[0]['fields']['text'];
            console.log("div");
            col4.appendChild(div);
            row.appendChild(col1);
            row.appendChild(col2);
            row.appendChild(col3);
            row.appendChild(col4);
            t_body.appendChild(row);
            table.appendChild(t_body);
        }
    })
});