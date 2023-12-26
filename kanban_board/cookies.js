function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + JSON.stringify(value) + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) == ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) == 0) {
            return JSON.parse(cookie.substring(nameEQ.length, cookie.length));
        }
    }
    return null;
}

function deleteCookie(name) {
    setCookie(name, "", -1);
}

function newBoxItemID() {
    i = 0;
    itemID = "boxItem" + i;

    while (getCookie(itemID) != null) {
        i++;
        itemID = "boxItem" + i;
    } return itemID;
}
