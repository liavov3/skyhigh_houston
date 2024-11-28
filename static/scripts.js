let slideIndex = 0;
showSlides();

function showSlides() {
    let slides = document.getElementsByClassName("slide");
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 5000); // Change image every 5 seconds
}

function plusSlides(n) {
    let slides = document.getElementsByClassName("slide");
    slides[slideIndex - 1].style.display = "none";
    slideIndex += n;
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    if (slideIndex < 1) {
        slideIndex = slides.length;
    }
    slides[slideIndex - 1].style.display = "block";
}

document.addEventListener('DOMContentLoaded', function() {
    const addToBagButtons = document.querySelectorAll('.add-to-bag');
    addToBagButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemName = button.getAttribute('data-item');
            const itemPrice = button.getAttribute('data-price');
            
            // Example of adding item to localStorage (you can modify this to use a backend server or session)
            let bag = JSON.parse(localStorage.getItem('bag')) || [];
            bag.push({ name: itemName, price: itemPrice });
            localStorage.setItem('bag', JSON.stringify(bag));

            // Show a success message
            alert(`${itemName} added to your bag!`);
        });
    });
});
