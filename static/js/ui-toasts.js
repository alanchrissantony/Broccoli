let toaster_ltnBox = document.getElementById('toaster_ltnBox');

function showToaster_ltn(tag, message) {
    let toaster_ltn = document.createElement('div');
    toaster_ltn.classList.add('toaster_ltn');

    let toaster_ltnHeader = document.createElement('div');
    toaster_ltnHeader.classList.add('toaster_ltn-header');
    
    let icon = document.createElement('i');
    if (tag === 'Error') {
        icon.classList.add('fa', 'fa-times-circle');
        toaster_ltn.classList.add('error');
        toaster_ltn.style.borderLeftColor = '6px solid red';
    } else if (tag === 'Warning') {
        icon.classList.add('fa', 'fa-exclamation-circle');
        toaster_ltn.classList.add('warning');
        toaster_ltn.style.borderLeftColor = '6px solid orange'
    } else {
        icon.classList.add('fa', 'fa-check-circle');
        toaster_ltn.style.borderLeftColor = '6px solid #80B500'; // default color
    }

    let toaster_ltnTag = document.createElement('div');
    toaster_ltnTag.classList.add('me-auto', 'fw-semibold');
    toaster_ltnTag.innerText = tag;

    let smallText = document.createElement('small');
    smallText.classList.add('small-text');
    smallText.innerText = 'Just now';

    toaster_ltnHeader.appendChild(icon);
    toaster_ltnHeader.appendChild(toaster_ltnTag);
    toaster_ltnHeader.appendChild(smallText);

    let toaster_ltnBody = document.createElement('div');
    toaster_ltnBody.classList.add('toaster_ltn-body');
    toaster_ltnBody.innerText = message;

    toaster_ltn.appendChild(toaster_ltnHeader);
    toaster_ltn.appendChild(toaster_ltnBody);
    toaster_ltnBox.appendChild(toaster_ltn);

    setTimeout(() => {
        toaster_ltn.remove();
    }, 5000);
}