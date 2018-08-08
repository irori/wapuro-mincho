if (document.fonts) {
    let text = document.getElementById('try-text');
    let size = document.getElementById('try-size');
    let display = document.getElementById('try-display');
    let face;

    document.getElementById('try').hidden = false;
    text.addEventListener('focus', () => {
        if (!face) {
            face = new FontFace('ワープロ明朝full', 'url("wapuro-mincho.woff2") format("woff2")');
            document.fonts.add(face);
            face.load();
        }
    });
    text.addEventListener('input', () => {
        display.textContent = text.value;
    });
    size.addEventListener('change', () => {
        display.style.fontSize = size.value;
    });
    // Initialize
    display.textContent = text.value;
    display.style.fontSize = size.value;
}