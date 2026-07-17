let HamburgerActive = false;

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) { return; }
        if (HamburgerActive) {
            navbarToggler.click();
            HamburgerActive = false;
        }
        if (window.scrollY === 0 && !navbarCollapsible.classList.contains('always-shrink')) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }
    };

    navbarShrink();

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function () {
            const navbarCollapsible = document.body.querySelector('#mainNav');
            if (!navbarCollapsible) { return; }
            
            if (HamburgerActive) {
                HamburgerActive = false;
                if (window.scrollY === 0) {
                    navbarCollapsible.classList.remove('navbar-shrink')
                }
            } else {
                HamburgerActive = true;
                navbarCollapsible.classList.add('navbar-shrink');
            }
        });
    }

    const responsiveNavItems = [].slice.call(document.querySelectorAll('#navbarResponsive .nav-link'));
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
                HamburgerActive = false;
            }
        });
    });

    // Close hamburger on scroll
    const UnobservedScrollObjects = ['BODY', 'INPUT', 'TEXTAREA'];
    document.addEventListener('scroll', () => {
        navbarShrink();
        const FocussedElement = document.activeElement;
        if (FocussedElement && !UnobservedScrollObjects.includes(FocussedElement.tagName) && typeof FocussedElement.blur === 'function') {
            FocussedElement.blur();
        }
    });

    // Contact Form Validation & Submission
    const UserForm = document.getElementById('contactForm');
    if (UserForm) {
        UserForm.addEventListener('submit', function (event) {
            event.preventDefault(); 
            document.querySelectorAll('.is-invalid').forEach(Field => Field.classList.remove('is-invalid'));

            const SuccessMsg = document.getElementById('submitSuccessMessage');
            const ErrorMsg = document.getElementById('submitErrorMessage');
            SuccessMsg.classList.add('d-none');
            ErrorMsg.classList.add('d-none');

            var FormValid = true;

            const InputName = document.getElementById('name');
            const InputEmail = document.getElementById('email');
            const InputNumber = document.getElementById('phone');
            const InputMessage = document.getElementById('message');
            
            if (!(InputName.value || InputEmail.value || InputNumber.value || InputMessage.value)) { return; }

            if (!InputName.value) {
                InputName.classList.add('is-invalid');
                FormValid = false;
            }

            const PhoneErrorDiv = document.querySelector('[data-sb-feedback="phone:error"]');
            if (!InputEmail.value && !InputNumber.value) {
                PhoneErrorDiv.textContent = 'An email or phone number is required.';
                InputEmail.classList.add('is-invalid');
                InputNumber.classList.add('is-invalid');
                FormValid = false;
            } else if (InputNumber.value) {
                const GBPhoneRegex = /^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$/;
                if (!GBPhoneRegex.test(InputNumber.value)) {
                    PhoneErrorDiv.textContent = 'Please enter a valid phone number.';
                    InputNumber.classList.add('is-invalid');
                    FormValid = false;
                }
            }

            if (!InputMessage.value) {
                InputMessage.classList.add('is-invalid');
                FormValid = false;
            }

            if (FormValid) {
                const SubmitBtn = document.getElementById('submitButton');
                SubmitBtn.disabled = true;
                SubmitBtn.textContent = 'Submitting...';

                fetch(UserForm.action, {
                    method: 'POST',
                    body: new FormData(UserForm),
                    headers: { 'Accept': 'application/json' }
                })
                .then(response => {
                    if (response.ok) {
                        SuccessMsg.classList.remove('d-none');
                        UserForm.reset();
                    } else {
                        ErrorMsg.querySelector('div').textContent = 'Error Sending Form: Field(s) Invalid.';
                        ErrorMsg.classList.remove('d-none');
                    }
                })
                .catch(error => {
                    ErrorMsg.querySelector('div').textContent = 'Error Sending Form: Bad Connection.';
                    ErrorMsg.classList.remove('d-none');
                })
                .finally(() => {
                    SubmitBtn.disabled = false;
                    SubmitBtn.textContent = 'Submit';
                });
            }
        });
    }



    // Intelligent loading of images, by adding wrapped imaged using data-src.
    const SliderTracking = document.querySelector('.slider-track');
    if (!SliderTracking) return;

    // Clones all images to form wrapped 2nd half.
    const Slides = Array.from(SliderTracking.children);
    Slides.forEach(img => {
        const clone = img.cloneNode(true);
        SliderTracking.appendChild(clone);
    });

    setTimeout(() => {
        SliderTracking.classList.add('is-animating');
    }, 50);

    // Adds lazy loading to wrapped images
    const WrappedImages = SliderTracking.querySelectorAll('img[data-src]');
    WrappedImages.forEach(img => {
        const ImageBox = new Image();
        ImageBox.src = img.getAttribute('data-src');
        ImageBox.decode()
            .then(() => {
                img.src = ImageBox.src;
                img.removeAttribute('data-src');
            })
            .catch(encodingError => {
                console.error("Image failed to decode smoothly:", encodingError);
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
            });
    });

    // Play/Pause mechanics with slider.
    const PlayPauseButton = document.getElementById('sliderToggle');
    const PlayPauseIcon = document.getElementById('toggleIcon');
    if (PlayPauseButton && SliderTracking) {
        PlayPauseButton.addEventListener('click', () => {
            if (SliderTracking.classList.toggle('is-paused')) {
                PlayPauseIcon.classList.replace('bi-pause-fill', 'bi-play-fill');
                PlayPauseButton.setAttribute('aria-label', 'Play slideshow');
            } else {
                PlayPauseIcon.classList.replace('bi-play-fill', 'bi-pause-fill');
                PlayPauseButton.setAttribute('aria-label', 'Pause slideshow');
            }
        });
    }

});



// Showcase panel for career and projects section.
document.addEventListener('DOMContentLoaded', () => {

    // Opens & closes a specific showcase item, by updating the URL hash.
    const OpenShowcase = (id) => {
        // Closes any open showcases.
        const OpenShowcase = document.querySelector('.item-showcase-overlay.active');
        if (OpenShowcase && OpenShowcase.id !== id) {
            OpenShowcase.classList.remove('active');
        }
        const Showcase = document.getElementById(id);
        Showcase.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (window.location.hash !== `#${id}`) {
            history.pushState(null, null, `#${id}`);
        }
        ToggleDivider(Showcase);
    };
    const CloseShowcase = (Showcase) => {
        if (Showcase) {
            // Resets scroll.
            Showcase.querySelector('.showcase-desc-area').scrollTop = 0;
            const galleryArea = Showcase.querySelector('.showcase-gallery-area');
            if (galleryArea) { 
                galleryArea.scrollLeft = 0;
                galleryArea.scrollTop = 0; 
            }

            Showcase.classList.remove('active');
            document.body.style.overflow = '';
            history.pushState(null, null, window.location.pathname + window.location.search);
        }
    };

    // Opens showcase upon panel click.
    const Panels = document.querySelectorAll('.clickable-panel');
    Panels.forEach(panel => {
        panel.addEventListener('click', () => {
            OpenShowcase(panel.getAttribute('panel-name'));
        });
    });

    // Closes showcases on close button, clicking outside the panel, or pressing esp (or mouse back button).
    const Showcases = document.querySelectorAll('.item-showcase-overlay');
    Showcases.forEach(showcase => {
        const CloseButton = showcase.querySelector('.showcase-close-btn');
        if (CloseButton) {CloseButton.addEventListener('click', () => CloseShowcase(showcase)); }
        showcase.addEventListener('click', (e) => {
            if (e.target === showcase) { CloseShowcase(showcase); }
        });
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') { CloseShowcase(document.querySelector('.item-showcase-overlay.active')); }
    });

    // Opens specific showcase based on URL hash.
    const HandlePanelURLHash = () => {
        const URLHash = window.location.hash.substring(1);
        if (URLHash) {
            const Showcase = document.getElementById(URLHash);
            if (Showcase && Showcase.classList.contains('item-showcase-overlay')) {
                OpenShowcase(URLHash);
            }
        } else {
            CloseShowcase(document.querySelector('.item-showcase-overlay.active'));
        }
    };
    HandlePanelURLHash();
    window.addEventListener('hashchange', HandlePanelURLHash);

    // Only shows the dividing line if the gallery scrolling isn't there.
    function ToggleDivider(activeShowcase) {
        if (!activeShowcase) return;
        const track = activeShowcase.querySelector('.showcase-gallery-track');
        const divider = activeShowcase.querySelector('.showcase-divider-area');
        if (track && divider) {
            if (window.innerWidth < 992 && track.scrollWidth > track.clientWidth) {
                divider.style.display = 'none';
            } else {
                divider.style.display = 'block';
            }
        }
    }
    window.addEventListener('resize', () => { ToggleDivider(document.querySelector('.item-showcase-overlay.active')); });
});