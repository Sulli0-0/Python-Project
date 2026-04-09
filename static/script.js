function validateForm() {
    let title = document.querySelector('input[name="title"]').value;
    if (title === "") {
        alert("Title is required");
        return false;
    }
    return true;
}