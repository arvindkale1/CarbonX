// ===== CONFIRM BUY ACTION =====
document.addEventListener("DOMContentLoaded", function () {
    const buyForms = document.querySelectorAll("form[action*='buy']");

    buyForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            const credits = form.querySelector("input[name='credits']");
            if (credits && credits.value <= 0) {
                alert("Credits must be greater than zero");
                e.preventDefault();
            }
        });
    });
});

// ===== CONFIRM SELL ACTION =====
document.addEventListener("DOMContentLoaded", function () {
    const sellForms = document.querySelectorAll("form[action*='sell']");

    sellForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            const credits = form.querySelector("input[name='credits']");
            if (credits && credits.value <= 0) {
                alert("Credits must be greater than zero");
                e.preventDefault();
            }
        });
    });
});
