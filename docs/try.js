(function() {
    let text = document.getElementById('try-text');
    let size = document.getElementById('try-size');
    let style = document.getElementById('try-style');
    let display = document.getElementById('try-display');

    text.addEventListener('focus', function() {
	if (document.fonts)
	    document.fonts.load('10px "ワープロ明朝full"');
	display.classList.remove('unfocused');
    });
    text.addEventListener('input', function() {
        display.textContent = text.value;
    });
    size.addEventListener('change', function() {
        display.style.fontSize = size.value;
    });
    style.addEventListener('change', function() {
        display.setAttribute('class', style.value);
    });
    // Initialize
    display.style.fontSize = size.value;
    if (text.value) {
	display.textContent = text.value;
	display.setAttribute('class', style.value);
    }
})();
