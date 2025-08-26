// components/GlobalCustomScrollbar.tsx
"use client";

import { useEffect } from "react";

/**
 * GlobalCustomScrollbar
 * - attach per-element custom scrollbar overlays to all scrollable elements automatically
 * - call this component once (e.g. in app/layout.tsx)
 */
export default function GlobalCustomScrollbar(): null {
  useEffect(() => {
    const PROCESSED_ATTR = "data-csb-processed";
    const overlays: HTMLElement[] = [];
    const cleanupFns: Array<() => void> = [];

    function isVisible(el: HTMLElement) {
      return el.offsetParent !== null || el === document.body || el === document.documentElement;
    }

    function isScrollable(el: HTMLElement) {
      try {
        const style = getComputedStyle(el);
        const oy = style.overflowY;
        return (
          (oy === "auto" || oy === "scroll" || oy === "overlay") &&
          el.scrollHeight > el.clientHeight
        );
      } catch {
        return false;
      }
    }

    function attachTo(el: HTMLElement) {
      if (el.hasAttribute(PROCESSED_ATTR)) return;
      if (!isVisible(el)) return;

      el.setAttribute(PROCESSED_ATTR, "1");
      el.classList.add("custom-scroll-hide");

      const computed = getComputedStyle(el).position;
      let changedPos = false;
      if (computed === "static" || !computed) {
        el.style.position = "relative";
        changedPos = true;
        el.dataset.csbOrigPos = "static";
      }

      const overlay = document.createElement("div");
      overlay.className = "custom-scrollbar-overlay";
      overlay.style.position = "absolute";
      overlay.style.top = "0";
      overlay.style.right = "2px";
      overlay.style.bottom = "0";
      overlay.style.width = "6px";
      overlay.style.pointerEvents = "auto";
      overlay.style.zIndex = "9999";
      overlay.style.display = "flex";
      overlay.style.alignItems = "flex-start";
      overlay.style.justifyContent = "center";

      const thumb = document.createElement("div");
      thumb.className = "custom-scrollbar-thumb";
      thumb.style.position = "absolute";
      thumb.style.top = "0";
      thumb.style.width = "100%";
      thumb.style.borderRadius = "9999px";
      thumb.style.cursor = "pointer";
      thumb.style.willChange = "transform";

      overlay.appendChild(thumb);
      el.appendChild(overlay);
      overlays.push(overlay);

      function updateThumb() {
        const ch = el.clientHeight;
        const contentH = el.scrollHeight;

        if (contentH <= ch) {
          thumb.style.display = "none";
          return;
        }

        thumb.style.display = "block";
        const thumbH = Math.max((ch * ch) / contentH, 20);
        const maxThumbTop = ch - thumbH;
        const scrollRatio = el.scrollTop / (contentH - ch);
        const top = scrollRatio * maxThumbTop;

        thumb.style.height = `${thumbH}px`;
        thumb.style.transform = `translateY(${top}px)`;

        thumb.dataset.thumbH = String(thumbH);
        thumb.dataset.maxThumbTop = String(maxThumbTop);
        thumb.dataset.maxScroll = String(contentH - ch);
      }

      updateThumb();

      const onScroll = () => updateThumb();
      el.addEventListener("scroll", onScroll);
      cleanupFns.push(() => el.removeEventListener("scroll", onScroll));

      const onResize = () => updateThumb();
      window.addEventListener("resize", onResize);
      cleanupFns.push(() => window.removeEventListener("resize", onResize));

      let dragging = false;
      let startY = 0;
      let startTop = 0;

      function onPointerDown(e: PointerEvent) {
        e.preventDefault();
        dragging = true;
        startY = e.clientY;

        const match = /translateY\(([\d.]+)px\)/.exec(thumb.style.transform || "");
        startTop = match ? parseFloat(match[1]) : 0;

        document.addEventListener("pointermove", onPointerMove);
        document.addEventListener("pointerup", onPointerUp);
        document.body.style.userSelect = "none";
      }

      function onPointerMove(e: PointerEvent) {
        if (!dragging) return;

        const deltaY = e.clientY - startY;
        const newTop = startTop + deltaY;

        const thumbH = parseFloat(thumb.dataset.thumbH || "20");
        const maxThumbTop = parseFloat(thumb.dataset.maxThumbTop || "0");
        const maxScroll = parseFloat(thumb.dataset.maxScroll || "0");

        const clampedTop = Math.max(0, Math.min(maxThumbTop, newTop));
        thumb.style.transform = `translateY(${clampedTop}px)`;

        const scrollRatio = clampedTop / maxThumbTop;
        el.scrollTop = scrollRatio * maxScroll;
      }

      function onPointerUp() {
        dragging = false;
        document.removeEventListener("pointermove", onPointerMove);
        document.removeEventListener("pointerup", onPointerUp);
        document.body.style.userSelect = "";
      }

      thumb.addEventListener("pointerdown", onPointerDown);
      cleanupFns.push(() => thumb.removeEventListener("pointerdown", onPointerDown));

      function onOverlayClick(e: MouseEvent) {
        if (e.target === thumb) return;
        const rect = overlay.getBoundingClientRect();
        const clickY = e.clientY - rect.top;
        const ch = el.clientHeight;
        const contentH = el.scrollHeight;
        const thumbH = thumb.offsetHeight;
        const maxThumbTop = ch - thumbH || 1;
        const ratio = Math.max(0, Math.min(1, (clickY - thumbH / 2) / maxThumbTop));
        const newScroll = ratio * (contentH - ch);
        el.scrollTop = newScroll;
      }
      overlay.addEventListener("click", onOverlayClick);
      cleanupFns.push(() => overlay.removeEventListener("click", onOverlayClick));

      const ro = new (window as any).ResizeObserver?.(() => updateThumb());
      if (ro) {
        ro.observe(el);
        cleanupFns.push(() => ro.disconnect());
      }

      if (changedPos) el.dataset.csbChangedPos = "1";
    }

    function scanAndAttach() {
      const nodes = Array.from(document.querySelectorAll<HTMLElement>("*"));
      for (const el of nodes) {
        try {
          if (el.hasAttribute(PROCESSED_ATTR)) continue;
          if (isScrollable(el)) attachTo(el);
        } catch {}
      }
    }

    const initialTimer = setTimeout(scanAndAttach, 50);

    let scanTimer: any = null;
    const mo = new MutationObserver(() => {
      if (scanTimer) clearTimeout(scanTimer);
      scanTimer = setTimeout(scanAndAttach, 120);
    });
    mo.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["class", "style"],
    });

    return () => {
      clearTimeout(initialTimer);
      mo.disconnect();
      cleanupFns.forEach((fn) => {
        try {
          fn();
        } catch {}
      });
      document.querySelectorAll<HTMLElement>("[data-csb-processed]").forEach((el) => {
        el.classList.remove("custom-scroll-hide");
        el.removeAttribute("data-csb-processed");
        if (el.dataset.csbChangedPos) {
          el.style.position = "";
          delete el.dataset.csbChangedPos;
        }
      });
      overlays.forEach((o) => o.remove());
    };
  }, []);

  return null;
}
