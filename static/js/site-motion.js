(() => {
    "use strict";

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    const initHeader = () => {
        const header = document.querySelector(".site-header");
        const backToTop = document.querySelector("[data-back-to-top]");
        const root = document.documentElement;
        if (!header) return;

        let queued = false;

        const update = () => {
            header.classList.toggle("is-scrolled", window.scrollY > 24);
            backToTop?.classList.toggle("is-visible", window.scrollY > 720);

            const scrollable = Math.max(
                root.scrollHeight - window.innerHeight,
                1
            );
            const progress = Math.min(Math.max(window.scrollY / scrollable, 0), 1);
            root.style.setProperty("--page-scroll-progress", String(progress));
            queued = false;
        };

        window.addEventListener(
            "scroll",
            () => {
                if (queued) return;
                queued = true;
                window.requestAnimationFrame(update);
            },
            { passive: true }
        );

        window.addEventListener("resize", update, { passive: true });

        backToTop?.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: reducedMotion.matches ? "auto" : "smooth"
            });
        });

        update();
    };

    const initMobileNavigation = () => {
        const button = document.querySelector(".menu-button");
        const menu = document.getElementById("mobile-menu");
        if (!button || !menu) return;

        let closeTimer;

        const setOpen = (open, returnFocus = false) => {
            window.clearTimeout(closeTimer);
            button.setAttribute("aria-expanded", String(open));
            button.classList.toggle("is-open", open);
            document.body.classList.toggle("mobile-menu-open", open);

            if (open) {
                menu.hidden = false;
                menu.setAttribute("aria-hidden", "false");
                menu.inert = false;
                window.requestAnimationFrame(() => menu.classList.add("is-open"));
                return;
            }

            menu.classList.remove("is-open");
            menu.setAttribute("aria-hidden", "true");
            menu.inert = true;

            const finishClose = () => {
                menu.hidden = true;
                if (returnFocus) button.focus();
            };

            if (reducedMotion.matches) {
                finishClose();
            } else {
                closeTimer = window.setTimeout(finishClose, 330);
            }
        };

        menu.setAttribute("aria-hidden", "true");
        menu.inert = true;

        button.addEventListener("click", () => {
            setOpen(button.getAttribute("aria-expanded") !== "true");
        });

        menu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => setOpen(false));
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && button.getAttribute("aria-expanded") === "true") {
                setOpen(false, true);
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 980 && button.getAttribute("aria-expanded") === "true") {
                setOpen(false);
            }
        });
    };

    const initHero = () => {
        const hero = document.querySelector(".hero");
        const slides = Array.from(document.querySelectorAll("[data-hero-slide]"));
        const dots = Array.from(document.querySelectorAll("[data-hero-go]"));
        const toggle = document.querySelector("[data-hero-toggle]");
        const toggleLabel = document.querySelector("[data-hero-toggle-label]");

        if (!hero || slides.length < 2 || reducedMotion.matches) return;

        const interval = 7000;
        let activeIndex = 0;
        let timer;
        let manuallyPaused = false;

        hero.classList.add("hero-js-active");

        const render = (nextIndex) => {
            activeIndex = (nextIndex + slides.length) % slides.length;

            slides.forEach((slide, index) => {
                slide.classList.toggle("is-active", index === activeIndex);
            });

            dots.forEach((dot, index) => {
                const active = index === activeIndex;
                dot.classList.toggle("is-active", active);
                dot.setAttribute("aria-pressed", String(active));
            });
        };

        const stop = () => {
            window.clearInterval(timer);
            timer = undefined;
        };

        const start = () => {
            stop();
            if (manuallyPaused || document.hidden) return;
            timer = window.setInterval(() => render(activeIndex + 1), interval);
        };

        const updateToggle = () => {
            if (!toggle) return;
            toggle.setAttribute("aria-pressed", String(manuallyPaused));
            if (toggleLabel) {
                toggleLabel.textContent = manuallyPaused
                    ? "Resume image rotation"
                    : "Pause image rotation";
            }
        };

        dots.forEach((dot) => {
            dot.addEventListener("click", () => {
                render(Number(dot.dataset.heroGo));
                start();
            });
        });

        if (toggle) {
            toggle.addEventListener("click", () => {
                manuallyPaused = !manuallyPaused;
                updateToggle();
                start();
            });
        }

        hero.addEventListener(
            "pointermove",
            (event) => {
                if (event.pointerType === "touch") return;
                const bounds = hero.getBoundingClientRect();
                const horizontal = (event.clientX - bounds.left) / bounds.width - 0.5;
                const vertical = (event.clientY - bounds.top) / bounds.height - 0.5;
                hero.style.setProperty("--hero-shift-x", `${horizontal * -16}px`);
                hero.style.setProperty("--hero-shift-y", `${vertical * -10}px`);
            },
            { passive: true }
        );

        hero.addEventListener("pointerleave", () => {
            hero.style.setProperty("--hero-shift-x", "0px");
            hero.style.setProperty("--hero-shift-y", "0px");
        });

        document.addEventListener("visibilitychange", start);
        render(0);
        updateToggle();
        start();
    };

    const initReveals = () => {
        if (reducedMotion.matches || !("IntersectionObserver" in window)) return;

        const selector = [
            ".page-hero-inner",
            ".listing-hero-inner",
            ".policy-hero-inner",
            ".listing-switcher-inner",
            ".section-heading",
            ".listing-heading",
            ".catalogue-filters",
            ".journey-steps-heading",
            ".journey-steps-grid article",
            ".tour-card",
            ".destination-card",
            ".feature-grid article",
            ".testimonial-grid figure",
            ".credential-card",
            ".team-card",
            ".value-card",
            ".gallery-card",
            ".about-copy",
            ".about-image-wrap",
            ".journey-promise-grid > *",
            ".about-choice-grid > *",
            ".about-choice-grid li",
            ".breadcrumbs",
            ".detail-hero-grid > *",
            ".detail-main > section",
            ".itinerary-item",
            ".package-card",
            ".tour-map",
            ".detail-info-card",
            ".booking-card",
            ".booking-expectations li",
            ".contact-details > .eyebrow",
            ".contact-details > h2",
            ".contact-details > p",
            ".contact-method",
            ".contact-form-card",
            ".contact-help-card",
            ".confirmation-card",
            ".confirmation-mark",
            ".confirmation-notice",
            ".confirmation-summary",
            ".confirmation-summary dl > div",
            ".confirmation-next",
            ".confirmation-next li",
            ".confirmation-safety",
            ".confirmation-actions",
            ".policy-nav",
            ".policy-intro-card",
            ".policy-content > section",
            ".listing-help",
            ".final-cta",
            ".detail-final-cta > .container > div",
            ".footer-grid > div",
            ".footer-bottom"
        ].join(",");

        const elements = Array.from(document.querySelectorAll(selector));
        if (!elements.length) return;

        const groupedParents = new Map();

        const disableReveals = (error) => {
            document.documentElement.classList.remove("motion-ready");
            elements.forEach((element) => {
                element.classList.remove("motion-reveal", "is-visible");
            });

            if (error) {
                console.error("Motion reveals disabled after an initialization error.", error);
            }
        };

        try {
            elements.forEach((element) => {
                element.classList.add("motion-reveal");

                const parent = element.parentElement;
                const siblings = groupedParents.get(parent) || [];
                siblings.push(element);
                groupedParents.set(parent, siblings);

                if (element.classList.contains("about-copy")) {
                    element.dataset.revealSide = "left";
                }

                if (element.classList.contains("about-image-wrap")) {
                    element.dataset.revealSide = "right";
                }

                if (
                    element.parentElement?.classList.contains("detail-hero-grid") ||
                    element.parentElement?.classList.contains("contact-grid")
                ) {
                    element.dataset.revealSide =
                        element === element.parentElement.firstElementChild
                            ? "left"
                            : "right";
                }
            });

            groupedParents.forEach((siblings) => {
                siblings.forEach((element, index) => {
                    const delay = `${Math.min(index, 5) * 70}ms`;
                    const inlineStyle = element.getAttribute("style") || "";
                    const separator =
                        inlineStyle && !inlineStyle.trimEnd().endsWith(";")
                            ? ";"
                            : "";

                    element.setAttribute(
                        "style",
                        `${inlineStyle}${separator}--reveal-delay: ${delay};`
                    );
                });
            });

            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (!entry.isIntersecting) return;
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    });
                },
                {
                    rootMargin: "0px 0px -8% 0px",
                    threshold: 0.08
                }
            );

            elements.forEach((element) => observer.observe(element));
            document.documentElement.classList.add("motion-ready");

            window.setTimeout(() => {
                const hiddenInViewport = elements.some((element) => {
                    const bounds = element.getBoundingClientRect();
                    const intersectsViewport =
                        bounds.bottom > 0 && bounds.top < window.innerHeight;

                    return (
                        intersectsViewport &&
                        !element.classList.contains("is-visible")
                    );
                });

                if (hiddenInViewport) {
                    disableReveals(
                        new Error("Visible content was not released by the observer.")
                    );
                }
            }, 1200);
        } catch (error) {
            disableReveals(error);
        }
    };

    const initPolicyNavigation = () => {
        const links = Array.from(document.querySelectorAll(".policy-nav a[href^='#']"));
        if (!links.length || !("IntersectionObserver" in window)) return;

        const sections = links
            .map((link) => document.querySelector(link.getAttribute("href")))
            .filter(Boolean);

        const linkById = new Map(
            links.map((link) => [link.getAttribute("href").slice(1), link])
        );

        const setActive = (id) => {
            links.forEach((link) => {
                const active = link === linkById.get(id);
                link.classList.toggle("is-active", active);
                if (active) {
                    link.setAttribute("aria-current", "true");
                } else {
                    link.removeAttribute("aria-current");
                }
            });
        };

        const observer = new IntersectionObserver(
            (entries) => {
                const visible = entries
                    .filter((entry) => entry.isIntersecting)
                    .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

                if (visible[0]) setActive(visible[0].target.id);
            },
            {
                rootMargin: "-20% 0px -62% 0px",
                threshold: [0, 0.15, 0.35]
            }
        );

        sections.forEach((section) => observer.observe(section));

        links.forEach((link) => {
            link.addEventListener("click", () => {
                setActive(link.getAttribute("href").slice(1));
            });
        });
    };

    const initMapFrames = () => {
        document.querySelectorAll(".tour-map iframe").forEach((frame) => {
            const markLoaded = () => frame.parentElement?.classList.add("is-loaded");
            frame.addEventListener("load", markLoaded, { once: true });
            window.setTimeout(markLoaded, 1800);
        });
    };

    const initImageReveals = () => {
        const shells = Array.from(
            document.querySelectorAll(
                ".card-image-wrap, .gallery-card, .detail-image-wrap"
            )
        );

        if (!shells.length || reducedMotion.matches) return;

        shells.forEach((shell) => shell.classList.add("image-reveal-shell"));

        if (!("IntersectionObserver" in window)) {
            shells.forEach((shell) => shell.classList.add("is-image-visible"));
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add("is-image-visible");
                    observer.unobserve(entry.target);
                });
            },
            {
                rootMargin: "0px 0px -10% 0px",
                threshold: 0.12
            }
        );

        shells.forEach((shell) => observer.observe(shell));
    };

    const initItineraryProgress = () => {
        const lists = Array.from(document.querySelectorAll(".itinerary-list"));
        if (!lists.length) return;

        if (reducedMotion.matches) {
            lists.forEach((list) => {
                list.style.setProperty("--itinerary-progress", "1");
            });
            return;
        }

        let queued = false;

        const update = () => {
            lists.forEach((list) => {
                const bounds = list.getBoundingClientRect();
                const start = window.innerHeight * 0.72;
                const distance = Math.max(bounds.height + window.innerHeight * 0.18, 1);
                const progress = Math.min(
                    Math.max((start - bounds.top) / distance, 0),
                    1
                );
                list.style.setProperty("--itinerary-progress", String(progress));
            });
            queued = false;
        };

        const requestUpdate = () => {
            if (queued) return;
            queued = true;
            window.requestAnimationFrame(update);
        };

        window.addEventListener("scroll", requestUpdate, { passive: true });
        window.addEventListener("resize", requestUpdate, { passive: true });
        update();
    };

    const initGalleryLightbox = () => {
        const items = Array.from(document.querySelectorAll("[data-gallery-item]"));
        if (!items.length) return;

        const viewer = document.createElement("div");
        viewer.className = "gallery-lightbox";
        viewer.hidden = true;
        viewer.setAttribute("role", "dialog");
        viewer.setAttribute("aria-modal", "true");
        viewer.setAttribute("aria-label", "Travel gallery image viewer");
        viewer.innerHTML = `
            <span class="gallery-lightbox-count" aria-live="polite"></span>
            <button class="gallery-lightbox-close" type="button" aria-label="Close image viewer">×</button>
            <button class="gallery-lightbox-nav gallery-lightbox-prev" type="button" aria-label="Previous image">‹</button>
            <figure class="gallery-lightbox-stage">
                <img class="gallery-lightbox-image" alt="">
                <figcaption class="gallery-lightbox-caption">
                    <strong></strong>
                    <span></span>
                </figcaption>
            </figure>
            <button class="gallery-lightbox-nav gallery-lightbox-next" type="button" aria-label="Next image">›</button>
        `;
        document.body.append(viewer);

        const image = viewer.querySelector(".gallery-lightbox-image");
        const title = viewer.querySelector(".gallery-lightbox-caption strong");
        const caption = viewer.querySelector(".gallery-lightbox-caption span");
        const count = viewer.querySelector(".gallery-lightbox-count");
        const closeButton = viewer.querySelector(".gallery-lightbox-close");
        const previousButton = viewer.querySelector(".gallery-lightbox-prev");
        const nextButton = viewer.querySelector(".gallery-lightbox-next");
        const navigationButtons = [previousButton, nextButton];

        let activeIndex = 0;
        let lastTrigger;
        let closeTimer;

        navigationButtons.forEach((button) => {
            button.hidden = items.length < 2;
        });

        const render = (index) => {
            activeIndex = (index + items.length) % items.length;
            const item = items[activeIndex];
            const thumbnail = item.querySelector("img");

            image.src = item.dataset.gallerySrc;
            image.alt = thumbnail?.alt || item.dataset.galleryTitle || "Travel image";
            title.textContent = item.dataset.galleryTitle || "Uganda travel experience";
            caption.textContent = item.dataset.galleryCaption || "";
            caption.hidden = !caption.textContent;
            count.textContent = `${activeIndex + 1} / ${items.length}`;
        };

        const open = (index, trigger) => {
            window.clearTimeout(closeTimer);
            lastTrigger = trigger;
            render(index);
            viewer.hidden = false;
            document.body.classList.add("gallery-viewer-open");
            window.requestAnimationFrame(() => {
                viewer.classList.add("is-open");
                closeButton.focus();
            });
        };

        const close = () => {
            viewer.classList.remove("is-open");
            document.body.classList.remove("gallery-viewer-open");

            const finish = () => {
                viewer.hidden = true;
                image.removeAttribute("src");
                lastTrigger?.focus();
            };

            if (reducedMotion.matches) {
                finish();
            } else {
                closeTimer = window.setTimeout(finish, 300);
            }
        };

        items.forEach((item, index) => {
            const trigger = item.querySelector("[data-gallery-open]");
            trigger?.addEventListener("click", () => open(index, trigger));
        });

        closeButton.addEventListener("click", close);
        previousButton.addEventListener("click", () => render(activeIndex - 1));
        nextButton.addEventListener("click", () => render(activeIndex + 1));

        viewer.addEventListener("click", (event) => {
            if (event.target === viewer) close();
        });

        document.addEventListener("keydown", (event) => {
            if (viewer.hidden) return;

            if (event.key === "Escape") {
                close();
            } else if (event.key === "ArrowLeft" && items.length > 1) {
                render(activeIndex - 1);
            } else if (event.key === "ArrowRight" && items.length > 1) {
                render(activeIndex + 1);
            } else if (event.key === "Tab") {
                const focusable = [
                    closeButton,
                    ...navigationButtons.filter((button) => !button.hidden)
                ];
                const first = focusable[0];
                const last = focusable[focusable.length - 1];

                if (event.shiftKey && document.activeElement === first) {
                    event.preventDefault();
                    last.focus();
                } else if (!event.shiftKey && document.activeElement === last) {
                    event.preventDefault();
                    first.focus();
                }
            }
        });
    };

    const init = () => {
        initHeader();
        initMobileNavigation();
        initHero();
        initReveals();
        initPolicyNavigation();
        initMapFrames();
        initImageReveals();
        initItineraryProgress();
        initGalleryLightbox();
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();
