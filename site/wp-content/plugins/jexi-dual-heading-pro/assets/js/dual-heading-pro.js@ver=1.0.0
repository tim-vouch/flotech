/**
 * Jexi Dual Heading Pro — Front-end Script
 *
 * • Intersection Observer for scroll-triggered animations
 * • Word splitting for "split-words" animation
 * • Line splitting for "split-lines" animation
 * • Stagger delays calculated automatically
 */
(function () {
    'use strict';

    /* ── Helpers ──────────────────────────────────────────── */

    /**
     * Wrap every word (including highlight spans) in a .jexi-word wrapper.
     * We walk childNodes so <span class="jexi-dhp__highlight"> stays intact.
     */
    function splitIntoWords(heading) {
        var fragment = document.createDocumentFragment();
        var wordIndex = 0;

        Array.prototype.forEach.call(heading.childNodes, function (node) {
            if (node.nodeType === Node.TEXT_NODE) {
                // Split text by spaces, keep spaces between words
                var parts = node.textContent.split(/(\s+)/);
                parts.forEach(function (part) {
                    if (/^\s+$/.test(part)) {
                        fragment.appendChild(document.createTextNode(part));
                    } else if (part.length) {
                        var span = document.createElement('span');
                        span.className = 'jexi-word';
                        span.textContent = part;
                        span.style.transitionDelay = (wordIndex * 60) + 'ms';
                        fragment.appendChild(span);
                        wordIndex++;
                    }
                });
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                // Wrap the element itself in a word span (e.g. <span class="jexi-dhp__highlight">)
                var wrapper = document.createElement('span');
                wrapper.className = 'jexi-word';
                wrapper.style.transitionDelay = (wordIndex * 60) + 'ms';
                wrapper.appendChild(node.cloneNode(true));
                fragment.appendChild(wrapper);
                wordIndex++;
                // Add a space after the element unless it's the last node
                fragment.appendChild(document.createTextNode(' '));
            }
        });

        heading.innerHTML = '';
        heading.appendChild(fragment);
    }

    /**
     * Split heading text into lines. We temporarily render it, measure where
     * line breaks happen, then wrap each line in a .jexi-line span.
     */
    function splitIntoLines(heading) {
        // Measure natural line breaks by inserting words and checking offsetTop
        var words = [];
        Array.prototype.forEach.call(heading.childNodes, function (node) {
            if (node.nodeType === Node.TEXT_NODE) {
                node.textContent.split(/(\s+)/).forEach(function (part) {
                    if (part.length) words.push({ type: 'text', content: part });
                });
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                words.push({ type: 'element', node: node.cloneNode(true) });
            }
        });

        // Build a temp container with inline spans to measure positions
        var tempContainer = document.createElement('div');
        tempContainer.style.cssText = window.getComputedStyle(heading).cssText;
        tempContainer.style.position = 'absolute';
        tempContainer.style.visibility = 'hidden';
        tempContainer.style.width = heading.offsetWidth + 'px';
        heading.parentNode.appendChild(tempContainer);

        var spans = [];
        words.forEach(function (w) {
            var el;
            if (w.type === 'text') {
                if (/^\s+$/.test(w.content)) {
                    tempContainer.appendChild(document.createTextNode(w.content));
                    return;
                }
                el = document.createElement('span');
                el.textContent = w.content;
            } else {
                el = w.node;
            }
            el.style.display = 'inline';
            tempContainer.appendChild(el);
            spans.push({ el: el, word: w });
            tempContainer.appendChild(document.createTextNode(' '));
        });

        // Group by offsetTop
        var lines = [];
        var currentLine = [];
        var currentTop = null;
        spans.forEach(function (s) {
            var top = s.el.offsetTop;
            if (currentTop === null || Math.abs(top - currentTop) < 4) {
                currentLine.push(s);
                if (currentTop === null) currentTop = top;
            } else {
                lines.push(currentLine);
                currentLine = [s];
                currentTop = top;
            }
        });
        if (currentLine.length) lines.push(currentLine);

        tempContainer.remove();

        // Rebuild heading with .jexi-line wrappers
        heading.innerHTML = '';
        lines.forEach(function (line, i) {
            var lineSpan = document.createElement('span');
            lineSpan.className = 'jexi-line';
            lineSpan.style.transitionDelay = (i * 100) + 'ms';
            line.forEach(function (s, j) {
                if (s.word.type === 'text') {
                    lineSpan.appendChild(document.createTextNode(s.word.content));
                } else {
                    lineSpan.appendChild(s.word.node.cloneNode(true));
                }
                if (j < line.length - 1) lineSpan.appendChild(document.createTextNode(' '));
            });
            heading.appendChild(lineSpan);
        });
    }

    /* ── Init ─────────────────────────────────────────────── */

    function initWidget(wrapper) {
        if (wrapper.dataset.jexiReady) return;
        wrapper.dataset.jexiReady = '1';

        var animType  = wrapper.dataset.jexiAnim;
        var delay     = parseInt(wrapper.dataset.jexiDelay, 10) || 0;
        var duration  = parseInt(wrapper.dataset.jexiDuration, 10) || 700;

        if (!animType || animType === 'none') return;

        // Set CSS custom property for duration
        wrapper.style.setProperty('--jexi-dur', duration + 'ms');

        // Split words / lines if needed
        var heading = wrapper.querySelector('.jexi-dhp__heading');
        if (heading) {
            if (animType === 'split-words') splitIntoWords(heading);
            if (animType === 'split-lines') splitIntoLines(heading);
        }

        // Observe for scroll trigger
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    setTimeout(function () {
                        wrapper.classList.add('jexi-dhp--visible');
                    }, delay);
                    observer.unobserve(wrapper);
                }
            });
        }, { threshold: 0.15 });

        observer.observe(wrapper);
    }

    /* ── Boot ─────────────────────────────────────────────── */

    function bootAll() {
        document.querySelectorAll('.jexi-dhp[data-jexi-anim]').forEach(initWidget);
    }

    // Run on DOMContentLoaded and also when Elementor frontend inits (for preview)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootAll);
    } else {
        bootAll();
    }

    // Elementor frontend hook (preview / editor)
    if (window.elementorFrontend) {
        // Re-init whenever a new widget renders in preview
        jQuery(window).on('elementor/frontend/init', function () {
            elementorFrontend.hooks.addAction('frontend/element_ready/jexi_dual_heading_pro.default', function ($scope) {
                var el = $scope[0].querySelector('.jexi-dhp[data-jexi-anim]');
                if (el) {
                    el.removeAttribute('data-jexi-ready');
                    initWidget(el);
                }
            });
        });
    }
})();
