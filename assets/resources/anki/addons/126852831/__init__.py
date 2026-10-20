from aqt import mw, gui_hooks
from aqt.editor import Editor

NBSPCLEANER_JS = """
(function() {
    // Stops script from running too many times.
    if (window.ankiNBSPCleaner_v2) return;
    window.ankiNBSPCleaner_v2 = true;


    function RemoveNBSPFromField(field) {     
        const oldHTML = field.innerHTML;
        
        // We only really care about MathJax tags, which are displayed via '&amp;nbsp;'. Find these, and replace with regular spaces.
        let newNTML = oldHTML
            // .replace(/&nbsp;/g, ' ')
            // .replace(/\u00A0/g, ' ')
            .replace(/&amp;nbsp;/g, ' ');
            //.replace(/&amp;amp;/g, '');
        
        if (oldHTML === newNTML) { return; }

        // Updates the field HTML.
        field.innerHTML = newNTML;
        field.dispatchEvent(new InputEvent('input', { 
            bubbles: true,
            cancelable: true,
            inputType: 'insertText'
        }));
    }
    
    function FindAllFields() {
        const Fields = new Set();
        
        function ScanField(parent) {
            parent.querySelectorAll('[contenteditable="true"]').forEach(el => {
                if (el.isContentEditable) Fields.add(el);
            });
            parent.querySelectorAll('*').forEach(el => {
                if (el.shadowRoot) ScanField(el.shadowRoot);
            });
        }
        
        ScanField(document);
        
        document.querySelectorAll('iframe').forEach(iframe => {
            try {
                const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (iframeDoc) ScanField(iframeDoc);
            } catch (e) {}
        });
        return Array.from(Fields);
    }
    

    function AttachListenerToField(field) {
        // Automatically cleans the field if we lose focus from it (the same time that MathJax runs).
        if (field._nbspCleanerAttached_v2) return;
        field.addEventListener('focusout', function(event) {
            RemoveNBSPFromField(field);
        }, true);
        field._nbspCleanerAttached_v2 = true;
    }
    

    
    setTimeout(() => {
        const fields = FindAllFields();
        fields.forEach(AttachListenerToField);
    }, 500);
    
    // Watch for new fields.
    const observer = new MutationObserver(() => {
        FindAllFields().forEach(AttachListenerToField);
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
})();
"""

def inject_nbsp_cleaner(editor: Editor):
    editor.web.eval(NBSPCLEANER_JS)
def delayed_inject(editor: Editor):
    mw.taskman.run_on_main(lambda: inject_nbsp_cleaner(editor))

gui_hooks.editor_did_init.append(inject_nbsp_cleaner)
gui_hooks.editor_did_load_note.append(inject_nbsp_cleaner)

gui_hooks.editor_did_load_note.append(lambda ed: mw.taskman.run_in_background(
    lambda: None,
    lambda _: delayed_inject(ed)
))