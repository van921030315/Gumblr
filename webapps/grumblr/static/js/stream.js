// server side program to keep pulling new posts from the server
function updatestream(){$(document).ready(function() {
    var request;
    request = $.ajax({
            type: 'GET',
            url: '/updatestream/',

            success:function(items){

                console.log("get response");
                var post_list = document.getElementById("post-list");

                // if no posts available, create an new postlist tag
                if (post_list == null){
                    post_list = document.createElement("div");
                    post_list.id = "post-list";
                    post_list.className = "content";
                }

                console.log("response");
                console.log(items);
                console.log("This is jquery")
                console.log(items)
                for (var i = 0; i < items.length; ++i) {
                var outer_box = document.createElement("section");
                outer_box.className = "outer-box";
                outer_box.id = "post_list"
                var section = document.createElement("section");
                section.className = "post";
                section.style.borderRight = "2px outset white";
                section.id = "newpost";
                var div = document.createElement("div");
                div.id = "content-box";


                var post = items[i]["fields"];

                var time = new Date(post["time"]);
                var date = time.toDateString().slice(4);
                var dates = date.split(" ");
                var times = time.toLocaleTimeString().split(" ");
                var date_str = dates[0]+". "+dates[1]+". "+dates[2]+", ";
                var time_str = times[0].slice(0,5)+ " ";
                time_str = times[1] == "PM" ? time_str+"p.m.":time_str+"a.m.";



                var pk = items[i]["pk"];
                var post_time = date_str+time_str;
                var post_text = post["post"];
                var post_username = post["username"];
                //var linebreak = document.createElement("br");

                // Builds a new HTML list item for the todo-list item
                //var newItem = document.createTextNode(text);
                //var newItem = document.createElement("newpost");
                var newphoto = document.createElement("img");
                newphoto.src = "photo/" + post_username;
                newphoto.alt = post_username;
                newphoto.height = "50";
                newphoto.width = "50";

                var hfour = document.createElement("h4");
                hfour.style.display = "inline-block";
                hfour.style.top = "0.5em";
                hfour.innerHTML = "<a href=\"/profile/" + post_username + "\"> " + post_username + "</a>";
                var hfive = document.createElement("h5");
                hfive.innerHTML = post_time;

                div.appendChild(newphoto);
                div.appendChild(hfour);
                div.appendChild(hfive);


                var text = document.createElement("p");
                text.style.textAlign = "left";
                text.style.marginLeft = "6em";
                text.style.color = "white";
                text.innerHTML = post_text;
                text.appendChild(document.createElement("br"));

                section.appendChild(div);
                section.appendChild(document.createElement("br"));
                section.appendChild(text);
                // 1
                outer_box.appendChild(section);

                var comment_box = document.createElement("div");
                comment_box.className = "comment-box";
                var comment_form = document.createElement("form");
                comment_form.id = "add_comment_form" ;
                comment_form.setAttribute("data-id", pk);


                var inputElem1 = document.createElement('input');
                inputElem1.type = 'hidden';
                inputElem1.name = 'csrfmiddlewaretoken';
                inputElem1.value = '{{ csrf_token }}';
                //console.log(inputElem1.value);
                //comment_form.appendChild(inputElem1);

                var inputElem2 = document.createElement('input');
                inputElem2.type = 'text';
                inputElem2.placeholder = 'Enter Comment';
                inputElem2.name = 'text';
                inputElem2.required = true;
                inputElem2.id = pk;
                comment_form.appendChild(inputElem2);

                var inputElem3 = document.createElement('input');
                inputElem3.type = 'submit';
                inputElem3.name = 'submit';
                inputElem3.value = 'Comment';
                comment_form.appendChild(inputElem3);

                comment_box.appendChild(comment_form);

                // 2
                outer_box.appendChild(comment_box);

                var comments = document.createElement("section");
                comments.className = 'comments';
                var hsix = document.createElement("h6");
                hsix.className = "comment-header";
                hsix.innerHTML = "Comments";
                var comment_table = document.createElement("table");
                comments.appendChild(hsix);
                comments.appendChild(comment_table);

                // 3

                outer_box.appendChild(comments);


                post_list.insertBefore(outer_box, post_list.firstChild);
                //post_list.prepend(section);
                // Adds the todo-list item to the HTML list
                //body.appendChild(fortune);
                }
            }
        })
    });
}



setInterval(function(){
        console.log("interval")
        updatestream()
    }, 5000);
