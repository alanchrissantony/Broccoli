'use strict';

(function () {

  const djangoMessage = document.getElementById('django-message');
  
  if (djangoMessage) {
    const message = djangoMessage.dataset.message;
    let messageTags = djangoMessage.dataset.tags.split(' ');

    const toastPlacementExample = document.querySelector('.toast-placement-ex');

    $('#toast-message').text(`${message}`);
    $('#toast-tag').text(`${messageTags.toString().toUpperCase()}`);

    if(messageTags == 'error'){
        messageTags = ['danger']
    }
    
    toastPlacementExample.classList.add('bg-'+messageTags);
    toastPlacementExample.classList.add('top-0', 'end-0');
    
    const toastPlacement = new bootstrap.Toast(toastPlacementExample);
    toastPlacement.show();
  }
})();