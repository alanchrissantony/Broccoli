$(function() {
               
            var LocsA = [
                {
                    lat: 40.740178,
                    lon: -74.190194,
                    title: 'Location 1',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.733617,
                    lon: -74.171150,
                    title: 'Location 2',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.743011,
                    lon: -74.247100,
                    title: 'Location 3',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.711150,
                    lon: -74.214998,
                    title: 'Location 4',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.690010,
                    lon: -74.151753,
                    title: 'Location 5',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.697590,
                    lon: -74.263164,
                    title: 'Location 6',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.729979,
                    lon: -74.271992,
                    title: 'Location 7',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.749702,
                    lon: -74.163631,
                    title: 'Location 8',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.718971,
                    lon: -74.323219,
                    title: 'Location 9',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.748350,
                    lon: -74.323219,
                    title: 'Location 10',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                },
                {
                    lat: 40.740178,
                    lon: -74.190194,
                    title: 'Location 11',
                    html: [ '<div class="ltn__map-item">',
                                '<h3 class="ltn__location-name">Boston, New York</h3>',
                                '<h5 class="ltn__location-single-info"><i class="fas fa-map-marked-alt"></i>5816 S. Coulter Street Amarillo, TX 79119</h5>',
                                '<h4 class="ltn__location-single-info"><i class="fas fa-phone-volume"></i>0123456789</h4>',
                                '<div class="btn-wrapper">',
                                    '<a href="contact.html" class="btn btn-transparent btn-border btn-effect-4"><i class="fas fa-location-arrow"></i> Get An Appointment</a>',
                                    '<a href="#" class="btn btn-transparent btn-border btn-effect-3"><i class="fas fa-globe"></i> View Website</a>',
                                '</div>',
                            '</div>'
                        ].join(''),
                    icon: 'img/icons/map-marker-2.png',
                    animation: google.maps.Animation.BOUNCE
                }

            ];
            new Maplace({
                locations: LocsA,
                controls_on_map: true,
                map_options: {
                    zoom: 13,
                    scrollwheel: false,
                    stopover: true
                },
                stroke_options: {
                    strokeColor: '#f10', 
                    strokeOpacity: 0.8, 
                    strokeWeight: 2, 
                    fillColor: '#f10', 
                    fillOpacity: 0.4
                }
            }).Load();

        });