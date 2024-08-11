const $ = document.querySelector.bind(document);

const popup = $('#popup');

document.addEventListener('click', (event) => {
    if (popup.classList.contains('show')) {
        popup.classList.remove('show');
    }
    const target = event.target;
    if (target.tagName !== 'TD' || target.classList.contains('blank')) return;
    const text = target.textContent;
    const unicode = [...text].map((c) =>
        `U+${c.codePointAt(0).toString(16).padStart(4, 0).toUpperCase()}`).join(' ');
    $('#popup-glyph').textContent = text;
    document.getElementById('popup-info-jis').textContent = target.dataset.jis;
    document.getElementById('popup-info-unicode').textContent = unicode;
    popup.classList.add('show');
    popup.style.top = event.pageY - popup.offsetHeight / 2 + 'px';
    popup.style.left = event.pageX - popup.offsetWidth / 2 + 'px';
    $('#copy-icon').hidden = false;
    $('#copied-icon').hidden = true;
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        popup.classList.remove('show');
    }
});

$('#copy-button').addEventListener('click', async (event) => {
    event.stopPropagation();
    await navigator.clipboard.writeText($('#popup-glyph').textContent);
    $('#copy-icon').hidden = true;
    $('#copied-icon').hidden = false;
});
