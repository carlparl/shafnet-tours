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
            ".journey-steps-heading",
            ".journey-steps-grid article",
            ".tour-card",
            ".destination-card",
            ".feature-grid article",
            ".testimonial-grid figure",
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

        document.documentElement.classList.add("motion-ready");

        const groupedParents = new Map();

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
                element.style.setProperty("--reveal-delay", `${Math.min(index, 5) * 70}ms`);
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

    const init = () => {
        initHeader();
        initMobileNavigation();
        initHero();
        initReveals();
        initPolicyNavigation();
        initMapFrames();
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();
