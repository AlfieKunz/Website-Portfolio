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
    const Year = { al: 'AQA, A-Level',
                    gcse: 'AQA, GCSE',
                    y1: 'Warwick University, Year 1',
                    y2: 'Warwick University, Year 2',
                    y3: 'Warwick University, Year 3',
                    y4: 'Warwick University, Year 4' };
    const QuizletBase = 'https://quizlet.com/';
    const HomeBase = '../../assets/resources/';
    const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const IsMobile = window.matchMedia('(max-width: 575.98px)');
    let Limit = IsMobile.matches ? 5 : 7, Peek = IsMobile.matches ? 2 : 3;
    const ApplyBreakpoint = () => { Limit = IsMobile.matches ? 5 : 7; Peek = IsMobile ? 2 : 3; };
    IsMobile.addEventListener('change', () => { ApplyBreakpoint(); RenderFieldTable(); });

    const LinkType = {
        a: { label: ' &nbspAnki deck&nbsp ', icon: 'bi-download', cls: 'btn-primary' },
        f: { label: ' &nbspNotes file&nbsp ', icon: 'bi-file-earmark-text', cls: 'btn-outline-secondary' },
        q: { label: ' Quizlet set', icon: 'bi-box-arrow-up-right', cls: 'btn-outline-primary' }
    };

    const Fields = [
        ['gcse', 'Mathematics', 'class/17146591'], ['gcse', 'Computer Science', 'class/16095339'], ['gcse', 'Physics', 'class/16062616'],

        ['al', 'Mathematics', 'class/19575302'], ['al', 'Further Mathematics', 'class/19575302'], ['al', 'Physics', 'class/19575306'], ['al', 'Computer Science', 'class/19657579'],

        ['y1', 'M1AK2: Refresher Mathematics', '833635034'], ['y1', 'MA149: Linear Algebra', 'Alfie_Kunz/folders/algebra'], ['y1', 'PX157: Electricity & Magnetism', 'Alfie_Kunz/folders/electricity-magnetism'],
        ['y1', 'MA138: Sets & Numbers', '833761922'], ['y1', 'MA140: Mathematical Analysis I', 'Alfie_Kunz/folders/mathematical-analysis'], ['y1', 'MA152: Mathematical Analysis II', 'Alfie_Kunz/folders/mathematical-analysis'], 
        ['y1', 'MA147: Mathematical Methods & Modelling I', '833876825'], ['y1', 'MA145: Mathematical Methods & Modelling II', 'Alfie_Kunz/folders/mathematical-methods-modelling'],
        ['y1', 'PX155: Classical Mechanics & Special Relativity', 'Alfie_Kunz/folders/mechanics-relativity'], ['y1', 'PX154: Physics Foundations', 'Alfie_Kunz/folders/px154-physics-foundations'],
        ['y1', 'PX160: Tutorial (Maths/Physics)', 'Alfie_Kunz/folders/px160-worksheets'], ['y1', 'PX156: Quantum Phenomena', 'Alfie_Kunz/folders/quantum-particle-physics'],
        ['y1', 'PX159: Physics Programming Workshop', 'note/PX159%20Syntax.py'],
        
        ['y2', 'PX284: Statistical Mechanics, Electromagnetic Theory & Optics', 'Alfie_Kunz/folders/px284-statistical-mechanics-electromagnetic-theory-optics'], ['y2', 'MA271: Mathematical Analysis III', '950029935'],
        ['y2', 'MA263: Multivariable Analysis', '990110750'], ['y2', 'MA250: Introduction to PDEs', '951260286'], ['y2', 'PX285: Hamiltonian & Fluid Mechanics', 'Alfie_Kunz/folders/mechanics-relativity'],
        ['y2', 'PX262: Quantum Mechanics & its Applications', 'Alfie_Kunz/folders/quantum-particle-physics'], ['y2', 'CS260: Algorithms', 'Alfie_Kunz/folders/computer-science-modules'],
        ['y2', 'MA260: Norms, Metrics & Topologies', 'Alfie_Kunz/folders/ma260-norms-metrics-topologies'], ['y2', 'MA269: Asymptotics & Integral Transforms', 'Alfie_Kunz/folders/ma269-asymptotics-integral-transforms'],
        ['y2', 'PX286: Methods of Mathematical Physics', 'Alfie_Kunz/folders/px286-methods-of-mathematical-physics'], ['y2', 'PX281: Computational Physics', 'note/PX281%20Syntax.py'],

        ['y3', 'CS313: Mobile Robotics', 'anki/decks/CS313'], ['y3', 'MA359: Measure Theory', 'anki/decks/MA359'], ['y3', 'MA3D1: Fluid Dynamics', 'anki/decks/MA3D1'], ['y3', 'MA3J4: Mathematical Modelling with PDEs', 'anki/decks/MA3J4'],
        ['y3', 'PX3A2: Quantum Physics of Atoms', 'anki/decks/PX3A2'], ['y3', 'PX3A3: Electrodynamics', 'anki/decks/PX3A3'], ['y3', 'PX3A5: The Standard Model', 'anki/decks/PX3A5'],

        ['y4', 'PX449: Kinetic Theory', 'anki/decks/PX449']

    ];
    Fields.sort((a, b) => a[1].localeCompare(b[1])); // Sorts modules alphabetically.

    const DeckList = document.getElementById('deckList');
    if (!DeckList) return;
    const DeckSearch = document.getElementById('deckSearch');
    const DeckClear = document.getElementById('deckClear');
    const DeckTabs = document.querySelectorAll('#deckTabs button');
    let CurrentTab = 'all';
    let DeckExpanded = false;

    function ConfigureFieldHTML(m, i, AnimateStart, BlurElement) {
        // Intelligently grabs the type of card depending on the metadata link.
        let href, Link, OpenOption;
        const RetrieveCode = m[2].slice(0,4);
        switch (RetrieveCode) {
            case 'anki':
                href = HomeBase + m[2] + `.apkg`;
                OpenOption = 'download';
                Link = LinkType.a;
                break;
            case 'note':
                href = HomeBase + m[2];
                OpenOption = 'download';
                Link = LinkType.f
                break;
            default:
                href = QuizletBase + m[2];
                OpenOption = 'target="_blank" rel="noopener noreferrer"';
                Link = LinkType.q;
        }
        let ElementClass = 'res-row d-flex align-items-center justify-content-between gap-3 bg-light rounded-4 p-3';
        let ElementStyle = '';
        let ElementExtra = '';
        if (i >= AnimateStart) { 
            ElementClass += ' res-anim'; 
            ElementStyle += `animation-delay:${Math.min(i - AnimateStart, 10) * 30}ms;`; 
        }
        if (BlurElement) { 
            const p = i - Limit + 1;
            ElementStyle += `filter:blur(${(p * 1.6).toFixed(1)}px);--o:${(1 - p * 0.2).toFixed(1)};pointer-events:none;`;
            ElementExtra = ' inert aria-hidden="true"';
        }

        return `<div class="${ElementClass}" style="${ElementStyle}"${ElementExtra}>
            <div class="flex-grow-1" style="min-width:0"><div class="fw-bolder">${esc(m[1])}</div><div class="small text-muted fst-italic">${Year[m[0]]}</div></div>
            <a class="btn btn-sm rounded-pill ${Link.cls} flex-shrink-0 text-nowrap px-4" href="${href}" ${OpenOption} aria-label="${Link.label}: ${esc(m[1])}"><i class="bi ${Link.icon} me-sm-1"></i><span class="d-none d-sm-inline">${Link.label}</span></a>
        </div>`;
    }

    function RenderFieldTable(AnimateStart = Infinity) {
        const SearchParam = DeckSearch.value.trim().toLowerCase();
        DeckClear.classList.toggle('d-none', !SearchParam);
        const AllFields = Fields.filter(m => {
            const matchesTab = CurrentTab === 'all' 
                || m[0] === CurrentTab 
                || (CurrentTab === 'scl' && (m[0] === 'gcse' || m[0] === 'al'));
            const matchesSearch = m[1].toLowerCase().includes(SearchParam);
            return matchesTab && matchesSearch;
        });
        
        if (!AllFields.length) {
            DeckList.innerHTML = `<p class="text-muted fst-italic text-center my-3">No modules match${SearchParam ? ` "${esc(SearchParam)}"` : ''}. Click to ${SearchParam ? '<button type="button" class="btn btn-link p-0 align-baseline" data-act="clear">Clear search</button>' : ''}.</p>`;
            return;
        }
        const CollapseDeck = (AllFields.length > Limit + Peek) && !DeckExpanded;
        const ShownFields = CollapseDeck ? AllFields.slice(0, Limit + Peek) : AllFields;
        let h = ShownFields.map((m, i) => ConfigureFieldHTML(m, i, AnimateStart, CollapseDeck && i >= Limit)).join('');
        if (CollapseDeck) h += `<div class="text-center res-fade"><button type="button" class="btn btn-primary btn-sm rounded-pill px-4 mt-2" data-act="more">Show all (${AllFields.length}) modules <i class="bi bi-chevron-down ms-1"></i></button></div>`;
        if ((AllFields.length > Limit + Peek) && DeckExpanded) h += '<div class="text-center mt-2"><button type="button" class="btn btn-outline-secondary btn-sm rounded-pill px-4" data-act="less">Show less <i class="bi bi-chevron-up ms-1"></i></button></div>';
        DeckList.innerHTML = h;
    }

    function ClearFieldSearch() { DeckSearch.value = ''; DeckSearch.focus(); RenderFieldTable(0); }

    DeckList.addEventListener('click', e => {
        const a = e.target.closest('[data-act]');
        if (!a) return;
        if (a.dataset.act === 'more') { DeckExpanded = true; RenderFieldTable(6); }
        else if (a.dataset.act === 'less') { DeckExpanded = false; RenderFieldTable(); document.getElementById('decks').scrollIntoView({ behavior: 'smooth' }); }
        else if (a.dataset.act === 'clear') { ClearFieldSearch(); }
    });
    DeckTabs.forEach(b => b.addEventListener('click', () => {
        CurrentTab = b.dataset.tab; DeckExpanded = false;
        DeckTabs.forEach(t => { t.classList.toggle('btn-primary', t === b); t.classList.toggle('btn-outline-secondary', t !== b); });
        RenderFieldTable(0);
    }));
    DeckSearch.addEventListener('input', () => RenderFieldTable(0));
    DeckSearch.addEventListener('keydown', e => { if (e.key === 'Escape' && DeckSearch.value) ClearFieldSearch(); });
    DeckClear.addEventListener('click', ClearFieldSearch);
    RenderFieldTable();


    // Copies Add-on code to clipboard, with Bootstrap tooltip to notify the user of said action.
    document.querySelectorAll('.copy-code').forEach(el => {
    const ToolTip = new bootstrap.Tooltip(el, {
      title: 'Copied to Clipboard!',
      trigger: 'manual',
      placement: 'bottom'
    });

    let Timeout;
    const CopyAddonCode = async () => {
      await navigator.clipboard.writeText(el.textContent.trim());
        clearTimeout(Timeout);
        ToolTip.show();
        Timeout = setTimeout(() => ToolTip.hide(), 1100);
    };
    el.addEventListener('click', CopyAddonCode);
  });
});