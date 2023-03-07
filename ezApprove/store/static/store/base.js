(function($) {
    "use strict";
    var $WIN = $( window );

    $WIN.on( 'load' , function() {
        var url = $( location ).attr( "href" );
        if (url.search('/sold') != -1) {
            setNavHighlight('nav-sold');
        } else if (url.search('/approved') != -1) {
            setNavHighlight('nav-approved');
        } else if (url.search('/denied') != -1) {
            setNavHighlight('nav-denied');
        } else if (url.search('/kicked-back') != -1) {
            setNavHighlight('nav-kicked-back');
        } else if ((url == 'http://127.0.0.1:8000/store') || (url == 'http://127.0.0.1:8000/store/') || (url == 'https://127.0.0.1:8000/store') || (url == 'https://127.0.0.1:8000/store/')) {
            setNavHighlight('nav-pending');
        } else {
            console.log('error - url not as expected');
        }
    });
    
    function setNavHighlight(nav_id) {
        $( ".topnav" ).children( "a" ).each( function() {
            if (($( this ).attr( 'id' ) == nav_id) && !($( this ).hasClass( "active" ))) {
                $( this ).addClass( "active" );
            }
            if (($( this ).attr( 'id' ) != nav_id) && ($( this ).hasClass( "active" ))) {
                $( this ).removeClass( "active" );
            }
        });
    }

    
})(jQuery);

function handleButtons(btn_id) {
    if (btn_id.search('-approve') != -1) {
        regex = /(-approve)/gm;
        approveItem(btn_id.split(regex)[0]);
    } else if (btn_id.search('-kickback') != -1) {
        regex = /(-kickback)/gm;
        kickBackItem(btn_id.split(regex)[0]);
    } else if (btn_id.search('-deny') != -1) {
        regex = /(-deny)/gm;
        denyItem(btn_id.split(regex)[0]);
    } else if (btn_id.search('-sell') != -1) {
        regex = /(-sell)/gm;
        sellItem(btn_id.split(regex)[0]);
    } else if (btn_id.search('-resubmit') != -1) {
        regex = /(-resubmit)/gm;
        submitItem(btn_id.split(regex)[0]);
    } else {
        console.log("unsupported button id found");
        return;
    }
}

function handleItemAction(data, view_path, dom_action, arg1, arg2) {
    fetchItemAction(data, view_path).then(function(json) {
        if (json.hasOwnProperty('status') && (json.status == 1)) {
            dom_action(arg1, arg2);
        } else {
            console.log("error reading server response");
        }
    });
}

async function fetchItemAction(data, view_path) {
    const csrftoken = getCookie('csrftoken');
    const request = new Request(window.location.origin + "/store/" + view_path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    });
    const response = await fetch(request);
    const json = await response.json();
    console.log(json);
    return json;
}

async function approveItem(id) {
    const payload = {
        item: id,
        action: 'approve',
        reason: 'none'
    };
    const rel_url = 'dbrequests/approve/';
    handleItemAction(payload, rel_url, replaceItemCard, "approved", id);
}

async function kickBackItem(id) {
    const comments = document.getElementById(id+"-comments-field").value;
    if ((comments != "") && (comments !== null)) {
        const payload = {
            item: id,
            action: 'kick-back',
            reason: comments
        };
        const rel_url = 'dbrequests/kick-back/';
        handleItemAction(payload, rel_url, replaceItemCard, "kicked-back", id);
    } else {
        alert("must enter approver comments to kick back item");
    }
    
}

function denyItem(id) {
    const payload = {
        item: id,
        action: 'deny',
        reason: 'none'
    };
    const rel_url = 'dbrequests/deny/';
    handleItemAction(payload, rel_url, replaceItemCard, "denied", id);
}

function sellItem(id) {
    const sold_price = document.getElementById(id+"-sold-price-field").value;
    if (/[0-9]+.[0-9]+$/.test(sold_price)) {
        const payload = {
            item: id,
            action: 'sell',
            price: sold_price
        };
        const rel_url = 'dbrequests/sell/';
        handleItemAction(payload, rel_url, replaceItemCard, "sold", id);
    } else {
        alert("no sell price given");
    }
}

function submitItem(id) {
    const list_price = document.getElementById(id+"-list-price-field").value;
    const details = document.getElementById(id+"-description-field").value;
    if ((/[0-9]+.[0-9]+$/.test(list_price)) && (details != "")) {
        const payload = {
            item: id,
            action: 'submit',
            price: list_price,
            description: details
        };
        const rel_url = 'dbrequests/submit/';
        handleItemAction(payload, rel_url, replaceItemCard, "submitted", id);
    } else {
        alert("fields missing or invalid");
    }
}

function replaceItemCard(msg, item_id) {
    var replaced_message = document.createElement("p");
    replaced_message.classList.add("temp");
    replaced_message.textContent = "-- You "+msg+" "+item_id+" --";
    replaced_message.style.borderStyle = 'groove';
    replaced_message.style.borderWidth = 'thick';
    replaced_message.style.borderColor = '#30363d';
    document.getElementById(item_id+"-card").replaceWith(replaced_message);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}