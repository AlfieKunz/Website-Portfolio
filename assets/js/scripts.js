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
                if (window.scrollY === 0 && !navbarCollapsible.classList.contains('always-shrink')) {
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

    // Adds GitHub repo and Live Demo button to the project showcase.
    document.querySelectorAll('.item-showcase-overlay').forEach(showcase => {
        const READMECont = showcase.querySelector('.readme-container');
        const Content = showcase.querySelector('.item-showcase-content');
        const CloseBtn = showcase.querySelector('.showcase-close-btn');
        if (!READMECont || !Content || !CloseBtn) return;

        const Actions = document.createElement('div');
        Actions.className = 'showcase-header-actions';
        if (showcase.id) {
            const GitHubBtn = document.createElement('a');
            GitHubBtn.className = 'showcase-icon-btn';
            GitHubBtn.href = `https://github.com/AlfieKunz/${showcase.id}`;
            GitHubBtn.target = '_blank';
            GitHubBtn.rel = 'noopener noreferrer';
            GitHubBtn.title = 'View GitHub Source Code';
            GitHubBtn.setAttribute('aria-label', 'View GitHub Source Code');
            GitHubBtn.innerHTML = '<i class="bi bi-github"></i>';
            Actions.appendChild(GitHubBtn);
        }
        if (READMECont.dataset.demo) {
            const LiveDemoBtn = document.createElement('a');
            LiveDemoBtn.className = 'showcase-icon-btn showcase-icon-btn-demo';
            LiveDemoBtn.href = READMECont.dataset.demo;
            LiveDemoBtn.target = '_blank';
            LiveDemoBtn.rel = 'noopener noreferrer';
            LiveDemoBtn.title = 'View Live Demo';
            LiveDemoBtn.setAttribute('aria-label', 'View Live Demo');
            LiveDemoBtn.textContent = 'DEMO';
            Actions.appendChild(LiveDemoBtn);
        }
        if (READMECont.dataset.doc) {
            const DocumentBtn = document.createElement('a');
            DocumentBtn.className = 'showcase-icon-btn showcase-icon-btn';
            DocumentBtn.href = READMECont.dataset.doc;
            DocumentBtn.target = '_blank';
            DocumentBtn.rel = 'noopener noreferrer';
            DocumentBtn.title = 'View Document';
            DocumentBtn.setAttribute('aria-label', 'View Document');
            DocumentBtn.innerHTML = '<i class="bi bi-file-earmark-text"></i>';
            Actions.appendChild(DocumentBtn);
        }
        Content.insertBefore(Actions, CloseBtn);
    });

    // Opens & closes a specific showcase item, by updating the URL hash.
    const OpenShowcase = (id) => {
        // Closes any open showcases.
        const OpenShowcase = document.querySelector('.item-showcase-overlay.active');
        if (OpenShowcase && OpenShowcase.id !== id) {
            OpenShowcase.classList.remove('active');

            // Resets scrolling when swapping panels directly.
            OpenShowcase.querySelector('.showcase-desc-area')?.scrollTo(0, 0);
            OpenShowcase.querySelector('.secondary-projects-container')?.scrollTo(0, 0);
            const galleryArea = OpenShowcase.querySelector('.showcase-gallery-area');
            if (galleryArea) { 
                galleryArea.scrollLeft = 0;
                galleryArea.scrollTop = 0; 
            }
        }
        const Showcase = document.getElementById(id);
        Showcase.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (window.location.hash !== `#${id}`) {
            history.pushState(null, null, `#${id}`);
        }

        const READMECont = Showcase.querySelector('.readme-container');
        if (READMECont) {
            LoadREADME(id, READMECont);
        }
        ToggleDivider(Showcase);
    };
    const CloseShowcase = (Showcase) => {
        if (Showcase) {
            // Resets scroll.
            Showcase.querySelector('.showcase-desc-area')?.scrollTo(0, 0);
            Showcase.querySelector('.secondary-projects-container')?.scrollTo(0, 0);
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
            if (e.target === showcase || e.target.classList.contains('secondary-projects-container')) { CloseShowcase(showcase); }
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

// Loads GitHub repository README for projects showcase.
async function LoadREADME(repoPath, container, branch = 'main') {
    if (!container || container.dataset.loadedRepo === repoPath) return;
    container.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>`;
    const READMEUrl = `https://raw.githubusercontent.com/AlfieKunz/${repoPath}/${branch}/`;
    try {
        const Responce = await fetch(`${READMEUrl}README.md`);
        if (!Responce.ok) throw new Error('README not found');
        const rawMarkdown = await Responce.text();
        const ProcessedBlock = rawMarkdown.replace(/<table[\s\S]*?<\/table>/gi, block => block.replace(/\n\s*\n/g, '\n'));

        container.innerHTML = marked.parse(ProcessedBlock);
        container.querySelectorAll('table').forEach(table => {
            const TableWrapper = document.createElement('div');
            TableWrapper.className = 'readme-table-wrapper';
            table.parentNode.insertBefore(TableWrapper, table);
            TableWrapper.appendChild(table);
        });

        // Removes main title (will be captured by gradient) and first "---" before first section.
        container.querySelector('h1').remove();
        container.querySelector('hr').remove();

        // Fix image sources so relative paths resolve against the repo.
        container.querySelectorAll('img').forEach(img => {
            const ImgSource = img.getAttribute('src');
            if (ImgSource && !ImgSource.startsWith('http://') && !ImgSource.startsWith('https://') && !ImgSource.startsWith('data:')) {
                img.src = `${READMEUrl}${ImgSource.replace(/^\.\//, '')}`;
            }
            img.removeAttribute('height');
            img.removeAttribute('width');
            img.removeAttribute('style');
        });
        container.querySelectorAll('table, td, th, p, div').forEach(el => {
            el.removeAttribute('width');
            el.removeAttribute('height');
            el.removeAttribute('style');
        });

        // Redirects all links to other GitHub repos back to my website :)
        container.querySelectorAll('a').forEach(link => {
        const Reference = link.getAttribute('href');
        if (Reference && Reference.match(/^https?:\/\/(www\.)?github\.com\//i)) {
            try {
                const Url = new URL(Reference);
                // Isolates the repo name, and tries to find a matching project in my website. If we can find it,
                // and it is different to our own (text citation contains a self-link), inject our local url.
                const URLParts = Url.pathname.split('/').filter(Boolean); 
                if (URLParts.length == 2) {
                    if (document.getElementById(URLParts[1]) && URLParts[1] != repoPath) {
                        link.href = `#${URLParts[1]}`;
                    }
                }
            } catch (e) { }
        }
    });

        container.dataset.loadedRepo = repoPath;
    } catch (error) {
        container.innerHTML = `<p class="text-muted fst-italic py-3">Error: Unable to load GitHub Repository README.</p>`;
    }
}



// Scripts to load and process flashcard grabbing in "Resources"
document.addEventListener('DOMContentLoaded', () => {
    const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const slug = (y, n) => y + '-' + n.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

    const CARD_TYPES = [
        ['Definition', 'Terms, statements and results.', ['Term and statement on separate faces', 'Optional worked example, revealed on demand', 'Colour-coded by module tag']],
        ['Cloze+', 'Cloze deletions with context.', ['Multiple cloze groups per note', 'Notes and source-reference fields', 'Hint button that does not spoil the answer']],
        ['Derivation', 'Proofs and multi-step derivations.', ['Reveals one step at a time', 'Each step has its own justification line', 'Full derivation shown at the end']],
        ['Theorem', 'Theorems with their conditions.', ['Statement, hypotheses and pitfalls kept apart', 'Counterexample field', 'Links to related theorems']],
        ['Code / Algorithm', 'Programming and algorithm cards.', ['Syntax-highlighted code blocks', 'Prompt, solution and complexity fields', 'Copy-friendly monospace styling']]
    ];
    document.getElementById('cardAcc').innerHTML = CARD_TYPES.map((c, i) => `
        <div class="accordion-item">
            <h3 class="accordion-header"><button class="accordion-button ${i ? 'collapsed' : ''}" type="button" data-bs-toggle="collapse" data-bs-target="#ct${i}">${esc(c[0])}</button></h3>
            <div id="ct${i}" class="accordion-collapse collapse ${i ? '' : 'show'}" data-bs-parent="#cardAcc">
                <div class="accordion-body small"><p class="text-muted mb-2">${esc(c[1])}</p><ul class="mb-0 ps-3">${c[2].map(f => `<li>${esc(f)}</li>`).join('')}</ul></div>
            </div>
        </div>`).join('');

    // ---- EDIT HERE: one row per module: [year, name, optional type, optional URL] ----
    // Type is 'q' (Quizlet), 'a' (Anki) or 'f' (own file); omit it to use the year's default below.
    // Anki decks:  /assets/resources/anki/decks/<year>-<module-name>.apkg
    // Files:       /assets/resources/files/<year>-<module-name>.pdf
    // Any row can be given its own URL as the 4th value, e.g. ['y1','Linear Algebra','q','https://quizlet.com/...']
    const YEARS = { y1: 'Warwick University, Year 1', y2: 'Warwick University, Year 2', y3: 'Warwick University, Year 3', al: 'AQA, A-Level', gcse: 'AQA, GCSE' };
    const DEFAULT = { y1: 'q', y2: 'q', y3: 'a', al: 'q', gcse: 'q'};
    const QUIZLET_BASE = 'https://quizlet.com/class/';
    const TYPES = {
        q: { label: 'Quizlet set', icon: 'bi-box-arrow-up-right', cls: 'btn-outline-primary' },
        a: { label: 'Anki deck', icon: 'bi-download', cls: 'btn-primary' },
        f: { label: 'Notes file', icon: 'bi-file-earmark-text', cls: 'btn-outline-secondary' }
    };
    const MODULES = [
        ['gcse','Mathematics', '17146591'],['gcse','Computer Science', '16095339'],['gcse','Physics', '16062616'],

        ['al','Mathematics', '19575302'],['al','Further Mathematics', '19575302'],['al','Physics', '19575306'],['al','Computer Science', '19657579']

        // ['y1','Sets & Numbers'],['y1','Mathematical Analysis I & II'],['y1','Mathematical Methods & Modelling I & II'],
        // ['y1','Linear Algebra'],['y1','Physics Foundations'],['y1','Classical Mechanics & Special Relativity'],
        // ['y1','Quantum Phenomena'],['y1','Electromagnetism'],['y1','Programming'],

        // ['y2','Intro to PDEs'],['y2','Mathematical Analysis III'],['y2','Quantum'],['y2','Statistical Mechanics'],
        // ['y2','Electromagnetism & Optics'],['y2','Hamiltonian & Fluid Mechanics'],['y2','Mathematical Physics'],
        // ['y2','Norms, Metrics & Topologies'],['y2','Multivariable Analysis'],['y2','Computational Physics','f'],
        // ['y2','Algorithms'],['y2','Asymptotics & Integral Transforms'],

        // ['y3','Measure Theory'],['y3','Modelling with PDEs'],['y3','Fluid Dynamics'],['y3','Quantum'],
        // ['y3','Electrodynamics'],['y3','The Standard Model'],['y3','Kinetic Theory'],['y3','Neural Computing'],['y3','Mobile Robotics','f']
    ];
    MODULES.sort((a, b) => a[1].localeCompare(b[1]));

    const LIMIT = 6, PEEK = 2; // rows shown normally, then rows shown blurred before "Show all"
    const list = document.getElementById('deckList');
    const search = document.getElementById('deckSearch');
    const clearBtn = document.getElementById('deckClear');
    const tabs = document.querySelectorAll('#deckTabs button');
    let tab = 'all', expanded = false;

    function rowHTML(m, i, animFrom, peek) {
        const [y, n] = m;
        
        // Check if 3rd item is an explicit type ('q', 'a', 'f') or an ID/link
        const hasExplicitType = m[2] && TYPES[m[2]];
        const k = hasExplicitType ? m[2] : DEFAULT[y];
        const target = hasExplicitType ? m[3] : m[2];
        const T = TYPES[k];

        let href = '';
        if (k === 'q') {
            href = target ? (target.startsWith('http') ? target : `${QUIZLET_BASE}${target}/materials`) : QUIZLET_BASE;
        } else if (k === 'a') {
            href = target || `../../assets/resources/anki/decks/${slug(y, n)}.apkg`;
        } else {
            href = target || `../../assets/resources/files/${slug(y, n)}.pdf`;
        }

        const attrs = k === 'a' ? 'download' : 'target="_blank" rel="noopener noreferrer"';
        let cls = 'res-row d-flex align-items-center justify-content-between gap-3 bg-light rounded-4 p-3', st = '', ex = '';
        
        if (i >= animFrom) { 
            cls += ' res-anim'; 
            st += `animation-delay:${Math.min(i - animFrom, 10) * 30}ms;`; 
        }
        if (peek) { 
            const p = i - LIMIT + 1; 
            st += `filter:blur(${(p * 1.6).toFixed(1)}px);--o:${(1 - p * 0.2).toFixed(1)};pointer-events:none;`; 
            ex = ' inert aria-hidden="true"'; 
        }

        return `<div class="${cls}" style="${st}"${ex}>
            <div class="flex-grow-1" style="min-width:0"><div class="fw-bolder">${esc(n)}</div><div class="small text-muted fst-italic">${YEARS[y]}</div></div>
            <a class="btn btn-sm rounded-pill ${T.cls} flex-shrink-0 text-nowrap px-3" href="${href}" ${attrs} aria-label="${T.label}: ${esc(n)}"><i class="bi ${T.icon} me-sm-1"></i><span class="d-none d-sm-inline">${T.label}</span></a>
        </div>`;
    }

    function render(animFrom = Infinity) {
        const raw = search.value.trim(), term = raw.toLowerCase();
        clearBtn.classList.toggle('d-none', !raw);
        const rows = MODULES.filter(m => (tab === 'all' || m[0] === tab) && m[1].toLowerCase().includes(term));
        if (!rows.length) {
            list.innerHTML = `<p class="text-muted fst-italic text-center my-3">No modules match${raw ? ` "${esc(raw)}"` : ''}. Click to ${raw ? '<button type="button" class="btn btn-link p-0 align-baseline" data-act="clear">Clear search</button>' : ''}.</p>`;
            return;
        }
        const long = rows.length > LIMIT + PEEK, collapsed = long && !expanded;
        const shown = collapsed ? rows.slice(0, LIMIT + PEEK) : rows;
        let h = shown.map((m, i, c) => rowHTML(m, i, c, animFrom, collapsed && i >= LIMIT)).join('');
        if (collapsed) h += `<div class="text-center res-fade"><button type="button" class="btn btn-primary btn-sm rounded-pill px-4 mt-2" data-act="more">Show all (${rows.length}) modules <i class="bi bi-chevron-down ms-1"></i></button></div>`;
        if (long && expanded) h += '<div class="text-center mt-2"><button type="button" class="btn btn-outline-secondary btn-sm rounded-pill px-4" data-act="less">Show less <i class="bi bi-chevron-up ms-1"></i></button></div>';
        list.innerHTML = h;
    }

    function clearSearch() { search.value = ''; search.focus(); render(0); }

    list.addEventListener('click', e => {
        const a = e.target.closest('[data-act]');
        if (!a) return;
        if (a.dataset.act === 'more') { expanded = true; render(LIMIT); }
        else if (a.dataset.act === 'less') { expanded = false; render(); document.getElementById('decks').scrollIntoView({ behavior: 'smooth' }); }
        else if (a.dataset.act === 'clear') { clearSearch(); }
    });
    tabs.forEach(b => b.addEventListener('click', () => {
        tab = b.dataset.tab; expanded = false;
        tabs.forEach(t => { t.classList.toggle('btn-primary', t === b); t.classList.toggle('btn-outline-secondary', t !== b); });
        render(0);
    }));
    search.addEventListener('input', () => render(0));
    search.addEventListener('keydown', e => { if (e.key === 'Escape' && search.value) clearSearch(); });
    clearBtn.addEventListener('click', clearSearch);
    render();
});