var editedID = null;
var targetHeight = {};

function loadBoard() {
    i = 0;
    itemID = "boxItem" + i;

    boxesIDs = []
    while (getCookie(itemID) != null) {
        itemID = "boxItem" + i;
        i++;
        boxesIDs.push(itemID);
    }

    for (const boxID of boxesIDs) {
        data = getCookie(boxID);
        if (data != null) {
            boxDiv = createObject(data.panelID, data.id);

            title = boxDiv.children[0];
            description = boxDiv.children[1];
            title.innerHTML = data.title;
            description.innerHTML = data.description;
        }
    }
}

function createObject(parentID, id = null) {
    const parentBox = document.getElementById(parentID);

    const newBox = document.createElement("div");
    newBox.className = "boxItem animation-enterFromBottom";

    if (id == null) {
        id = newBoxItemID();
    }
    newBox.id = id;

    const title = document.createElement("h3");
    title.onclick = () => openInfoPanel(newBox);
    title.innerHTML = "Title";
    newBox.appendChild(title);

    const description = document.createElement("p");
    description.className = "description";
    description.innerHTML = "No description provided";
    newBox.appendChild(description);

    parentBox.appendChild(newBox);
    var newH = parentBox.offsetHeight - 48;
    parentBox.removeChild(newBox);

    animateElementProgressively(parentBox, newH);
    parentBox.appendChild(newBox);

    setTimeout(() => {
        newBox.className = "boxItem";
        parentBox.style.height = "auto";
        drag(newBox);
    }, 2000);

    return newBox;
}

function animateElementProgressively(animatedElement, targetHeight) {
    const duration = 300;
    const startHeight = animatedElement.offsetHeight;
    const startTime = performance.now();

    function updateHeight() {
        const currentTime = performance.now();
        const progress = (currentTime - startTime) / duration;

        if (progress < 1) {
            const newHeight = startHeight + progress * (targetHeight - startHeight);
            animatedElement.style.height = newHeight + 'px';
            requestAnimationFrame(updateHeight);
        } else {
            animatedElement.style.height = targetHeight + 'px';
        }
    }

    updateHeight();
}


function closeInfoPanel(save = true) {
    const infoPanel = document.getElementById("infoPanel");
    infoPanel.className = "infoPanel animation-hideRight";
    document.body.style.overflow = "hidden";

    setTimeout(() => {
        document.body.style.overflow = "auto";
        infoPanel.className = "infoPanel";
        infoPanel.style.display = "none";

    }, 1500);

    if (save) {
        cookieName = editedID;
        data = {
            "id": editedID,
            "panelID": document.getElementById(editedID).parentElement.id,
            "title": infoPanel.children[0].children[0].value,
            "description": infoPanel.children[1].value
        }

        setCookie(cookieName, data, 7);
    }
}

function openInfoPanel(parentDiv) {
    const duration = 750;
    const infoPanel = document.getElementById("infoPanel");
    infoPanel.className = "infoPanel animation-showRight";
    infoPanel.style.display = "block";

    document.body.style.overflow = "hidden";

    title = parentDiv.children[0].innerHTML;
    description = parentDiv.children[1].innerHTML;

    editedID = parentDiv.id;
    infoPanel.children[0].children[0].value = "";
    infoPanel.children[1].value = "";
    if (title != "Title") {
        infoPanel.children[0].children[0].value = title;
    }
    if (description != "No description provided") {
        infoPanel.children[1].value = description;
    }

    setTimeout(() => {
        document.body.style.overflow = "auto";
        infoPanel.className = "infoPanel";

        document.addEventListener('click', handleCloseInfo);
    }, duration);

    function handleCloseInfo(event) {
        var infoPanel = document.getElementById('infoPanel');
        var targetElement = event.target;

        if (!infoPanel.contains(targetElement)) {
            closeInfoPanel();
            document.removeEventListener('click', handleCloseInfo);
        }
    }
}

function drag(element) {
    let isPressed = false;
    let offsetX, offsetY;
    let w = element.offsetWidth;
    let tableID = null;
    let mouseX, mouseY;

    function handleMouseDown(e) {
        if (e.target.tagName === 'H3') {
            return;
        }

        isPressed = true;

        element.style.position = "absolute";
        element.style.width = w + "px";
        element.style.userSelect = "none";

        offsetX = e.clientX - element.getBoundingClientRect().left;
        offsetY = e.clientY - element.getBoundingClientRect().top;

        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    }

    function handleMouseMove(e) {
        if (isPressed) {
            element.style.left = e.clientX - offsetX + 'px';
            element.style.top = e.clientY - offsetY + 'px';
        }
    }

    function handleMouseUp(e) {
        isPressed = false;

        mouseX = e.clientX;
        mouseY = e.clientY;

        const boxIds = ["ideas", "to_do", "in_progress", "done"];
        for (const boxId of boxIds) {
            const box = document.getElementById(boxId);
            if (checkInsideDiv(box, boxId, mouseX, mouseY)) {
                tableID = boxId;
            }
        }

        if (tableID != null) {
            const table = document.getElementById(tableID);
            table.appendChild(element);
        }

        element.style.position = "static";
        element.style.width = "95%";
        element.style.left = "auto";
        element.style.top = "auto";

        element.style.userSelect = "auto";

        cookieName = element.id;
        data = {
            "id": element.id,
            "panelID": element.parentElement.id,
            "title": element.children[0].innerHTML,
            "description": element.children[1].innerHTML
        }
        setCookie(cookieName, data, 7);

        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
    }

    function checkInsideDiv(checkDiv, id, mouseX, mouseY) {
        const rect = checkDiv.getBoundingClientRect();
        const divX = rect.left;
        const divY = rect.top;
        const divWidth = rect.width;
        const divHeight = rect.height;

        if (
            mouseX >= divX && mouseX <= divX + divWidth &&
            mouseY >= divY && mouseY <= divY + divHeight
        ) {
            return id;
        }
    }

    element.addEventListener('mousedown', handleMouseDown);
}


function handleDescriptionInput(textArea) {
    infoPanel = document.getElementById("infoPanel");

    boxDiv = document.getElementById(editedID);
    description = boxDiv.children[1];
    description.innerHTML = textArea.value;
}

function handleTitleInput(input) {
    infoPanel = document.getElementById("infoPanel");

    boxDiv = document.getElementById(editedID);
    title = boxDiv.children[0];
    title.innerHTML = input.value;
}

function deleteBox() {
    boxDiv = document.getElementById(editedID);
    boxDiv.parentElement.removeChild(boxDiv);
    closeInfoPanel(false);

    deleteCookie(editedID);
}
