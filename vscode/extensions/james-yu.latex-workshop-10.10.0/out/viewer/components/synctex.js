import { send, sendLog } from './connection.js';
import { scrollHistory } from './viewerhistory.js';
import * as utils from './utils.js';
let synctexEnabled = true;
export function isSyncTeXEnabled() {
    return synctexEnabled;
}
export function toggleSyncTeX() {
    synctexEnabled = !synctexEnabled;
    return synctexEnabled;
}
let reverseSynctexKeybinding = 'ctrl-click';
export function setSyncTeXKey(binding) {
    reverseSynctexKeybinding = binding;
}
function callSynctex(e, page, pageDom, viewerContainer) {
    const canvasDom = pageDom.getElementsByTagName('canvas')[0];
    const selection = window.getSelection();
    let textBeforeSelection = '';
    let textAfterSelection = '';
    // workaround for https://github.com/James-Yu/LaTeX-Workshop/issues/1314
    if (selection && selection.anchorNode && selection.anchorNode.nodeName === '#text') {
        const text = selection.anchorNode.textContent;
        if (text) {
            textBeforeSelection = text.substring(0, selection.anchorOffset);
            textAfterSelection = text.substring(selection.anchorOffset);
        }
    }
    const canvas = document.getElementsByClassName('canvasWrapper')[0];
    const left = e.pageX - pageDom.offsetLeft + viewerContainer.scrollLeft - canvas.offsetLeft;
    const top = e.pageY - pageDom.offsetTop + viewerContainer.scrollTop - canvas.offsetTop;
    const pos = PDFViewerApplication.pdfViewer._pages[page - 1]?.getPagePoint(left, canvasDom.offsetHeight - top);
    if (pos === undefined) {
        return;
    }
    void send({ type: 'reverse_synctex', pdfFileUri: utils.parseURL().pdfFileUri, pos, page, textBeforeSelection, textAfterSelection });
}
export function registerSyncTeX() {
    const viewerDom = document.getElementById('viewer');
    const pageDomList = viewerDom.childNodes[0].classList.contains('spread') ? [...viewerDom.childNodes].map(node => [...node.childNodes]).flat() : viewerDom.childNodes;
    for (const pageDom of pageDomList) {
        const page = Number(pageDom.dataset.pageNumber);
        const viewerContainer = document.getElementById('viewerContainer');
        switch (reverseSynctexKeybinding) {
            case 'ctrl-click': {
                pageDom.onclick = (e) => {
                    if (!(e.ctrlKey || e.metaKey)) {
                        return;
                    }
                    callSynctex(e, page, pageDom, viewerContainer);
                };
                break;
            }
            case 'double-click': {
                pageDom.ondblclick = (e) => {
                    callSynctex(e, page, pageDom, viewerContainer);
                };
                break;
            }
            default: {
                console.log(`Unknown keybinding ${reverseSynctexKeybinding} (view.pdf.internal.synctex.keybinding)`);
                break;
            }
        }
    }
}
function createIndicator(type, scrollX, scrollY, width_px, height_px) {
    let indicator = document.getElementById('synctex-indicator');
    if (type === 'rect') {
        const parent = indicator.parentNode;
        indicator = indicator.cloneNode(true);
        indicator.id = '';
        indicator.classList.add('synctex-indicator-rect');
        indicator.style.width = `${width_px}px`;
        indicator.style.height = `${height_px}px`;
        indicator.addEventListener('animationend', () => {
            indicator.style.display = 'none';
            parent.removeChild(indicator);
        });
        parent.appendChild(indicator);
    }
    else {
        indicator.className = 'show';
        setTimeout(() => indicator.className = 'hide', 10);
        // setTimeout(() => {
        //     indicator.style.left = ''
        //     indicator.style.top = ''
        // }, 1000)
    }
    indicator.style.left = `${scrollX}px`;
    indicator.style.top = `${scrollY}px`;
}
function forwardSynctexRect(data) {
    for (const record of data) {
        const page = document.getElementsByClassName('page')[record.page - 1];
        const pos_left_top = PDFViewerApplication.pdfViewer._pages[record.page - 1].viewport.convertToViewportPoint(record.h, record.v - record.H);
        const pos_right_down = PDFViewerApplication.pdfViewer._pages[record.page - 1].viewport.convertToViewportPoint(record.h + record.W, record.v);
        const canvas = document.getElementsByClassName('canvasWrapper')[0];
        pos_left_top[0] += canvas.offsetLeft;
        pos_left_top[1] += canvas.offsetTop;
        pos_right_down[0] += canvas.offsetLeft;
        pos_right_down[1] += canvas.offsetTop;
        const { scrollX, scrollY } = scrollToPosition(page, pos_left_top[0], pos_left_top[1]);
        if (record.indicator) {
            const width_px = pos_right_down[0] - Math.max(scrollX, pos_left_top[0]);
            const height_px = pos_left_top[1] - pos_right_down[1];
            createIndicator('rect', scrollX, scrollY, width_px, height_px);
        }
    }
}
function forwardSynctexCirc(data) {
    const page = document.getElementsByClassName('page')[data.page - 1];
    // use the offsetTop of the actual page, much more accurate than multiplying the offsetHeight of the first page
    // https://github.com/James-Yu/LaTeX-Workshop/pull/417
    const pos = PDFViewerApplication.pdfViewer._pages[data.page - 1].viewport.convertToViewportPoint(data.x, data.y);
    const { scrollX, scrollY } = scrollToPosition(page, pos[0], pos[1], true);
    if (data.indicator) {
        createIndicator('circ', scrollX, scrollY);
    }
}
export function forwardSynctex(data) {
    if (!isSyncTeXEnabled()) {
        sendLog('SyncTeX temporarily disabled.');
        return;
    }
    // if the type of data is SynctexRangeData[], parse as a rectangular indicator.
    if (Array.isArray(data)) {
        forwardSynctexRect(data);
    }
    else {
        forwardSynctexCirc(data);
    }
}
function scrollToPosition(page, posX, posY, isCircle = false) {
    const container = document.getElementById('viewerContainer');
    const maxScrollX = window.innerWidth * (isCircle ? 0.9 : 1);
    const minScrollX = window.innerWidth * (isCircle ? 0.1 : 0);
    let scrollX = page.offsetLeft + posX;
    scrollX = Math.min(scrollX, maxScrollX);
    scrollX = Math.max(scrollX, minScrollX);
    const scrollY = page.offsetTop + page.offsetHeight - posY;
    scrollHistory.set(container.scrollTop);
    if (PDFViewerApplication.pdfViewer.scrollMode === 1) {
        container.scrollLeft = page.offsetLeft;
    }
    else {
        container.scrollTop = scrollY - document.body.offsetHeight * 0.4;
    }
    scrollHistory.set(container.scrollTop);
    return { scrollX, scrollY };
}
//# sourceMappingURL=synctex.js.map