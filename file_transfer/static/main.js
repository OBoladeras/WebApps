var filesVisible = false;

function checkFiles(input) {
    if (input.files.length > 0) {
        document.getElementById("file-list").innerHTML = "";
        for (let i = 0; i < input.files.length; i++) {
            document.getElementById("file-list").innerHTML += "<li>" + input.files[i].name + "</li>";
        }
    }
}

function copytext(text) {
    navigator.clipboard.writeText(text);

    var toastContainer = document.getElementById('toast-container');
    toastContainer.textContent = 'Url copied!';
    toastContainer.style.display = 'block';

    setTimeout(function () {
        toastContainer.style.display = 'none';
    }, 3000);
}

function submitForm() {
    const formm = document.getElementById("filesForm");
    if (formm.title.value == "") {
        alert("Please enter a title");
        return;
    }
    if (formm.username.value == "") {
        alert("Please enter a username");
        return;
    }
    if (formm.file.files.length == 0) {
        alert("Please select at least one file");
        return;
    }

    box = document.getElementById("formBox");
    box.style.visibility = "hidden";

    formm.submit();
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    document.getElementById("file").files = files;
    checkFiles(document.getElementById("file"));
}

function downloadZip() {
    window.location.href = "/download/{{ token }}/zip";
}

function seeFiles() {
    const card = document.getElementById("card");
    const files = document.getElementById("files");
    const button = document.getElementById("seefilesButton");

    if (filesVisible) {
        card.style.top = "50%";
        card.style.transform = "translate(-50%, -50%)";
        files.style.visibility = "hidden";
        button.innerHTML = "See files";

        filesVisible = false;
    }
    else {
        card.style.top = "5%";
        card.style.transform = "translate(-50%, 0%)";
        files.style.visibility = "visible";
        button.innerHTML = "Hide files";

        filesVisible = true;
    }
}
