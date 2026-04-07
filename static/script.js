function validateForm() {
    let name = document.querySelector('input[name="name"]').value;
    if (name === "") {
        alert("Name is required");
        return false;
    }
    return true;
}