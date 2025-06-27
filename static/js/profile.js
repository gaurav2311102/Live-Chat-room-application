
document.addEventListener("DOMContentLoaded", () => {
    const mainSection = document.getElementsByClassName("main-feed-profile")[0];
    const activitySection = document.getElementsByClassName("right-sidebar-profile")[0];

    const profileBtn = document.getElementById("show-profile");
    const activityBtn = document.getElementById("show-activity");

    document.getElementById("show-profile").addEventListener("click", () => {

        mainSection.classList.add("section-visible");
        activitySection.classList.remove("section-visible");

        profileBtn.classList.add("active");
        activityBtn.classList.remove("active");
    });

    document.getElementById("show-activity").addEventListener("click", () => {
        mainSection.classList.remove("section-visible");
        activitySection.classList.add("section-visible");

        activityBtn.classList.add("active");
        profileBtn.classList.remove("active");
    });

    // Show profile by default
    document.getElementById("show-profile").click();
});

