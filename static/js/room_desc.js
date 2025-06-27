document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("descriptionModal");
    const viewMoreBtn = document.getElementById("view-more-btn");
    const closeBtn = document.querySelector(".modal .close");

    // Attach global functions so inline onclick works
    window.openModal = function () {
        if (modal) {
            modal.style.display = "block";
        }
    };

    window.closeModal = function () {
        if (modal) {
            modal.style.display = "none";
        }
    };

    // Optional: wire up using addEventListener if you prefer not to use inline onclick
    if (viewMoreBtn) {
        viewMoreBtn.addEventListener("click", function (e) {
            e.preventDefault();
            openModal();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            closeModal();
        });
    }

    window.addEventListener("click", function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });
});