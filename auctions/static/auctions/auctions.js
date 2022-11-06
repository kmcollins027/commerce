document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".toggle-form").forEach(form => {
        form.onsubmit = function() {
            const formData = new FormData(form);
            fetch(form.action, {
                method: "POST",
                body: formData
            })
            .then(response => {
                return response.json()})
            .then(data => {
                icon_id = "#toggler-icon-" + form.dataset.listing_id;
                console.log(data);
                if (data["current_status"]) {
                document.querySelector(icon_id).src= "/media/images/heart-filled.png";
                }
                else {
                document.querySelector(icon_id).src= "/media/images/heart-outline.png";
                }
            })
            .catch(error => {
                console.log("*** api/listing error ***", error);
            })
            return false;
        }
    })
}) 