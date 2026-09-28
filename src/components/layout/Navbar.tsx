"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { Menu, ShieldCheck, X } from "lucide-react";
import { siteConfig } from "@/config/site";

export function Navbar() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [lastPathname, setLastPathname] = useState(pathname);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Close the mobile menu on navigation. Adjusting state during render (per
  // https://react.dev/learn/you-might-not-need-an-effect) instead of in an
  // effect avoids an extra render pass.
  if (pathname !== lastPathname) {
    setLastPathname(pathname);
    setMenuOpen(false);
  }

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-300 ${
        scrolled
          ? "border-b border-border bg-background/85 backdrop-blur-md"
          : "border-b border-transparent bg-transparent"
      }`}
    >
      <nav
        aria-label="Primary"
        className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6"
      >
        <Link
          href="/"
          className="flex items-center gap-2 text-sm font-semibold tracking-tight text-foreground"
        >
          <ShieldCheck className="h-5 w-5 text-accent" aria-hidden="true" />
          <span>{siteConfig.shortName}</span>
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {siteConfig.nav.map((item) => {
            const active =
              item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`relative rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                  active ? "text-foreground" : "text-muted hover:text-foreground"
                }`}
              >
                {item.label}
                {active && (
                  <span className="absolute inset-x-4 -bottom-[1px] h-px bg-accent" />
                )}
              </Link>
            );
          })}
        </div>

        <div className="hidden md:block">
          <Link
            href="/join"
            className="inline-flex items-center justify-center rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-background transition-all hover:bg-accent/90 hover:shadow-[0_0_0_1px_rgba(56,189,248,0.4),0_8px_24px_-8px_rgba(56,189,248,0.55)] active:scale-[0.98]"
          >
            Join the Community
          </Link>
        </div>

        <button
          type="button"
          onClick={() => setMenuOpen((open) => !open)}
          aria-expanded={menuOpen}
          aria-controls="mobile-nav"
          aria-label={menuOpen ? "Close menu" : "Open menu"}
          className="flex h-10 w-10 items-center justify-center rounded-full border border-border text-foreground md:hidden"
        >
          {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </nav>

      <div
        id="mobile-nav"
        className={`overflow-hidden border-b border-border bg-background/95 backdrop-blur-md transition-[max-height,opacity] duration-300 md:hidden ${
          menuOpen ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
        }`}
      >
        <div className="flex flex-col gap-1 px-6 py-4">
          {siteConfig.nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-lg px-3 py-2.5 text-sm font-medium text-foreground/90 hover:bg-white/[0.04] hover:text-accent"
            >
              {item.label}
            </Link>
          ))}
          <Link
            href="/join"
            className="mt-2 inline-flex items-center justify-center rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-background"
          >
            Join the Community
          </Link>
        </div>
      </div>
    </header>
  );
}
